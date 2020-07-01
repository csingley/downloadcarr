"""Tests for Sonarr API /parse endpoint

https://github.com/Sonarr/Sonarr/wiki/Parse
"""
import json

import pytest

import downloadcarr.sonarr.models as models
from downloadcarr.sonarr.client import SonarrClient

from . import PARSE, mock_server


CLIENT = SonarrClient("localhost", "MYKEY")


def test_series_title_info() -> None:
    """Test the SeriesTitleInfo model."""
    # instance returned by /parse
    parsed = models.ParseResult.from_dict(json.loads(PARSE))
    info = parsed.parsedEpisodeInfo.seriesTitleInfo
    assert info.title == "Series Title"
    assert info.titleWithoutYear == "Series Title"
    assert info.year == 0


def test_parsed_episode_info() -> None:
    """Test the ParsedEpisodeInfo model."""
    # instance returned by /parse
    parsed = models.ParseResult.from_dict(json.loads(PARSE))
    info = parsed.parsedEpisodeInfo
    assert info.releaseTitle == "Series.Title.S01E01.720p.HDTV-Sonarr"
    assert info.seriesTitle == "Series Title"
    # tested in test_models_quality.test_quality_revision()
    assert isinstance(info.quality, models.QualityRevision)
    assert info.seasonNumber == 1
    assert info.episodeNumbers == (1, )
    assert info.absoluteEpisodeNumbers == ()
    assert info.language == "english"
    assert info.fullSeason is False
    assert info.special is False
    assert info.releaseGroup == "Sonarr"
    assert info.releaseHash == ""
    assert info.isDaily is False
    assert info.isAbsoluteNumbering is False
    assert info.isPossibleSpecialEpisode is False


def test_parse_result() -> None:
    """Test the ParseResult model."""
    # instance returned by /parse
    parsed = models.ParseResult.from_dict(json.loads(PARSE))
    assert parsed.title == "Series.Title.S01E01.720p.HDTV-Sonarr"
    assert parsed.series is None
    assert parsed.episodes == ()


@pytest.fixture
def parse_title_server():
    yield from mock_server(
        uri="/api/parse?title=Title",
        body=PARSE,
        match_query=True,
    )


def test_parse_title(parse_title_server):
    """Test API call for SonarrClient.parse_title()

    NEEDS EXAMPLE
    """

    CLIENT.port = parse_title_server.server_port
    response = CLIENT.parse_title("Title")
    assert isinstance(response, models.ParseResult)


@pytest.fixture
def parse_path_server():
    yield from mock_server(
        uri="/api/parse?path=Path",
        body=PARSE,
        match_query=True,
    )


def test_parse_path(parse_path_server):
    """Test API call for SonarrClient.parse_path()

    NEEDS EXAMPLE
    """

    CLIENT.port = parse_path_server.server_port
    response = CLIENT.parse_path("Path")
    assert isinstance(response, models.ParseResult)
