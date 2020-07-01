"""
"""
from datetime import datetime
import json

import pytest

from downloadcarr.models import (
    CommandStatus,
    CommandStatusBody,
    DiskSpace,
    SystemStatus,
)

#  from downloadcarr.sonarr.client import SonarrClient
from downloadcarr.client import Client
from downloadcarr.utils import UTC

from . import COMMANDS, COMMAND, DISKSPACE, SYSTEMSTATUS, mock_server


#  CLIENT = SonarrClient("localhost", "MYKEY")
CLIENT = Client("localhost", "MYKEY")


def test_command_status_body() -> None:
    """Test the CommandStatusBody model."""
    item0 = CommandStatus.from_dict(json.loads(COMMANDS)[0])
    body0 = item0.body
    assert isinstance(body0, CommandStatusBody)
    assert body0.isNewSeries is False
    assert body0.sendUpdatesToClient is True
    assert body0.updateScheduledTask is True
    assert body0.completionMessage == "Completed"
    assert body0.requiresDiskAccess is False
    assert body0.isExclusive is False
    assert body0.name == "RefreshSeries"
    assert body0.trigger == "manual"
    assert body0.suppressMessages is False


def test_command_status() -> None:
    """Test the CommandStatus model."""
    item0 = CommandStatus.from_dict(json.loads(COMMANDS)[0])
    assert item0
    assert item0.name == "RefreshSeries"
    assert isinstance(
        item0.body, CommandStatusBody
    )  # tested in test_command_status_body()
    assert item0.priority == "normal"
    assert item0.status == "started"
    assert item0.queued == datetime(2020, 4, 6, 16, 54, 6, 419450, tzinfo=UTC)
    assert item0.started == datetime(2020, 4, 6, 16, 54, 6, 421322, tzinfo=UTC)
    assert item0.trigger == "manual"
    assert item0.state == "started"
    assert item0.manual is True
    assert item0.startedOn == datetime(2020, 4, 6, 16, 54, 6, 419450, tzinfo=UTC)
    assert item0.stateChangeTime == datetime(2020, 4, 6, 16, 54, 6, 421322, tzinfo=UTC)
    assert item0.sendUpdatesToClient is True
    assert item0.updateScheduledTask is True
    assert item0.id == 368621

    item1 = CommandStatus.from_dict(json.loads(COMMANDS)[1])
    assert item1
    assert item1.name == "RefreshSeries"
    assert item1.body is None
    assert item1.priority is None
    assert item1.status is None
    assert item1.queued is None
    assert item1.started is None
    assert item1.trigger is None
    assert item1.state == "started"
    assert item1.manual is None
    assert item1.startedOn == datetime(2020, 4, 6, 16, 57, 51, 406504, tzinfo=UTC)
    assert item1.stateChangeTime == datetime(2020, 4, 6, 16, 57, 51, 417931, tzinfo=UTC)
    assert item1.sendUpdatesToClient is True
    assert item1.updateScheduledTask is None
    assert item1.id == 368629


def test_disk_space() -> None:
    """Test the DiskSpace model."""
    diskspace = DiskSpace.from_dict(json.loads(DISKSPACE)[0])
    assert diskspace.path == "C:\\"
    assert diskspace.label == ""
    assert diskspace.freeSpace == 282500067328
    assert diskspace.totalSpace == 499738734592


def test_system_status() -> None:
    """Test the SystemStatus model."""
    status = SystemStatus.from_dict(json.loads(SYSTEMSTATUS))

    assert status.version == "2.0.0.1121"

    # "buildTime": "2014-02-08T20:49:36.5560392Z"
    # Round fractional seconds to microseconds
    assert status.buildTime == datetime(2014, 2, 8, 20, 49, 36, 556039, tzinfo=UTC)
    assert status.isDebug is False
    assert status.isProduction is True
    assert status.isAdmin is True
    assert status.isUserInteractive is False
    assert status.startupPath == "C:\\ProgramData\\NzbDrone\\bin"
    assert status.appData == "C:\\ProgramData\\NzbDrone"
    assert status.osVersion == "6.2.9200.0"
    assert status.isMono is False
    assert status.isLinux is False
    assert status.isWindows is True
    assert status.branch == "develop"
    assert status.authentication is False
    assert status.startOfWeek == 0
    assert status.urlBase == ""
