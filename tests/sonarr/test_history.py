"""Tests for Sonarr API /history endpoint

https://github.com/Sonarr/Sonarr/wiki/History
"""
from datetime import datetime
import json

import pytest

import downloadcarr.sonarr.models as models
from downloadcarr.sonarr.client import SonarrClient
from downloadcarr.enums import SortDirection, SortKey
from downloadcarr.utils import UTC

from . import HISTORY, mock_server


CLIENT = SonarrClient("localhost", "MYKEY")


def test_download_data() -> None:
    """Test the DownloadData model."""
    hist = models.History.from_dict(json.loads(HISTORY))
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    dldata0 = dl0.data
    assert dldata0.droppedPath == "d:\\tvshows\\Blindspot S01E11 1080p WEB-DL DD5 1 H 264-NTB\\160223_06.mkv"
    assert dldata0.importedPath == "F:\\TV_Shows\\Blindspot\\Season 01\\Blindspot.S01E11.Cease.Forcing.Enemy.WEBDL-1080p.mkv"
    assert dldata0.downloadClient == "Sabnzbd"
    assert dldata0.reason is None
    assert dldata0.indexer is None
    assert dldata0.nzbInfoUrl is None
    assert dldata0.releaseGroup is None
    assert dldata0.age is None
    assert dldata0.ageHours is None
    assert dldata0.ageMinutes is None
    assert dldata0.publishedDate is None
    assert dldata0.size is None
    assert dldata0.downloadUrl is None
    assert dldata0.guid is None
    assert dldata0.tvdbId is None
    assert dldata0.tvRageId is None
    assert dldata0.protocol is None

    dldata1 = dl1.data
    assert dldata1.droppedPath is None
    assert dldata1.importedPath is None
    assert dldata1.downloadClient is None
    assert dldata1.reason == "Upgrade"
    assert dldata1.indexer is None
    assert dldata1.nzbInfoUrl is None
    assert dldata1.releaseGroup is None
    assert dldata1.age is None
    assert dldata1.ageHours is None
    assert dldata1.ageMinutes is None
    assert dldata1.publishedDate is None
    assert dldata1.size is None
    assert dldata1.downloadUrl is None
    assert dldata1.guid is None
    assert dldata1.tvdbId is None
    assert dldata1.tvRageId is None
    assert dldata1.protocol is None


def test_download() -> None:
    """Test the Download model."""
    hist = models.History.from_dict(json.loads(HISTORY))
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    assert dl0.episodeId == 5276
    assert dl0.seriesId == 60
    assert dl0.sourceTitle == "Blindspot S01E11 1080p WEB-DL DD5 1 H 264-NTB"
    # Tested in test_models_quality.test_quality_revision()
    assert isinstance(dl0.quality, models.QualityRevision)
    assert dl0.qualityCutoffNotMet is False
    # "date": "2016-09-10T20:26:32.2634211Z"
    # Round to microseconds
    assert dl0.date == datetime(2016, 9, 10, 20, 26, 32, 263421, tzinfo=UTC)
    assert dl0.downloadId == "SABnzbd_nzo_tlsnni"
    assert dl0.eventType == "downloadFolderImported"
    assert isinstance(dl0.data, models.DownloadData)  # tested in test_download_data()
    assert isinstance(dl0.episode, models.Episode)  # tested in test_models_episode.test_episode()
    assert isinstance(dl0.series, models.Series)  # tested in test_models_series.test_series()
    assert dl0.id == 11915

    assert dl1.episodeId == 5276
    assert dl1.seriesId == 60
    assert dl1.sourceTitle == "F:\\TV_Shows\\Blindspot\\Season 01\\Blindspot.S01E11.Cease.Forcing.Enemy.HDTV-1080p.Proper.mkv"
    # Tested in test_models_quality.test_quality_revision()
    assert isinstance(dl1.quality, models.QualityRevision)
    assert dl1.qualityCutoffNotMet is True
    # "date": "2016-09-10T20:26:27.9055911Z"
    # Round to microseconds
    assert dl1.date == datetime(2016, 9, 10, 20, 26, 27, 905591, tzinfo=UTC)
    assert dl1.eventType == "episodeFileDeleted"
    assert isinstance(dl1.data, models.DownloadData)  # tested in test_download_data()
    assert isinstance(dl1.episode, models.Episode)  # tested in test_models_episode.test_episode()
    assert isinstance(dl1.series, models.Series)  # tested in test_models_series.test_series()
    assert dl1.id == 11914


def test_history() -> None:
    """Test the History model."""
    hist = models.History.from_dict(json.loads(HISTORY))
    assert hist.page == 1
    assert hist.pageSize == 10
    assert hist.sortKey == SortKey.DATE
    assert hist.sortDirection == SortDirection.DESCENDING
    assert hist.totalRecords == 8094
    assert len(hist.records) == 2
    dl0, dl1 = hist.records
    assert isinstance(dl0, models.Download)  # Download tested in test_download()
    assert isinstance(dl1, models.Download)  # Download tested in test_download()


@pytest.fixture
def history_server():
    yield from mock_server(
        uri="/api/history?sortKey=series.title&page=1&pageSize=10&sortDir=asc",
        body=HISTORY,
        match_query=True,
    )


def test_get_history(history_server):
    """Test API call for SonarrClient.get_history() with default query args

    GET http://$HOST:8989/api/history?page=1&pageSize=15&sortKey=date&sortDir=desc
    GET http://$HOST:8989/api/history?page=1&pageSize=15&sortKey=date&sortDir=desc&episodeId=35
    """
    CLIENT.port = history_server.server_port
    response = CLIENT.get_history(sortKey=SortKey.SERIESTITLE)
    assert isinstance(response, models.History)

    assert response.pageSize == 10
    assert response.totalRecords == 8094
    assert response.sortKey is SortKey.DATE
    assert response.sortDirection is SortDirection.DESCENDING

    assert isinstance(response.records, tuple)
    assert len(response.records) == 2

    for record in response.records:
        assert isinstance(record, models.Download)
