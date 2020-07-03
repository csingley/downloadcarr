"""Python client for Sonarr-based servers (Radarr, Lidarr, etc.).
"""
import pathlib
import urllib.request
import urllib.error
import urllib.parse
import ssl
import json
import socket
from typing import Any, Mapping, Optional
from dataclasses import dataclass

from .__version__ import __version__, __title__
from .enums import HttpMethod
from .models import CommandStatus


class ArrClientError(Exception):
    """Base class for errors in this module."""

    pass


class ArrConnectionError(ArrClientError):
    pass


class ArrHttpError(ArrClientError):
    pass


@dataclass(frozen=True)
class Client:
    """Main class for handling connections with *arr API."""

    #  port_default: int = 0  # Define in subclass

    host: str
    api_key: str
    port: int = 0
    base_path: str = "api"
    request_timeout: int = 8
    tls: bool = False
    verify_ssl: bool = True
    user_agent: str = ""

    #  def __init__(
    #      self,
    #      host: str,
    #      api_key: str,
    #      port: int = 0,
    #      base_path: str = "api",
    #      request_timeout: int = 8,
    #      tls: bool = False,
    #      verify_ssl: bool = True,
    #      user_agent: str = "",
    #  ) -> None:
    #      self.api_key = api_key
    #      self.base_path = base_path
    #      self.host = host
    #      self.port = port if port != 0 else self.port_default
    #      self.request_timeout = request_timeout
    #      self.tls = tls
    #      self.verify_ssl = verify_ssl
    #      self.user_agent = user_agent

    #      if user_agent == "":
    #          clsnm = self.__class__.__name__
    #          self.user_agent = f"{__title__}.{clsnm}/{__version__} (Python)"

    #  def __repr__(self):
    #      attrs = (
    #          f"{attr}={repr(getattr(self, attr))}"
    #          for attr in [
    #              "host",
    #              "port",
    #              "api_key",
    #              "base_path",
    #              "request_timeout",
    #              "tls",
    #              "verify_ssl",
    #              "user_agent",
    #          ]
    #      )
    #      rep = f"{self.__class__.__name__}(" f'{", ".join(attrs)}' ")"
    #      return rep

    def _request(
        self,
        uri: str = "",
        method: HttpMethod = HttpMethod.GET,
        data: Any = None,
        query: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """Handle a request to API."""
        scheme = "https" if self.tls else "http"

        # Reuse pathlib logic to construct paths without separator headaches
        full_uri = str(pathlib.PurePosixPath("/") / self.base_path / uri)

        url = f"{scheme}://{self.host}:{self.port}{full_uri}"
        if query:
            encoded_query = urllib.parse.urlencode(query)
            url += f"?{encoded_query}"

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
            "X-Api-Key": self.api_key,
        }

        request = urllib.request.Request(
            url,
            data=json.dumps(data).encode() if data else None,
            headers=headers,
            method=method.name,
        )

        if self.verify_ssl is False:
            ssl_context = ssl._create_unverified_context()
        else:
            ssl_context = ssl.create_default_context()

        try:
            with urllib.request.urlopen(
                request, timeout=self.request_timeout, context=ssl_context
            ) as f:
                response_info = f.info()
                content_type = response_info["Content-Type"]
                assert "application/json" in content_type
                response = json.load(f)
        except urllib.error.HTTPError as err:
            # HTTPError subclasses URLError; catch it first
            errcode = str(err.code)
            # Redirects should be handled by urllib
            assert errcode.startswith(("4", "5"))
            raise ArrHttpError(errcode, err.reason, err.url)
        except urllib.error.URLError as err:
            reason = err.reason
            assert isinstance(reason, ConnectionError)
            raise ArrConnectionError(url, err.reason.args[1])  # type: ignore
        except socket.timeout:
            raise ArrConnectionError(url, "Timeout")

        return response

    def _post_command(self, name: str, **kwargs) -> CommandStatus:
        """POST a request to /{base_path}/command.

        All POST/PUT requests require all parameters to be JSON encoded in the
        body, unless otherwise noted.
        """
        data = {"name": name}
        data.update(kwargs)
        results = self._request("command", method=HttpMethod.POST, data=data)
        return CommandStatus.from_dict(results)
