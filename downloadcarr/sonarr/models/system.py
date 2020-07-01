"""
https://github.com/Sonarr/Sonarr/wiki/Diskspace
https://github.com/Sonarr/Sonarr/wiki/Rootfolder
https://github.com/Sonarr/Sonarr/wiki/System-Status
https://github.com/Sonarr/Sonarr/wiki/System-Backup

DiskSpace, SystemStatus implemented in downloadcarr.models.common
"""
from dataclasses import dataclass
from typing import Tuple, Optional
from datetime import datetime

from downloadcarr.models import Base, DiskSpace, SystemStatus


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
class SystemBackup(Base):
    """Returned by /system/backup."""

    name: str
    path: str
    type: str
    time: datetime
    id: int
