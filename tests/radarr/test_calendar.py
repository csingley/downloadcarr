"""Tests for Radarr /calendar endpoint.

https://github.com/Radarr/Radarr/wiki/API:Calendar
"""
from datetime import date
from dataclasses import replace

import pytest

from downloadcarr.radarr import models

from . import CALENDAR, mock_server, CLIENT


@pytest.fixture
def calendar_server():
    yield from mock_server(uri="/api/calendar", body=CALENDAR, match_query=True)


def test_get_calendar(calendar_server):
    """Test API call for RadarrClient.get_calendar() with default params
    """

    client = replace(CLIENT, port=calendar_server.server_port)
    response = client.get_calendar()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Movie)


@pytest.fixture
def calendar_server_params():
    yield from mock_server(
        uri="/api/calendar?start=2020-01-01&end=2020-01-31",
        body=CALENDAR,
        match_query=True,
    )


def test_get_calendar_params(calendar_server_params):
    """Test API call for RadarrClient.get_calendar() with start/end args
    """

    client = replace(CLIENT, port=calendar_server_params.server_port)
    response = client.get_calendar(start=date(2020, 1, 1), end=date(2020, 1, 31))
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Movie)
