"""Tests for downloadcarr.client (base class).
"""
import http.server
from time import sleep
import threading

import pytest

from downloadcarr.client import (
    Client,
    ArrHttpError,
    ArrConnectionError,
    ArrClientError,
)

from . import mock_server, mock_error_server, get_free_port


CLIENT = Client("localhost", "MYKEY")


@pytest.fixture
def alt_base_path_server():
    yield from mock_server(uri="/sonarr/api/system/status", body="123")


def test_alt_base_path(alt_base_path_server):
    """Test API running on different base path."""

    other_client = Client(
        "localhost",
        "MYKEY",
        base_path="/sonarr/api",
        port=alt_base_path_server.server_port,
    )

    response = other_client._request("system/status")
    assert response == 123


@pytest.fixture
def timeout_server():
    class Sleepy(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            sleep(2)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b"{}")

    server = http.server.HTTPServer(("localhost", get_free_port()), Sleepy)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield server
    server.shutdown()
    server.server_close()


def test_timeout(timeout_server):
    client = Client(
        "localhost", "MYKEY", port=timeout_server.server_port, request_timeout=2,
    )
    with pytest.raises(ArrConnectionError):
        client._request("system/status")


def test_nobody_home():
    client = Client("localhost", "MYKEY", port=get_free_port(), request_timeout=1,)
    with pytest.raises(ArrConnectionError):
        client._request("system/status")


@pytest.fixture
def err_403_server():
    yield from mock_error_server(
        uri="/api/system/status",
        err_code=403,
        err_msg="Forbidden",
        err_explain="Unauthorized",
    )


def test_http_error403(err_403_server):
    """Test HTTP 403 response handling."""

    CLIENT.port = err_403_server.server_port
    with pytest.raises(ArrHttpError):
        CLIENT._request("system/status")

    # Other URI doesn't raise error
    CLIENT._request("system/backup")


@pytest.fixture
def err_404_server():
    yield from mock_error_server(
        uri="/api/system/status",
        err_code=404,
        err_msg="Not Found",
        err_explain="What you're looking for ain't here",
    )


def test_http_error404(err_404_server):
    """Test HTTP 404 response handling."""

    CLIENT.port = err_404_server.server_port
    with pytest.raises(ArrClientError):
        CLIENT._request("system/status")

    # Other URI doesn't raise error
    CLIENT._request("system/backup")


@pytest.fixture
def err_500_server():
    yield from mock_error_server(
        uri="/api/system/status",
        err_code=500,
        err_msg="Internal Server Error",
        err_explain="Our gimmick is busted; back to the lab",
    )


def test_http_error500(err_500_server):
    """Test HTTP 500 response handling."""

    CLIENT.port = err_500_server.server_port
    with pytest.raises(ArrClientError):
        CLIENT._request("system/status")

    # Other URI doesn't raise error
    CLIENT._request("system/backup")
