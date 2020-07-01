"""
https://github.com/Sonarr/Sonarr/wiki/History
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Optional

from downloadcarr.models import Base, PageMixin, DownloadData
from .episode import Episode
from .series import Series
from .quality import QualityRevision


@dataclass(frozen=True)
class Download(Base):
    """Episode download report.

    Attribute of History.
    """

    episodeId: int
    seriesId: int
    sourceTitle: str
    quality: QualityRevision
    qualityCutoffNotMet: bool
    date: datetime
    eventType: str
    data: DownloadData
    episode: Episode
    series: Series
    id: int
    downloadId: Optional[str] = None


@dataclass(frozen=True)
class History(Base, PageMixin):
    """Page of episode download history.

    Returned by /history.
    """
    records: Tuple[Download, ...]
