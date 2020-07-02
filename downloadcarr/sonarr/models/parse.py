"""
https://github.com/Sonarr/Sonarr/wiki/Parse
"""
from dataclasses import dataclass
from typing import Tuple, Optional

from downloadcarr.models import Base
from .episode import Episode
from .series import Series
from .quality import QualityRevision


@dataclass(frozen=True)
class SeriesTitleInfo(Base):
    """Attribute of ParsedEpisodeInfo."""

    title: str
    titleWithoutYear: str
    year: int


@dataclass(frozen=True)
class ParsedEpisodeInfo(Base):
    """Attribute of ParseResult."""

    releaseTitle: str
    seriesTitle: str
    seriesTitleInfo: SeriesTitleInfo
    quality: QualityRevision
    seasonNumber: int
    episodeNumbers: Tuple[int, ...]
    absoluteEpisodeNumbers: Tuple[int, ...]
    language: str
    fullSeason: bool
    special: bool
    releaseHash: str
    isDaily: bool
    isAbsoluteNumbering: bool
    isPossibleSpecialEpisode: bool
    releaseGroup: Optional[str] = None
    isPartialSeason: Optional[bool] = None
    isSeasonExtra: Optional[bool] = None
    seasonPart: Optional[int] = None
    isPossibleSceneSeasonSpecial: Optional[bool] = None
    specialAbsoluteEpisodeNumbers: Tuple[int, ...] = ()


@dataclass(frozen=True)
class ParseResult(Base):
    """Returns the result of parsing a title or path.
    Series and episodes will be returned only if the parsing matches to a
    specific series and one or more episodes.

    Returned by /parse.
    """

    parsedEpisodeInfo: ParsedEpisodeInfo
    episodes: Tuple[Episode, ...]
    title: Optional[str] = None
    series: Optional[Series] = None
