"""
https://github.com/Sonarr/Sonarr/wiki/Calendar
https://github.com/Sonarr/Sonarr/wiki/Episode
https://github.com/Sonarr/Sonarr/wiki/EpisodeFile
https://github.com/Sonarr/Sonarr/wiki/Wanted-Missing
"""
from dataclasses import dataclass
from typing import Optional, Tuple
from datetime import datetime, date

from downloadcarr.models import Base, PageMixin
from .series import Series
from .quality import QualityRevision


@dataclass(frozen=True)
class MediaInfo(Base):
    """Attribute of EpisodeFile
    """

    audioChannels: float
    audioCodec: str
    videoCodec: str


@dataclass(frozen=True)
class EpisodeFile(Base):
    """TV series episode file metadata.

    Returned by /episodefile.
    """

    seriesId: int
    seasonNumber: int
    path: str
    size: int
    dateAdded: datetime
    quality: QualityRevision
    id: int
    relativePath: Optional[str] = None
    mediaInfo: Optional[MediaInfo] = None
    originalFilePath: Optional[str] = None
    qualityCutoffNotMet: Optional[bool] = None
    sceneName: Optional[str] = None


@dataclass(frozen=True)
class Episode(Base):
    """TV series episode metadata.

    Returned by /calendar, /episode.

    Attribute of Download, ParseResult, WantedMissing.
    """

    seriesId: int
    episodeFileId: int
    seasonNumber: int
    episodeNumber: int
    title: str
    hasFile: bool
    monitored: bool
    id: int
    airDate: Optional[date] = None
    airDateUtc: Optional[datetime] = None
    overview: Optional[str] = None
    absoluteEpisodeNumber: Optional[int] = None
    sceneSeasonNumber: Optional[int] = None
    sceneEpisodeNumber: Optional[int] = None
    sceneAbsoluteEpisodeNumber: Optional[int] = None
    tvDbEpisodeId: Optional[int] = None
    series: Optional[Series] = None
    downloading: Optional[bool] = None
    unverifiedSceneNumbering: Optional[bool] = None
    lastSearchTime: Optional[datetime] = None
    episodeFile: Optional[EpisodeFile] = None


@dataclass(frozen=True)
class WantedMissing(Base, PageMixin):
    """Page of wanted Episodes that are missing.

    Returned by /wanted/missing.
    """

    records: Tuple[Episode, ...]
