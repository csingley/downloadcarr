"""Tests for Sonarr API /command endpoint.

https://github.com/Sonarr/Sonarr/wiki/Command
"""
from dataclasses import replace

import pytest

from downloadcarr.models import CommandStatus
from downloadcarr.sonarr.client import SonarrClient
from downloadcarr.enums import HttpMethod, ImportMode

from . import COMMANDS, COMMAND, mock_server, CLIENT


#  https://github.com/Sonarr/Sonarr/wiki/Command
@pytest.fixture
def commands_server():
    yield from mock_server(uri="/api/command", body=COMMANDS)


def test_get_all_commands_status(commands_server):
    """Test API call for SonarrClient.get_all_commands_status()
    """
    #  NEEDS EXAMPLE

    client = replace(CLIENT, port=commands_server.server_port)
    response = client.get_all_commands_status()

    assert isinstance(response, tuple)
    assert len(response) == 2
    for item in response:
        assert isinstance(item, CommandStatus)


@pytest.fixture
def command_server():
    yield from mock_server(uri="/api/command/368630", body=COMMAND)


def test_get_command_status(command_server):
    """Test API call for SonarrClient.get_command_status()
    """
    #  NEEDS EXAMPLE

    client = replace(CLIENT, port=command_server.server_port)
    response = client.get_command_status(368630)
    assert isinstance(response, CommandStatus)


@pytest.fixture
def command_echo_server():
    yield from mock_server(
        uri="/api/command", body=COMMAND, method=HttpMethod.POST, echo=True,
    )


def test_refresh_all_series(command_echo_server):
    """Test API call for SonarrClient.refresh_all_series()
    """
    #  POST http://$HOST:8989/api/command {"name":"refreshseries"}

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.refresh_all_series()
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "RefreshSeries"}


def test_refresh_series(command_echo_server):
    """Test API call for SonarrClient.refresh_series()
    """
    #  POST http://$HOST:8989/api/command {"name":"refreshSeries","seriesId":307}

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.refresh_series(1)
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "RefreshSeries", "seriesId": 1}


def test_rescan_all_series(command_echo_server):
    """Test API call for SonarrClient.rescan_all_series()
    """
    #  NEEDS EXAMPLE

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.rescan_all_series()
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "RescanSeries"}


def test_rescan_series(command_echo_server):
    """Test API call for SonarrClient.rescan_series()
    """
    #  NEEDS EXAMPLE

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.rescan_series(1)
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "RescanSeries", "seriesId": 1}


def test_search_episodes(command_echo_server):
    """Test API call for SonarrClient.search_episodes()
    """
    #  POST http://$HOST:8989/api/command {"name":"episodeSearch","episodeIds":[19223]}

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.search_episodes(1, 2, 3)
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "EpisodeSearch", "episodeIds": [1, 2, 3]}


def test_search_season(command_echo_server):
    """Test API call for SonarrClient.search_season()
    """
    #  POST http://$HOST:8989/api/command {"name":"seasonSearch","seriesId":3,"seasonNumber":5}

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.search_season(seriesId=1, seasonNumber=2)
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "SeasonSearch", "seriesId": 1, "seasonNumber": 2}


def test_search_series(command_echo_server):
    """Test API call for SonarrClient.search_series()
    """
    #  POST http://$HOST:8989/api/command {"name":"seriesSearch","seriesId":3}

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.search_series(1)
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "SeriesSearch", "seriesId": 1}


def test_scan_downloaded_episodes(command_echo_server):
    """Test API call for SonarrClient.scan_downloaded_episodes()
    """
    #  POST http://$HOST:8989/api/command {"name":"DownloadedEpisodesScan"}

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.scan_downloaded_episodes(
        "/path/to/downloads/", downloadClientId="drone", importMode=ImportMode.MOVE,
    )
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {
        "name": "DownloadedEpisodesScan",
        "path": "/path/to/downloads/",
        "downloadClientId": "drone",
        "importMode": "Move",
    }


def test_sync_rss(command_echo_server):
    """Test API call for SonarrClient.sync_rss()
    """
    #  POST http://$HOST:8989/api/command {"name":"RssSync"}

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.sync_rss()
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "RssSync"}


def test_rename_files(command_echo_server):
    """Test API call for SonarrClient.rename_files()
    """
    #  POST http://$HOST:8989/api/command {"name":"renameFiles","seriesId":205,"seasonNumber":-1,"files":[102036,101353,100458,50137,49744,49108,48545,47995,47549,47327,46445]}

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.rename_files(123, 345, 567)
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "RenameFiles", "files": [123, 345, 567]}


def test_rename_series(command_echo_server):
    """Test API call for SonarrClient.rename_series()
    """
    #  GET http://$HOST:8989/api/rename?seriesId=205

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.rename_series(123, 345, 567)
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "RenameSeries", "seriesIds": [123, 345, 567]}


def test_backup(command_echo_server):
    """Test API call for SonarrClient.backup()
    """
    #  POST http://$HOST:8989/api/command {"name":"backup","type":"manual"}
    #  POST http://$HOST:8989/api/command {"name":"Backup"}

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.backup()
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "Backup"}


def test_search_missing_episodes(command_echo_server):
    """Test API call for SonarrClient.search_missing_episodes()
    """
    #  POST http://$HOST:8989/api/command {"name":"missingEpisodeSearch"}

    client = replace(CLIENT, port=command_echo_server.server_port)
    response = client.search_missing_episodes()
    assert isinstance(response, CommandStatus)

    echo = client._request("echo")
    assert echo == {"name": "missingEpisodeSearch"}
