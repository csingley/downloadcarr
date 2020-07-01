"""
"""
from pathlib import Path

from .. import mock_server, COMMANDS, COMMAND, DISKSPACE, SYSTEMSTATUS


def load(filename):
    """Load test data from file."""

    path = Path(__file__).parent / "data" / filename
    with open(path) as f:
        return f.read()


CALENDAR = load("calendar.json")
EPISODES = load("episodes.json")
EPISODE = load("episode.json")
EPISODEFILES = load("episodefiles.json")
EPISODEFILE = load("episodefile.json")
HISTORY = load("history.json")
PARSE = load("parse.json")
PROFILE = load("profile.json")
QUEUE = load("queue.json")
RELEASE = load("release.json")
ROOTFOLDER = load("rootfolder.json")
ALLSERIES = load("allseries.json")
SERIES = load("series.json")
SERIESPOST = load("series-post.json")
SERIESLOOKUP = load("series-lookup.json")
SYSTEMBACKUP = load("system-backup.json")
TAGS = load("tags.json")
TAG = load("tag.json")
WANTEDMISSING = load("wanted-missing.json")
