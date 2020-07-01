"""Tests for Sonarr API /tag endpoint

https://github.com/Sonarr/Sonarr/wiki/Tag
"""
import json

import pytest

import downloadcarr.sonarr.models as models
from downloadcarr.sonarr.client import SonarrClient
from downloadcarr.enums import HttpMethod

from . import TAGS, TAG, mock_server


CLIENT = SonarrClient("localhost", "MYKEY")


def test_tag() -> None:
    """Test the Tag model."""
    # instance returned by /series
    pass  # FIXME - need data

    # instance returned by /tag
    tags = [models.Tag.from_dict(tag) for tag in json.loads(TAGS)]
    assert len(tags) == 2
    tag0, tag1 = tags

    assert tag0.label == "amzn"
    assert tag0.id == 1

    assert tag1.label == "netflix"
    assert tag1.id == 2


@pytest.fixture
def tags_server():
    yield from mock_server(
        uri="/api/tag", body=TAGS,
    )


def test_get_tags(tags_server):
    """Test API call for SonarrClient.get_tags()

    GET http://$HOST:8989/api/tag
    """

    CLIENT.port = tags_server.server_port
    response = CLIENT.get_tags()
    assert isinstance(response, tuple)
    assert len(response) == 2
    for tag in response:
        assert isinstance(tag, models.Tag)


@pytest.fixture
def tag_server():
    yield from mock_server(
        uri="/api/tag/1", body=TAG,
    )


def test_get_tag(tag_server):
    """Test API call for SonarrClient.get_tag()

    NEEDS EXAMPLE
    """

    CLIENT.port = tag_server.server_port
    response = CLIENT.get_tag(1)
    assert isinstance(response, models.Tag)


@pytest.fixture
def add_tag_echo_server():
    yield from mock_server(
        uri="/api/tag", body=TAG, method=HttpMethod.POST, echo=True,
    )


def test_add_tag(add_tag_echo_server):
    """Test API call for SonarrClient.add_tag()

    POST http://$HOST:8989/api/tag {"label":"test"}
    """

    CLIENT.port = add_tag_echo_server.server_port
    response = CLIENT.add_tag("amzn")
    assert isinstance(response, models.Tag)

    echo = CLIENT._request("echo")
    assert echo == {"label": "amzn"}


@pytest.fixture
def update_tag_echo_server():
    yield from mock_server(
        uri="/api/tag", body=TAG, method=HttpMethod.PUT, echo=True,
    )


def test_update_tag(update_tag_echo_server):
    """Test API call for SonarrClient.update_tag()

    NEEDS EXAMPLE
    """

    CLIENT.port = update_tag_echo_server.server_port
    response = CLIENT.update_tag(1, "amzn")
    assert isinstance(response, models.Tag)

    echo = CLIENT._request("echo")
    assert echo == {"id": 1, "label": "amzn"}


@pytest.fixture
def delete_tag_server():
    yield from mock_server(
        uri="/api/tag/1", body="{}", method=HttpMethod.DELETE,
    )


def test_delete_tag(delete_tag_server):
    """Test API call for SonarrClient.delete_tag()

    NEEDS EXAMPLE
    """

    CLIENT.port = delete_tag_server.server_port
    response = CLIENT.delete_tag(1)
    assert response is None
