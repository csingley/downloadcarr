"""Tests for Sonarr /calendar endpoint.

https://github.com/Sonarr/Sonarr/wiki/Calendar
"""
from dataclasses import replace

import pytest

from . import CALENDAR, mock_server, CLIENT
from downloadcarr.sonarr import models


@pytest.fixture
def calendar_server():
    yield from mock_server(
        uri="/api/calendar", body=CALENDAR,
    )


def test_get_calendar(calendar_server):
    """Test API call for SonarrClient.get_calendar()
    """

    client = replace(CLIENT, port=calendar_server.server_port)
    response = client.get_calendar()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Episode)
