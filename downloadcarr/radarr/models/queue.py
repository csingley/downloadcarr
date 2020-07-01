"""
https://github.com/Radarr/Radarr/wiki/API:Queue
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple

from downloadcarr.models import Base
from downloadcarr import enums

from .movie import Movie
from .quality import QualityRevision


@dataclass(frozen=True)
class StatusMessage(Base):
    """Radarr QueueItem status message.

    Attribute of QueueItem
    """
    title: str
    messages: Tuple[str, ...] = ()


@dataclass(frozen=True)
class QueueItem(Base):
    """Object holding queue item information from Radarr.

    Returned by /queue.
    """

    movie: Movie
    quality: QualityRevision
    size: int
    title: str
    sizeleft: float
    timeleft: timedelta
    estimatedCompletionTime: datetime
    status: str
    trackedDownloadStatus: str
    downloadId: str
    protocol: enums.Protocol
    id: int
    statusMessages: Tuple[StatusMessage, ...] = ()
