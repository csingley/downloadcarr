"""Object model for Sonarr API.

https://github.com/Sonarr/Sonarr/wiki/API
"""
__all__ = [
    "Episode",
    "EpisodeFile",
    "WantedMissing",
    "DownloadData",
    "Download",
    "History",
    "QueueItem",
    "SeriesTitleInfo",
    "ParsedEpisodeInfo",
    "ParseResult",
    "Revision",
    "Quality",
    "QualityValue",
    "QualityProfile",
    "QualityRevision",
    "QualityAllowed",
    "QualityAllowedProfile",
    "Release",
    "SeasonStatistics",
    "Season",
    "Rating",
    "AlternateTitle",
    "Image",
    "Tag",
    "Series",
]

# /calendar classes in .episode
# /command classes in downloadcarr.models
# /diskspace classes in .system
from .episode import MediaInfo, EpisodeFile, Episode, WantedMissing
from .history import DownloadData, Download, History

# TODO Images
# /wanted/missing classes in .episode
from .queue import QueueItem
from .parse import SeriesTitleInfo, ParsedEpisodeInfo, ParseResult

# /profile classes in .quality
from .quality import (
    Revision,
    Quality,
    QualityValue,
    QualityProfile,
    QualityRevision,
    QualityAllowed,
    QualityAllowedProfile,
)
from .release import Release

# /release/push classes in .release
# /rootfolder classes in .system
from .series import (
    SeasonStatistics,
    Season,
    Rating,
    AlternateTitle,
    Image,
    Tag,
    AddOptions,
    Series,
)

# /series/lookup classes in .series
# /system classes in downloadcarr.models
# /system/backup classes in .system
# /tag classes in .series
