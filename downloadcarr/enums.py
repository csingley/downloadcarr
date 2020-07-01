"""Enumerated values used by *arr API
"""
import enum


@enum.unique
class HttpMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


@enum.unique
class SortKey(enum.Enum):
    SERIESTITLE = "series.title"
    DATE = "date"
    AIRDATE = "airDateUtc"
    MOVIETITLE = "movie.title"


@enum.unique
class SortDirection(enum.Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


@enum.unique
class Protocol(enum.Enum):
    USENET = "usenet"
    TORRENT = "torrent"


@enum.unique
class ImportMode(enum.Enum):
    """Handling instructions for *arr /command Downloaded*Scan
    """
    MOVE = "Move"
    COPY = "Copy"
