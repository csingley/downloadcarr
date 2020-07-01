"""
https://github.com/Radarr/Radarr/wiki/API:Movie
"""
from dataclasses import dataclass
from typing import Tuple, Optional
from datetime import datetime, timedelta

from downloadcarr.models import Base, Rating, Image
from .quality import QualityRevision


@dataclass(frozen=True)
class MediaInfo(Base):
    """Audio/video quality metadata

    Attribute of MovieFile
    """

    containerFormat: str
    videoFormat: str
    videoCodecID: str
    videoProfile: str
    videoCodecLibrary: str
    videoBitrate: int
    videoBitDepth: int
    videoMultiViewCount: int
    videoColourPrimaries: str
    videoTransferCharacteristics: str
    width: int
    height: int
    audioFormat: str
    audioCodecID: str
    audioCodecLibrary: str
    audioAdditionalFeatures: str
    audioBitrate: int
    runTime: timedelta
    audioStreamCount: int
    audioChannels: int
    audioChannelPositions: str
    audioChannelPositionsText: str
    audioProfile: str
    videoFps: float
    audioLanguages: str
    subtitles: str
    scanType: str
    schemaRevision: int


@dataclass(frozen=True)
class AlternativeTitle(Base):
    """Attribute of Movie
    """

    sourceType: str
    movieId: int
    title: str
    sourceId: int
    votes: int
    voteCount: int
    language: str
    id: int


@dataclass(frozen=True)
class MovieFile(Base):
    movieId: int
    relativePath: str
    size: int
    dateAdded: datetime
    quality: QualityRevision
    id: int
    mediaInfo: Optional[MediaInfo] = None
    sceneName: Optional[str] = None
    edition: Optional[str] = None
    releaseGroup: Optional[str] = None


@dataclass(frozen=True)
class Movie(Base):
    """Movie metadata.

    Returned by /movie, /calendar, /history
    """

    title: str
    sortTitle: str
    sizeOnDisk: int
    status: str
    images: Tuple[Image, ...]
    downloaded: bool
    year: int
    hasFile: bool
    profileId: int
    monitored: bool
    runtime: int
    tmdbId: int
    titleSlug: str
    genres: Tuple[str, ...]
    added: datetime
    qualityProfileId: int
    alternativeTitles: Tuple[AlternativeTitle, ...] = ()
    #  alternativeTitles: Tuple[str, ...] = ()
    tags: Tuple[int, ...] = ()
    secondaryYear: Optional[int] = None
    id: Optional[int] = None
    path: Optional[str] = None
    cleanTitle: Optional[str] = None
    imdbId: Optional[str] = None
    overview: Optional[str] = None
    inCinemas: Optional[datetime] = None
    website: Optional[str] = None
    youTubeTrailerId: Optional[str] = None
    studio: Optional[str] = None
    lastInfoSync: Optional[datetime] = None
    ratings: Optional[Rating] = None
    secondaryYearSourceId: Optional[int] = None
    remotePoster: Optional[str] = None
    pathState: Optional[str] = None
    isAvailable: Optional[bool] = None
    folderName: Optional[str] = None
    minimumAvailability: Optional[str] = None
    physicalRelease: Optional[datetime] = None
    physicalReleaseNote: Optional[str] = None
    movieFile: Optional[MovieFile] = None
