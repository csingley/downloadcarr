"""Tests for Sonarr API /release endpoint

https://github.com/Sonarr/Sonarr/wiki/Release
https://github.com/Sonarr/Sonarr/wiki/Release-Push
"""
from datetime import datetime
import json

import pytest

import downloadcarr.sonarr.models as models
from downloadcarr.sonarr.client import SonarrClient
from downloadcarr.utils import UTC
from downloadcarr.enums import HttpMethod, Protocol

from . import RELEASE, mock_server


CLIENT = SonarrClient("localhost", "MYKEY")


def test_release() -> None:
    """Test the Release model."""
    # instance returned by /release
    rel = models.Release.from_dict(json.loads(RELEASE)[0])
    assert rel.guid == "a5a4a6a7-f7c9-4ff0-b3c4-b8dea9ed965b"
    # tested in test_models_quality.test_quality_revision()
    assert isinstance(rel.quality, models.QualityRevision)
    assert rel.age == 0
    assert rel.size == 0
    assert rel.indexerId == 5
    assert rel.indexer == "Wombles"
    assert rel.releaseGroup == "YesTV"
    assert rel.title == "The.Devils.Ride.S03E01.720p.HDTV.x264-YesTV"
    assert rel.fullSeason is False
    assert rel.sceneSource is False
    assert rel.seasonNumber == 3
    assert rel.language == "english"
    assert rel.seriesTitle == "devilsride"
    assert rel.episodeNumbers == (1, )
    assert rel.approved is False
    assert rel.tvRageId == 0
    assert rel.rejections == ("Unknown Series", )
    assert rel.publishDate == datetime(2014, 2, 10, tzinfo=UTC)
    assert rel.downloadUrl == (
        "http://www.newshost.co.za/nzb/5a6/"
        "The.Devils.Ride.S03E01.720p.HDTV.x264-YesTV.nzb"
    )
    assert rel.downloadAllowed is True


@pytest.fixture
def release_server():
    yield from mock_server(
        uri="/api/release?episodeId=1",
        body=RELEASE,
        match_query=True,
    )


def test_get_release(release_server):
    """Test API call for SonarrClient.get_release()

    GET http://$HOST:8989/api/release?episodeId=35&sort_by=releaseWeight&order=asc
    """

    CLIENT.port = release_server.server_port
    response = CLIENT.get_release(1)
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Release)


@pytest.fixture
def add_release_echo_server():
    yield from mock_server(
        uri="/api/release",
        body=RELEASE,
        method=HttpMethod.POST,
        echo=True,
    )


def test_add_release(add_release_echo_server):
    """Test API call for SonarrClient.add_release()

    NEEDS EXAMPLE
    """

    CLIENT.port = add_release_echo_server.server_port
    response = CLIENT.add_release(
        guid="a5a4a6a7-f7c9-4ff0-b3c4-b8dea9ed965b",
        indexerId=5,
    )
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Release)

    echo = CLIENT._request("echo")
    assert echo == {'guid': 'a5a4a6a7-f7c9-4ff0-b3c4-b8dea9ed965b', 'indexerId': 5}


#  https://github.com/Sonarr/Sonarr/wiki/Release-Push
@pytest.fixture
def push_release_echo_server():
    yield from mock_server(
        uri="/api/release/push",
        body=RELEASE,
        method=HttpMethod.POST,
        echo=True,
    )


def test_push_release(push_release_echo_server):
    """Test API call for SonarrClient.push_release()

    NEEDS EXAMPLE
    """

    CLIENT.port = push_release_echo_server.server_port
    response = CLIENT.push_release(
        title="The.Devils.Ride.S03E01.720p.HDTV.x264-YesTV",
        downloadUrl="http://www.newshost.co.za/nzb/5a6/The.Devils.Ride.S03E01.720p.HDTV.x264-YesTV.nzb",
        protocol=Protocol.USENET,
        publishDate=datetime(2014, 2, 10, tzinfo=UTC)
    )
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Release)

    echo = CLIENT._request("echo")
    assert echo == {
        'title': 'The.Devils.Ride.S03E01.720p.HDTV.x264-YesTV',
        'downloadUrl': 'http://www.newshost.co.za/nzb/5a6/The.Devils.Ride.S03E01.720p.HDTV.x264-YesTV.nzb',
        'protocol': 'usenet',
        'publishDate': '2014-02-10T00:00:00Z',
    }
