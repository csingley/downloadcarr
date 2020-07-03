"""
"""
from dataclasses import dataclass
from typing import Optional, Tuple
from datetime import datetime, timedelta

from downloadcarr import enums

from .base import Base


@dataclass(frozen=True)
class CommandStatusBody(Base):
    """Attribute of CommandStatus."""

    sendUpdatesToClient: bool
    updateScheduledTask: bool
    completionMessage: str
    name: str
    trigger: str
    isNewSeries: Optional[bool] = None
    requiresDiskAccess: Optional[bool] = None
    isExclusive: Optional[bool] = None
    suppressMessages: Optional[bool] = None
    seriesId: Optional[int] = None
    seriesIds: Tuple[int, ...] = ()
    episodeId: Optional[int] = None
    episodeIds: Tuple[int, ...] = ()
    movieId: Optional[int] = None
    movieIds: Tuple[int, ...] = ()
    listId: Optional[int] = None
    seasonNumber: Optional[int] = None
    sendUpdates: Optional[bool] = None
    importMode: Optional[str] = None
    type: Optional[str] = None
    filterValue: Optional[bool] = None
    filterKey: Optional[str] = None


@dataclass(frozen=True)
class CommandStatus(Base):
    """Sonarr command status.

    Returned by /command.
    """

    name: str
    state: str
    startedOn: datetime
    sendUpdatesToClient: bool
    id: int
    message: Optional[str] = None
    body: Optional[CommandStatusBody] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    queued: Optional[datetime] = None
    started: Optional[datetime] = None
    trigger: Optional[str] = None
    manual: Optional[bool] = None
    updateScheduledTask: Optional[bool] = None
    stateChangeTime: Optional[datetime] = None
    ended: Optional[datetime] = None
    duration: Optional[timedelta] = None


@dataclass(frozen=True)
class Rating(Base):
    """Review site rating metadata
    """

    votes: int
    value: float


@dataclass(frozen=True)
class Image(Base):
    """Image metadata.
    """

    coverType: str
    url: str


@dataclass(frozen=True)
class DownloadData(Base):
    """Attribute of Download.
    """

    droppedPath: Optional[str] = None
    importedPath: Optional[str] = None
    reason: Optional[str] = None
    indexer: Optional[str] = None
    nzbInfoUrl: Optional[str] = None
    releaseGroup: Optional[str] = None
    age: Optional[str] = None
    ageHours: Optional[str] = None
    ageMinutes: Optional[str] = None
    publishedDate: Optional[datetime] = None
    downloadClient: Optional[str] = None
    size: Optional[str] = None
    downloadUrl: Optional[str] = None
    guid: Optional[str] = None
    tvdbId: Optional[str] = None
    tvRageId: Optional[str] = None
    protocol: Optional[enums.Protocol] = None
    torrentInfoHash: Optional[str] = None
    message: Optional[str] = None


@dataclass(frozen=True)
class DiskSpace(Base):
    """Disk space information.

    Returned by /diskspace.
    """

    path: str
    label: str
    freeSpace: int
    totalSpace: int


@dataclass(frozen=True)
class UnmappedFolder(Base):
    """Attribute of RootFolder"""

    name: str
    path: str


@dataclass(frozen=True)
class RootFolder(Base):
    """Returned by /rootfolder."""

    path: str
    freeSpace: int
    unmappedFolders: Tuple[UnmappedFolder, ...]
    id: int
    totalSpace: Optional[int] = None


@dataclass(frozen=True)
class SystemStatus(Base):
    """Returned by /system/status."""

    version: str
    buildTime: datetime
    isDebug: bool
    isProduction: bool
    isAdmin: bool
    isUserInteractive: bool
    startupPath: str
    appData: str
    osVersion: str
    isMono: bool
    isLinux: bool
    isWindows: bool
    branch: str
    authentication: bool
    urlBase: str
    startOfWeek: Optional[int] = None
    osName: Optional[str] = None
    runtimeVersion: Optional[str] = None
    runtimeName: Optional[str] = None
    isMonoRuntime: Optional[bool] = None
    isOsx: Optional[bool] = None
    sqliteVersion: Optional[str] = None


@dataclass(frozen=True)
class SystemBackup(Base):
    """Returned by /system/backup."""

    name: str
    path: str
    type: str
    time: datetime
    id: int
