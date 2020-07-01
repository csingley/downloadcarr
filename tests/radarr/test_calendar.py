"""Tests for Radarr /calendar endpoint.

https://github.com/Radarr/Radarr/wiki/API:Calendar
"""
import pytest

from . import CALENDAR, mock_server
from downloadcarr.radarr import models
from downloadcarr.radarr import RadarrClient


CLIENT = RadarrClient("localhost", "MYKEY")


@pytest.fixture
def calendar_server():
    yield from mock_server(
        uri="/api/calendar",
        body=CALENDAR,
    )


def test_get_calendar(calendar_server):
    """Test API call for RadarrClient.get_calendar()
    """

    CLIENT.port = calendar_server.server_port
    response = CLIENT.get_calendar()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Movie)
