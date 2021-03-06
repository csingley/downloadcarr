"""Tests for Sonarr API endpoints:
    /system
    /diskspace

https://github.com/Sonarr/Sonarr/wiki/Diskspace
https://github.com/Sonarr/Sonarr/wiki/Rootfolder
https://github.com/Sonarr/Sonarr/wiki/System-Status
https://github.com/Sonarr/Sonarr/wiki/System-Backup

DiskSpace, SystemStatus models tested in downloadcarr.tests.test_models-common
"""
from dataclasses import replace

import pytest

from downloadcarr.models import (
    DiskSpace,
    RootFolder,
    SystemStatus,
    SystemBackup,
)

from . import (
    DISKSPACE,
    ROOTFOLDER,
    SYSTEMBACKUP,
    SYSTEMSTATUS,
    mock_server,
    CLIENT,
)


@pytest.fixture
def diskspace_server():
    yield from mock_server(
        uri="/api/diskspace", body=DISKSPACE,
    )


def test_get_diskspace(diskspace_server):
    """Test API call for SonarrClient.get_diskspace()
    """
    #  GET http://$HOST:8989/api/diskspace

    client = replace(CLIENT, port=diskspace_server.server_port)
    response = client.get_diskspace()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], DiskSpace)


@pytest.fixture
def rootfolder_server():
    yield from mock_server(
        uri="/api/rootfolder", body=ROOTFOLDER,
    )


def test_get_rootfolders(rootfolder_server):
    """Test API call for SonarrClient.get_rootfolders()
    """
    #  GET http://$HOST:8989/api/rootfolder

    client = replace(CLIENT, port=rootfolder_server.server_port)
    response = client.get_rootfolders()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], RootFolder)


@pytest.fixture
def system_status_server():
    yield from mock_server(
        uri="/api/system/status", body=SYSTEMSTATUS,
    )


def test_get_system_status(system_status_server):
    """Test API call for SonarrClient.get_system_status()
    """
    #  GET http://$HOST:8989/api/system/status

    client = replace(CLIENT, port=system_status_server.server_port)
    response = client.get_system_status()
    assert isinstance(response, SystemStatus)


@pytest.fixture
def system_backup_server():
    yield from mock_server(
        uri="/api/system/backup", body=SYSTEMBACKUP,
    )


def test_get_system_backups(system_backup_server):
    """Test API call for SonarrClient.get_system_backups()
    """
    #  GET http://$HOST:8989/api/system/backup?sort_by=time&order=desc

    client = replace(CLIENT, port=system_backup_server.server_port)
    response = client.get_system_backups()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], SystemBackup)
