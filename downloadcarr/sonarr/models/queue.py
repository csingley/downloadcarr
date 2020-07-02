"""
https://github.com/Sonarr/Sonarr/wiki/Queue
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple, Optional

from downloadcarr.models import Base
from downloadcarr import enums
from .series import Series
from .episode import Episode
from .quality import QualityRevision


@dataclass(frozen=True)
class QueueItem(Base):
    """Object holding queue item information from Sonarr.

    Returned by /queue.
    """

    series: Series
    episode: Episode
    quality: QualityRevision
    size: int
    title: str
    sizeleft: int
    status: str
    trackedDownloadStatus: str
    statusMessages: Tuple[str, ...]
    downloadId: str
    protocol: enums.Protocol
    id: int
    timeleft: Optional[timedelta] = None
    estimatedCompletionTime: Optional[datetime] = None
