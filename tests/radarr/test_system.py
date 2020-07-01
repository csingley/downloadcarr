"""Tests for Radarr API endpoints:
    /system
    /diskspace

https://github.com/Radarr/Radarr/wiki/API:Diskspace
https://github.com/Radarr/Radarr/wiki/API:System-Status

DiskSpace, SystemStatus models tested in downloadcarr.tests.test_models-common
"""
from datetime import datetime
import json

import pytest

from downloadcarr.models import DiskSpace, SystemStatus
import downloadcarr.radarr.models as models
from downloadcarr.radarr.client import RadarrClient
from downloadcarr.utils import UTC

from . import (
    DISKSPACE,
    SYSTEMSTATUS,
    mock_server,
)


CLIENT = RadarrClient("localhost", "MYKEY")


@pytest.fixture
def diskspace_server():
    yield from mock_server(
        uri="/api/diskspace",
        body=DISKSPACE,
    )


def test_get_diskspace(diskspace_server):
    """Test API call for RadarrClient.get_diskspace()
    """

    CLIENT.port = diskspace_server.server_port
    response = CLIENT.get_diskspace()
    assert isinstance(response, tuple)
    assert len(response) == 2
    for disk in response:
        assert isinstance(disk, DiskSpace)


@pytest.fixture
def system_status_server():
    yield from mock_server(
        uri="/api/system/status",
        body=SYSTEMSTATUS,
    )


def test_get_system_status(system_status_server):
    """Test API call for RadarrClient.get_system_status()
    """

    CLIENT.port = system_status_server.server_port
    response = CLIENT.get_system_status()
    assert isinstance(response, SystemStatus)
