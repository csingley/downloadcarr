"""
"""
from dataclasses import dataclass
from typing import Optional, Tuple

from downloadcarr.models import Base


@dataclass(frozen=True)
class Quality(Base):
    """Quality definition.

    Attribute of QualityRevision
    """

    id: int
    name: Optional[str] = None
    source: Optional[str] = None
    resolution: Optional[str] = None
    weight: Optional[int] = None
    modifier: Optional[str] = None


@dataclass(frozen=True)
class Revision(Base):
    """Attribute of QualityRevision
    """

    version: int
    real: int


@dataclass(frozen=True)
class QualityRevision(Base):
    """Attribute of Download, QueueItem, EpisodeFile, Release.
    """

    quality: Quality
    customFormats: Tuple[str, ...] = ()
    revision: Optional[Revision] = None
    proper: Optional[bool] = None
    hardcodedSubs: Optional[str] = None
