"""Tests for Radarr API /command endpoint.

https://github.com/Radarr/Radarr/wiki/API:Command
"""
import pytest

from downloadcarr.models import CommandStatus
from downloadcarr.radarr.client import RadarrClient
from downloadcarr.enums import HttpMethod, ImportMode

from . import COMMANDS, COMMAND, COMMANDPOST, mock_server


CLIENT = RadarrClient("localhost", "MYKEY")


#  https://github.com/Sonarr/Sonarr/wiki/Command
@pytest.fixture
def commands_server():
    yield from mock_server(uri="/api/command", body=COMMANDS)


def test_get_all_commands_status(commands_server):
    """Test API call for RadarrClient.get_all_commands_status()
    """
    CLIENT.port = commands_server.server_port
    response = CLIENT.get_all_commands_status()

    assert isinstance(response, tuple)
    assert len(response) == 2
    for item in response:
        assert isinstance(item, CommandStatus)


@pytest.fixture
def command_server():
    yield from mock_server(uri="/api/command/368630", body=COMMAND)


def test_get_command_status(command_server):
    """Test API call for RadarrClient.get_command_status()
    """
    CLIENT.port = command_server.server_port
    response = CLIENT.get_command_status(368630)
    assert isinstance(response, CommandStatus)


@pytest.fixture
def command_echo_server():
    yield from mock_server(
        uri="/api/command", body=COMMAND, method=HttpMethod.POST, echo=True,
    )


def test_refresh_movies(command_echo_server):
    """Test API call for RadarrClient.refresh_movies()
    """
    CLIENT.port = command_echo_server.server_port
    response = CLIENT.refresh_movies()
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {"name": "RefreshMovie"}


def test_refresh_movie(command_echo_server):
    """Test API call for RadarrClient.refresh_movie()
    """
    CLIENT.port = command_echo_server.server_port
    response = CLIENT.refresh_movie(1)
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {"name": "RefreshMovie", "movieId": 1}


def test_rescan_movies(command_echo_server):
    """Test API call for RadarrClient.rescan_movies()
    """
    CLIENT.port = command_echo_server.server_port
    response = CLIENT.rescan_movies()
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {"name": "RescanMovie"}


def test_rescan_movie(command_echo_server):
    """Test API call for RadarrClient.rescan_movie()
    """
    CLIENT.port = command_echo_server.server_port
    response = CLIENT.rescan_movie(1)
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {"name": "RescanMovie", "movieId": 1}


def test_search_movies(command_echo_server):
    """Test API call for RadarrClient.search_movies()
    """

    CLIENT.port = command_echo_server.server_port
    response = CLIENT.search_movies(1, 2, 3)
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {"name": "MoviesSearch", "movieIds": [1, 2, 3]}


def test_scan_downloaded_movies(command_echo_server):
    """Test API call for RadarrClient.scan_downloaded_movies()
    """

    CLIENT.port = command_echo_server.server_port
    response = CLIENT.scan_downloaded_movies(
        "/path/to/downloads/", downloadClientId="drone", importMode=ImportMode.MOVE,
    )
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {
        "name": "DownloadedMoviesScan",
        "path": "/path/to/downloads/",
        "downloadClientId": "drone",
        "importMode": "Move",
    }


def test_sync_rss(command_echo_server):
    """Test API call for RadarrClient.sync_rss()
    """

    CLIENT.port = command_echo_server.server_port
    response = CLIENT.sync_rss()
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {"name": "RssSync"}


def test_rename_files(command_echo_server):
    """Test API call for RadarrClient.rename_files()
    """

    CLIENT.port = command_echo_server.server_port
    response = CLIENT.rename_files(123, 345, 567)
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {"name": "RenameFiles", "files": [123, 345, 567]}


def test_rename_movies(command_echo_server):
    """Test API call for RadarrClient.rename_movies()
    """

    CLIENT.port = command_echo_server.server_port
    response = CLIENT.rename_movies(123, 345, 567)
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {"name": "RenameMovie", "movieIds": [123, 345, 567]}


def test_search_cutoff_unmet_movies(command_echo_server):
    """Test API call for RadarrClient.search_cutoff_unmet_movies()
    with default query params
    """

    CLIENT.port = command_echo_server.server_port
    response = CLIENT.search_cutoff_unmet_movies()
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {
        "name": "CutOffUnmetMoviesSearch",
        "filterKey": "monitored",
        "filterValue": "true",
    }


def test_sync_net_import(command_echo_server):
    """Test API call for RadarrClient.sync_net_import()
    """

    CLIENT.port = command_echo_server.server_port
    response = CLIENT.sync_net_import()
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {"name": "NetImportSync"}


def test_search_missing_movies(command_echo_server):
    """Test API call for RadarrClient.search_missing_movies()
    with default query params
    """

    CLIENT.port = command_echo_server.server_port
    response = CLIENT.search_missing_movies()
    assert isinstance(response, CommandStatus)

    echo = CLIENT._request("echo")
    assert echo == {
        "name": "missingMoviesSearch",
        "filterKey": "monitored",
        "filterValue": "true",
    }
