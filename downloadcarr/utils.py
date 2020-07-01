"""Common utility functions and constants used in this package.
"""
from datetime import datetime, timezone, time
from typing import Tuple


NoneType = type(None)
UTC = timezone.utc


BOOL2JSON = {True: "true", False: "false"}


def _parse_usec(dt_str: str) -> Tuple[str, int]:
    """Strip microsecond from ISO-8601 time string.
    Return stripped string and microseconds cast to int val.
    """
    if "." in dt_str:
        dt_str, frac_sec = dt_str.split(".")
        num_digits = len(frac_sec)
        microsecond = round(int(frac_sec) / 10**(num_digits - 6))
    else:
        microsecond = 0

    return dt_str, microsecond


def datetime_fromisoformat(dt_str: str) -> datetime:
    """Parse ISO-8601 datetime strings as provided by Sonarr's API.

    Specifically handle:
        * "Zulu" milspeak for UTC
        * fractional seconds other than exactly 3 or 6 digits (milli/microseconds)

    ... all of which are legal per ISO-8601 and used by Sonarr's API, but blow up
    datetime.datetime.fromisoformat().

    N.B. a more general solution is to use the dateutil package to parse ISO-8601,
    but the dependency seems like overkill given the stability and predictability
    of Sonarr's APi in this regard.
    """
    # "Zulu" milspeak for UTC
    # HACK - brittle inelegant hardcode
    assert dt_str.endswith("Z")
    dt_str = dt_str[:-1]

    # datetime.datetime.fromisoformat() blows up if fractional seconds don't
    # have exactly 3 or 6 digits.
    #
    # datetime.datetime.strptime() zero-pads (on the right) fractional seconds
    # with fewer than 6 digits (good) but still blows up if fractional seconds
    # have more than 6 digits (bad).
    #
    # Sonarr API returns fractional seconds with arbitrary digits, so we need
    # to parse them manually.
    dt_str, microsecond = _parse_usec(dt_str)
    #  if "." in dt_str:
    #      dt_str, frac_sec = dt_str.split(".")
    #      num_digits = len(frac_sec)
    #      microsecond = round(int(frac_sec) / 10**(num_digits - 6))
    #  else:
    #      microsecond = 0

    dt = datetime.fromisoformat(dt_str)
    return dt.replace(microsecond=microsecond, tzinfo=UTC)


def time_fromisoformat(time_str: str) -> datetime:
    """Parse ISO-8601 time strings as provided by Sonarr's API.

    Specifically handle:
        * fractional seconds other than exactly 3 or 6 digits (milli/microseconds)

    ... which are legal per ISO-8601 and used by Sonarr's API, but blow up
    datetime.time.fromisoformat().

    N.B. a more general solution is to use the dateutil package to parse ISO-8601,
    but the dependency seems like overkill given the stability and predictability
    of Sonarr's APi in this regard.
    """
    # datetime.time.fromisoformat() blows up if fractional seconds don't
    # have exactly 3 or 6 digits.
    #
    # Sonarr API returns fractional seconds with arbitrary digits, so we need
    # to parse them manually.
    time_str, microsecond = _parse_usec(time_str)
    #  if "." in dt_str:
    #      dt_str, frac_sec = dt_str.split(".")
    #      num_digits = len(frac_sec)
    #      microsecond = round(int(frac_sec) / 10**(num_digits - 6))
    #  else:
    #      microsecond = 0

    t = time.fromisoformat(time_str)
    return t.replace(microsecond=microsecond, tzinfo=None)
