"""Base classes for logic common to *arr API JSON objects.

Note that the JSON objects of *arr APIs don't contain metadata that would allow
us to introspect type from the data stream itself, so we can't really implement
a Python <--> JSON codec as a custom (json.JSONEncoder, json.JSONDecoder).

Instead we must rely on a schema defined out of band, which we provide as
``models`` subpackages.  Here we define a base class for these models,
implementing the rest of needed type conversion & validation logic beyond
the basic serialization/deserialization provided by stdlib json, i.e.

    JSON            Python
    ====            ======
    object          dict
    array           list
    string          unicode
    number (int)    int, long
    number (real)   float
    true            True
    false           False
    null            None
"""

import dataclasses
from typing import Tuple, Optional, Union
from datetime import date, datetime, time, timedelta
import enum

from downloadcarr import utils


class Base:
    """Base class for *arr API JSON objects.

    The decoder i.e. from_dict() introspects data type from hints in the model
    definition, and applies appropriate transforms to the values.

    The encoder i.e. to_dict() uses attribute type (not hints) to serialize
    any data type not handled natively by json.JSONEncoder.
    """

    def to_dict(self) -> dict:
        """Generate input suitable to stock json.JSONDecoder.
        """
        if type(self) is Base:
            raise NotImplementedError("Don't use base class, only subclasses.")

        encoded = encode_dict(dataclasses.asdict(self))
        return encoded

    @classmethod
    def from_dict(cls, data: dict) -> "Base":
        """Instantiate from output of stock json.JSONDecoder.
        """
        if cls is Base:
            raise NotImplementedError("Don't use base class, only subclasses.")

        try:
            classtypes = {fd.name: fd.type for fd in dataclasses.fields(cls)}
        except TypeError:
            raise TypeError(f"{cls.__name__} must be a dataclasses.dataclass")

        if not hasattr(data, "items") or not callable(data.items):
            msg = (
                f"{cls.__name__}.from_dict(): "
                f"type(arg) must be dict not {type(data)}"
                f"\n\n{data}"
            )
            raise TypeError(msg)

        decoded = {}
        for attr, val in data.items():
            if attr not in classtypes:
                msg = (f"{cls.__name__}.from_dict() got an unexpected keyword "
                       f"argument {attr}={val}")
                raise TypeError(msg)

            attr_type = classtypes[attr]

            try:
                if hasattr(attr_type, "__origin__"):
                    # Generic type from ``typing`` module
                    attr_type, decoder = make_decoder_generic(attr_type)
                else:
                    decoder = make_decoder_specific(attr_type)

                decoded_val = decoder(attr_type, val)
            except Exception as err:
                errmsg = err.args[0]
                msg = f"{cls.__name__}.{attr}(type {attr_type})={val}: {type(err).__name__} - {errmsg}"
                raise ValueError(msg)

            decoded[attr] = decoded_val

        try:
            instance = cls(**decoded)
        except Exception as e:
            msg = f"{cls.__name__}.from_dict() failed: " + e.args[0]
            raise ValueError(msg)
        return instance


def encode_basic(val: Union[bool, int, float, str]) -> Union[bool, int, float, str]:
    return val


def encode_datetime(val: datetime) -> str:
    """'Zulu' milspeak for UTC
    """
    encoded = val.replace(tzinfo=None).isoformat()
    if "." in encoded:
        encoded = encoded.rstrip("0")

    return encoded + "Z"


def encode_date(val: date) -> str:
    encoded = val.isoformat()
    return encoded


def encode_time(val: time) -> str:
    encoded = val.replace(tzinfo=None).isoformat()
    return encoded.rstrip("0")


def encode_timedelta(val: timedelta) -> str:
    minutes, seconds = divmod(val.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    encoded = f"{hours:02}:{minutes:02}:{seconds:02}"
    if val.microseconds != 0:
        encoded += f".{val.microseconds:06}"
    return encoded.rstrip("0")


def encode_tuple(val: tuple) -> list:
    encoded = [TYPE_ENCODERS[type(v)](v) for v in val]
    return encoded


def encode_dict(val: dict) -> dict:
    def enc(v):
        if isinstance(v, enum.Enum):
            v_enc = v.value
        else:
            encoder = TYPE_ENCODERS[type(v)]
            v_enc = encoder(v)
        return v_enc

    return {attr: enc(v) for attr, v in val.items()}


TYPE_ENCODERS = {
    utils.NoneType: encode_basic,
    bool: encode_basic,
    int: encode_basic,
    float: encode_basic,
    str: encode_basic,
    datetime: encode_datetime,
    date: encode_date,
    time: encode_time,
    timedelta: encode_timedelta,
    tuple: encode_tuple,
    dict: encode_dict,
}


def make_decoder_generic(attr_type):
    origin = attr_type.__origin__
    args = attr_type.__args__
    # Of the generic type constructors, Sonarr API models only use:
    #   - variable length Tuple of homogenous type e.g. Tuple[str, ...]
    #   - Optional type i.e. Union[str, NoneType]
    if origin is tuple:
        if len(args) != 2 or args[-1] is not Ellipsis:
            msg = "Tuple attribute definition must contain Ellipsis"
            raise ValueError(msg)

        attr_type = args[0]
        decoder = decode_list_to_tuple
    else:
        assert origin is Union
        if len(args) != 2 or args[-1] is not utils.NoneType:
            msg = "Union attribute definition only allowed as Optional"
            raise TypeError(msg)

        attr_type = args[0]
        decoder = decode_optional

    return attr_type, decoder


def decode_list_to_tuple(attr_type, val: list) -> Tuple:
    decoder = make_decoder_specific(attr_type)
    return tuple(decoder(attr_type, item) for item in val)


def decode_optional(attr_type, val) -> Optional:
    if val is None:
        return None
    elif issubclass(attr_type, Base) and len(val) == 0:
        return None

    decoder = make_decoder_specific(attr_type)
    return decoder(attr_type, val)


def make_decoder_specific(attr_type):
    if issubclass(attr_type, Base):
        return decode_model
    elif issubclass(attr_type, enum.Enum):
        return decode_enum
    else:
        assert attr_type in TYPE_DECODERS
        return TYPE_DECODERS[attr_type]


def decode_model(attr_type: Base, val: dict) -> Base:
    return attr_type.from_dict(val)


def decode_enum(attr_type: enum.Enum, val) -> enum.Enum:
    members = {member.value: member for member in attr_type}
    return members[val]


def decode_basic(attr_type, val) -> Union[bool, int, float, str]:
    # There's some slop in the Sonarr API w/r/t int vs. float
    # e.g. models.series.SeasonStatistics.percentOfEpisodes
    return attr_type(val)


def decode_datetime(attr_type, val) -> datetime:
    return utils.datetime_fromisoformat(val)


def decode_date(attr_type, val) -> date:
    return date.fromisoformat(val)


def decode_time(attr_type, val) -> time:
    #  return time.fromisoformat(val)
    return utils.time_fromisoformat(val)


def decode_timedelta(attr_type, val) -> timedelta:
    # datetime.timedelta lacks a parsing constructor, so reuse
    # time_fromisoformat() and cast as datetime.timedelta.
    #  tm = time.fromisoformat(val)
    tm = utils.time_fromisoformat(val)
    return timedelta(
        hours=tm.hour,
        minutes=tm.minute,
        seconds=tm.second,
        microseconds=tm.microsecond
    )


TYPE_DECODERS = {
    bool: decode_basic,
    int: decode_basic,
    float: decode_basic,
    str: decode_basic,
    datetime: decode_datetime,
    date: decode_date,
    time: decode_time,
    timedelta: decode_timedelta,
}
