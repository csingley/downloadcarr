"""
https://github.com/Radarr/Radarr/wiki/API:History
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Optional, Literal

from downloadcarr.models import Base, PageMixin, DownloadData
from downloadcarr import enums
from .movie import Movie
from .quality import QualityRevision


@dataclass(frozen=True)
class Download(Base):
    """Episode download report.

    Attribute of History.
    """

    episodeId: int
    seriesId: int
    movieId: int
    sourceTitle: str
    quality: QualityRevision
    qualityCutoffNotMet: bool
    date: datetime
    eventType: str
    data: DownloadData
    movie: Movie
    id: int
    downloadId: Optional[str] = None


@dataclass(frozen=True)
class History(Base, PageMixin):
    """Page of episode download history.

    Returned by /history.
    """
    records: Tuple[Download, ...]
