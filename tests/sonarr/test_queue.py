"""Tests for Sonarr API /queue endpoint

https://github.com/Sonarr/Sonarr/wiki/Queue
"""
from datetime import datetime, timedelta
import json

import pytest

from downloadcarr.client import ArrClientError
import downloadcarr.sonarr.models as models
from downloadcarr.sonarr.client import SonarrClient
from downloadcarr.enums import Protocol, HttpMethod
from downloadcarr.utils import UTC

from . import QUEUE, mock_server


CLIENT = SonarrClient("localhost", "MYKEY")


def test_queue_item() -> None:
    """Test the QueueItem model."""
    item = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    # Tested in test_model_series.test_series()
    assert isinstance(item.series, models.Series)
    # Tested in test_model_episode.test_episode()
    assert isinstance(item.episode, models.Episode)
    # Tested in test_model_quality.test_qulity_revision()
    assert isinstance(item.quality, models.QualityRevision)
    assert item.size == 4472186820
    assert item.title == "The.Andy.Griffith.Show.S01E01.x264-GROUP"
    assert item.sizeleft == 0
    assert item.timeleft == timedelta(0)
    assert item.estimatedCompletionTime == datetime(
        2016, 2, 5, 22, 46, 52, 440104, tzinfo=UTC
    )
    assert item.status == "Downloading"
    assert item.trackedDownloadStatus == "Ok"
    assert item.statusMessages == ()
    assert item.downloadId == "SABnzbd_nzo_Mq2f_b"
    assert item.protocol == Protocol.USENET
    assert item.id == 1503378561


@pytest.fixture
def queue_server():
    yield from mock_server(
        uri="/api/queue", body=QUEUE,
    )


def test_get_queue(queue_server):
    """Test API call for SonarrClient.get_queue()

    GET http://$HOST:8989/api/queue?sort_by=timeleft&order=asc
    """

    CLIENT.port = queue_server.server_port
    response = CLIENT.get_queue()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.QueueItem)


@pytest.fixture
def queueitem_delete_server():
    yield from mock_server(
        uri="/api/queue/1", body="{}", method=HttpMethod.DELETE,
    )


def test_delete_queue_item(queueitem_delete_server):
    """Test API call for SonarrClient.delete_queue_item()

    DELETE http://$HOST:8989/api/queue/1242502863?blacklist=false
    """

    CLIENT.port = queueitem_delete_server.server_port
    response = CLIENT.delete_queue_item(1)
    assert response is None


@pytest.fixture
def queueitem_delete_bad_server():
    yield from mock_server(
        uri="/api/queue/1", body="[1, 2, 3]", method=HttpMethod.DELETE,
    )


def test_bad_delete_queue_item(queueitem_delete_bad_server):
    """SonarrClient.delete_queue_item() raises error if return value
    isn't empty JSON array.
    """

    CLIENT.port = queueitem_delete_bad_server.server_port
    with pytest.raises(ArrClientError):
         CLIENT.delete_queue_item(1)
