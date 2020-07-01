"""
"""
import http.server
import socket
import threading
from urllib.parse import urlparse, parse_qs
from pathlib import Path

from downloadcarr.enums import HttpMethod


def load(filename):
    """Load test data from file."""

    path = Path(__file__).parent / "data" / filename
    with open(path) as f:
        return f.read()


COMMANDS = load("commands.json")
COMMAND = load("command.json")
DISKSPACE = load("diskspace.json")
SYSTEMSTATUS = load("system-status.json")


#  https://realpython.com/testing-third-party-apis-with-mock-servers/
def get_free_port():
    """Find an open TCP port available on localhost.
    """
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    address, port = s.getsockname()
    s.close()
    return port


def make_mock_server(
    uri: str,
    body: str,
    host: str = "localhost",
    port: int = get_free_port(),
    method: HttpMethod = HttpMethod.GET,
    match_query: bool = False,
    echo: bool = False,
):
    """Create an HTTP server that listens on (ONLY!) the input
    ``host``/``port``/``uri``/``method``, and responds with the input ``body``.

    ``match_query``, if True, requires that the URI query params must match;
    otherwise they are ignored.

    If ``echo`` is True, after an HTTP request has been made, the server will
    also echo data sent in the request body, accessible via HTTP GET at the
    /api/echo endpoint.
    """

    def do_http_response(self):
        """Unified handler for all HTTP request methods.

        Used for do_{GET, POST, PUT, DELETE} methods of
        http.server.BaseHTTPRequestHandler subclasses.

        Relies on ``self`` possessing:
            * attributes holding ``make_mock_server()`` args
              - ``uri``
              - ``body``
              - ``method``
              - ``match_query``
              - ``echo``
        """
        # Make sure HTTP method matches spec configuration
        if self.command != self.method.name:
            self.send_error(405)

        # Parse URI for incoming request vs fixture
        parsed_uri = urlparse(self.path)
        parsed_uri_cfg = urlparse(self.uri)

        # Make sure URI path matches fixture config
        if parsed_uri.path != parsed_uri_cfg.path:
            self.send_error(401)

        # Make sure query matches spec configuration
        elif self.match_query and (
            parse_qs(parsed_uri.query) != parse_qs(parsed_uri_cfg.query)
        ):
            self.send_error(417)

        else:
            if self.echo:
                # Read HTTP request body; stash in class attribute for echo
                length = int(self.headers.get('content-length'))
                body = self.rfile.read(length)
                if body:
                    assert self.__class__.echo_body == b"{}"
                    self.__class__.echo_body = body

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(self.body.encode())

    def do_GET(self):
        if self.echo and self.path == "/api/echo":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(self.echo_body)
            self.__class__.echo_body = b"{}"  # Reset
        else:
            self._do()

    MockRequestHandler = type(
        "MockRequestHandler",
        (http.server.BaseHTTPRequestHandler, ),
        {
            # Make function args available in class namespace.
            "uri": uri,
            "body": body,
            "method": method,
            "match_query": match_query,
            "echo": echo,

            # Alternate echo handler for HTTP GET
            "do_GET": do_GET,
            # Unified handler for all other HTTP request methods
            "_do": do_http_response,
            "do_POST": lambda self: self._do(),
            "do_PUT": lambda self: self._do(),
            "do_DELETE": lambda self: self._do(),

            # Class attribute allowing different RequestHandler instances
            # (instantiated from different HTTP requests) to pass data
            "echo_body": b"{}",
        }
    )

    server = http.server.HTTPServer((host, port), MockRequestHandler)
    return server


def mock_server(
    uri: str,
    body: str,
    host: str = "localhost",
    port: int = get_free_port(),
    method: HttpMethod = HttpMethod.GET,
    match_query: bool = False,
    echo: bool = False,
):
    server = make_mock_server(
        host=host,
        port=port,
        uri=uri,
        body=body,
        method=method,
        match_query=match_query,
        echo=echo,
    )

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True  # stop Python from biting ctrl-C
    thread.start()
    yield server
    server.shutdown()
    server.server_close()


def make_mock_error_server(
    uri: str,
    err_code: int,
    err_msg: str = None,
    err_explain: str = None,
    host: str = "localhost",
    port: int = get_free_port(),
    method: HttpMethod = HttpMethod.GET,
):
    """
    """

    def do_http_response(self):
        """
        """
        send_error = False

        if self.command == self.method.name:
            # Parse URI for incoming request vs fixture
            parsed_uri = urlparse(self.path)
            parsed_uri_cfg = urlparse(self.uri)

            # Make sure URI path matches fixture config
            if parsed_uri.path == parsed_uri_cfg.path:
                send_error = True

        if send_error:
            self.send_error(self.err_code, self.err_msg, self.err_explain)
        else:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b"{}")

    MockRequestHandler = type(
        "MockRequestHandler",
        (http.server.BaseHTTPRequestHandler, ),
        {
            # Make function args available in class namespace.
            "uri": uri,
            "method": method,
            "err_code": err_code,
            "err_msg": err_msg,
            "err_explain": err_explain,

            # Unified handler for all HTTP request methods
            "_do": do_http_response,
            "do_GET": lambda self: self._do(),
            "do_POST": lambda self: self._do(),
            "do_PUT": lambda self: self._do(),
            "do_DELETE": lambda self: self._do(),
        }
    )

    server = http.server.HTTPServer((host, port), MockRequestHandler)
    return server


def mock_error_server(
    uri: str,
    err_code: int,
    err_msg: str,
    err_explain,
    host: str = "localhost",
    port: int = get_free_port(),
    method: HttpMethod = HttpMethod.GET,
):
    server = make_mock_error_server(
        host=host,
        port=port,
        uri=uri,
        method=method,
        err_code=err_code,
        err_msg=err_msg,
        err_explain=err_explain,
    )

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True  # stop Python from biting ctrl-C
    thread.start()
    yield server
    server.shutdown()
    server.server_close()
