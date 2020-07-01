"""
"""
from pathlib import Path

from .. import mock_server


def load(filename):
    """Load test data from file."""

    path = Path(__file__).parent / "data" / filename
    with open(path) as f:
        return f.read()


CALENDAR = load("calendar.json")
COMMANDS = load("commands.json")
COMMAND = load("command.json")
COMMANDPOST = load("command-post.json")
DISKSPACE = load("diskspace.json")
HISTORY = load("history.json")
MOVIES = load("movies.json")
MOVIE = load("movie.json")
MOVIEPOST = load("movie-post.json")
MOVIELOOKUP = load("movie-lookup.json")
QUEUE = load("queue.json")
SYSTEMSTATUS = load("system-status.json")
