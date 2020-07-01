"""Tests for Radarr API /queue endpoint

https://github.com/Radarr/Radarr/wiki/API:Queue
"""
import json
from datetime import datetime, timedelta

import pytest

import downloadcarr.radarr.models as models
from downloadcarr.radarr.client import RadarrClient
from downloadcarr.utils import UTC
from downloadcarr.enums import Protocol, HttpMethod

from . import QUEUE, mock_server


CLIENT = RadarrClient("localhost", "MYKEY")


def test_status_message() -> None:
    """Test the StatusMessage model."""
    queue = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    assert isinstance(queue, models.QueueItem)
    assert isinstance(queue.statusMessages, tuple)
    assert len(queue.statusMessages) == 1
    msg = queue.statusMessages[0]
    assert isinstance(msg, models.StatusMessage)
    assert msg.title == "Mowgli (2018) Web-Dl 1080p x264 AC3-NoTag.mkv"
    assert isinstance(msg.messages, tuple)
    assert len(msg.messages) == 1
    assert msg.messages[0] == "No files found are eligible for import in /home/usr/download/movies/Mowgli (2018) Web-Dl 1080p x264 AC3-NoTag.mkv"


def test_queue_item() -> None:
    """Test the QueueItem model."""
    #  instance from /queue
    queue = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    assert isinstance(queue, models.QueueItem)
    assert isinstance(queue.movie, models.Movie)  # tested in test_movie
    assert isinstance(queue.quality, models.QualityRevision)  # tested in test_quality
    assert queue.size == 2948099499.0
    assert queue.title == "Mowgli (2018) Web-Dl 1080p x264 AC3-NoTag.mkv"
    assert queue.sizeleft == 0.0
    assert queue.timeleft == timedelta(0)
    assert queue.estimatedCompletionTime == datetime(2019, 8, 16, 9, 10, 12, 721926, tzinfo=UTC)
    assert queue.status == "Completed"
    assert queue.trackedDownloadStatus == "Warning"
    assert isinstance(queue.statusMessages, tuple)
    assert len(queue.statusMessages) == 1
    assert isinstance(queue.statusMessages[0], models.StatusMessage)
    assert queue.downloadId == "123456789xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    assert queue.protocol is Protocol.TORRENT
    assert queue.id == 473989688


@pytest.fixture
def get_queue_server():
    yield from mock_server(
        uri="/api/queue",
        body=QUEUE,
    )


def test_get_queue(get_queue_server):
    """Test API call for RadarrClient.get_queue()
    """

    CLIENT.port = get_queue_server.server_port
    response = CLIENT.get_queue()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.QueueItem)


@pytest.fixture
def queueitem_delete_server():
    yield from mock_server(
        uri="/api/queue/1",
        body="{}",
        method=HttpMethod.DELETE,
    )


def test_delete_queue_item(queueitem_delete_server):
    """Test API call for RadarrClient.delete_queue_item()
    """

    CLIENT.port = queueitem_delete_server.server_port
    response = CLIENT.delete_queue_item(1)
    assert response is None
