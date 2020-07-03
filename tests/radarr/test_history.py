"""Tests for Radarr /history endpoint.

https://github.com/Radarr/Radarr/wiki/API:History
"""
import json
from datetime import datetime
from dataclasses import replace

import pytest

from downloadcarr.models import DownloadData
from downloadcarr.radarr import models
from downloadcarr import enums
from downloadcarr.utils import UTC

from . import HISTORY, mock_server, CLIENT


def test_download() -> None:
    """Test the Download model."""
    #  instance from /history
    history = models.History.from_dict(json.loads(HISTORY))
    assert isinstance(history, models.History)
    assert isinstance(history.records, tuple)
    assert len(history.records) == 1
    download = history.records[0]
    assert isinstance(download, models.Download)

    assert download.episodeId == 0
    assert download.movieId == 13
    assert download.seriesId == 0
    assert download.sourceTitle == "Minions 2015 720p BluRay DD-EX x264-xxxxxxxxxx"
    assert isinstance(download.quality, models.QualityRevision)  # tested elsewhere
    assert download.qualityCutoffNotMet is False
    assert download.date == datetime(2017, 1, 24, 14, 57, 5, 134486, tzinfo=UTC)
    assert download.downloadId == "xxxxxxxxxx"
    assert download.eventType == "grabbed"
    assert isinstance(download.data, DownloadData)  # tested elsewhere
    assert isinstance(download.movie, models.Movie)  # tested elsewhere
    assert download.id == 9


def test_history() -> None:
    """Test the History model."""
    #  instance from /history
    history = models.History.from_dict(json.loads(HISTORY))
    assert isinstance(history, models.History)
    assert history.page == 1
    assert history.pageSize == 10
    assert history.sortKey is enums.SortKey.DATE
    assert history.sortDirection is enums.SortDirection.DESCENDING
    assert history.totalRecords == 1
    assert isinstance(history.records, tuple)
    assert len(history.records) == 1
    assert isinstance(history.records[0], models.Download)


@pytest.fixture
def history_server():
    yield from mock_server(
        uri="/api/history", body=HISTORY,
    )


def test_get_history(history_server):
    """Test API call for RadarrClient.get_history()
    """

    client = replace(CLIENT, port=history_server.server_port)
    response = client.get_history()
    assert isinstance(response, models.History)
