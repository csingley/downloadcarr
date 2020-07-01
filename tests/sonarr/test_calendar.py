"""Tests for Sonarr /calendar endpoint.

https://github.com/Sonarr/Sonarr/wiki/Calendar
"""
import pytest

from . import CALENDAR, mock_server
from downloadcarr.sonarr import models
from downloadcarr.sonarr import SonarrClient


CLIENT = SonarrClient("localhost", "MYKEY")


@pytest.fixture
def calendar_server():
    yield from mock_server(
        uri="/api/calendar",
        body=CALENDAR,
    )


def test_get_calendar(calendar_server):
    """Test API call for SonarrClient.get_calendar()
    """

    CLIENT.port = calendar_server.server_port
    response = CLIENT.get_calendar()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Episode)
