"""Tests for Sonarr API endpoints:
    /episode
    /episodefile
    /calendar
    /wanted/missing

https://github.com/Sonarr/Sonarr/wiki/Calendar
https://github.com/Sonarr/Sonarr/wiki/Episode
https://github.com/Sonarr/Sonarr/wiki/EpisodeFile
https://github.com/Sonarr/Sonarr/wiki/Wanted-Missing
"""
from datetime import datetime, date
import json

import pytest

import downloadcarr.sonarr.models as models
from downloadcarr.client import ArrHttpError
from downloadcarr.sonarr.client import SonarrClient
from downloadcarr.enums import SortKey, SortDirection, HttpMethod
from downloadcarr.utils import UTC

from . import (
    CALENDAR,
    EPISODES,
    EPISODE,
    EPISODEFILES,
    EPISODEFILE,
    HISTORY,
    QUEUE,
    WANTEDMISSING,
    mock_server,
)


CLIENT = SonarrClient("localhost", "MYKEY")


def test_episode() -> None:
    """Test the Episode model."""
    # Episode instance returned by /episode
    ep = models.Episode.from_dict(json.loads(EPISODES)[0])

    assert ep
    assert ep.seriesId == 1
    assert ep.episodeFileId == 0
    assert ep.seasonNumber == 1
    assert ep.episodeNumber == 1
    assert ep.title == "Mole Hunt"
    assert ep.airDate == date(2009, 9, 17)
    assert ep.airDateUtc == datetime(2009, 9, 18, 2, tzinfo=UTC)
    assert ep.overview == (
        "Archer is in trouble with his Mother and the Comptroller because his "
        "expense account is way out of proportion to his actual expenses. So "
        "he creates the idea that a Mole has breached ISIS and he needs to get"
        " into the mainframe to hunt him down (so he can cover his tracks!). "
        "All this leads to a surprising ending."
    )
    assert ep.hasFile is False
    assert ep.monitored is True
    assert ep.sceneEpisodeNumber == 0
    assert ep.sceneSeasonNumber == 0
    assert ep.tvDbEpisodeId == 0
    assert ep.absoluteEpisodeNumber == 1
    assert ep.id == 1
    assert ep.sceneAbsoluteEpisodeNumber is None
    assert ep.series is None
    assert ep.downloading is None
    assert ep.unverifiedSceneNumbering is None
    assert ep.lastSearchTime is None

    # Episode instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(json.loads(WANTEDMISSING))
    ep0, ep1 = want.records
    assert isinstance(ep0, models.Episode)
    assert isinstance(ep1, models.Episode)

    assert ep0.seriesId == 3
    assert ep0.episodeFileId == 0
    assert ep0.seasonNumber == 4
    assert ep0.episodeNumber == 11
    assert ep0.title == "Easy Com-mercial, Easy Go-mercial"
    assert ep0.airDate == date(2014, 1, 26)
    assert ep0.airDateUtc == datetime(2014, 1, 27, 1, 30, tzinfo=UTC)
    assert ep0.overview == (
        'To compete with fellow "restaurateur," Jimmy Pesto, and his blowout '
        "Super Bowl event, Bob is determined to create a Bob's Burgers "
        'commercial to air during the "big game." In an effort to outshine '
        "Pesto, the Belchers recruit Randy, a documentarian, to assist with "
        "the filmmaking and hire on former pro football star Connie Frye to "
        "be the celebrity endorser."
    )
    assert ep0.hasFile is False
    assert ep0.monitored is True
    assert ep0.sceneEpisodeNumber == 0
    assert ep0.sceneSeasonNumber == 0
    assert ep0.tvDbEpisodeId == 0
    assert isinstance(ep0.series, models.Series)  # Series tested in test_models_series
    assert ep0.downloading is False
    assert ep0.id == 14402

    assert ep1.seriesId == 17
    assert ep1.episodeFileId == 0
    assert ep1.seasonNumber == 1
    assert ep1.episodeNumber == 1
    assert ep1.title == "The New Housekeeper"
    assert ep1.airDate == date(1960, 10, 3)
    assert ep1.airDateUtc == datetime(1960, 10, 3, 1, tzinfo=UTC)
    assert ep1.overview == (
        "Sheriff Andy Taylor and his young son Opie are in need of a new "
        "housekeeper. Andy's Aunt Bee looks like the perfect candidate and "
        "moves in, but her presence causes friction with Opie."
    )
    assert ep1.hasFile is False
    assert ep1.monitored is True
    assert ep1.sceneEpisodeNumber == 0
    assert ep1.sceneSeasonNumber == 0
    assert ep1.tvDbEpisodeId == 0
    assert isinstance(ep1.series, models.Series)  # Series tested in test_models_series
    assert ep1.downloading is False
    assert ep1.id == 889

    # Episode instance returned by /calendar
    pass  # /calendar JSON response (Bob's Burgers S04E11) duplicates /wanted/missing

    # Episode instance returned by /history
    hist = models.History.from_dict(json.loads(HISTORY))
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    ep0 = dl0.episode

    assert ep0.seriesId == 60
    assert ep0.episodeFileId == 3464
    assert ep0.seasonNumber == 1
    assert ep0.episodeNumber == 11
    assert ep0.title == "Cease Forcing Enemy"
    assert ep0.airDate == date(2016, 2, 29)
    assert ep0.airDateUtc == datetime(2016, 3, 1, 1, tzinfo=UTC)
    assert ep0.overview == (
        "Jane reels from a series of massive revelations about her tattoos "
        "and grapples with whether to trust Oscar. Meanwhile, a tattoo leads "
        "the team to a shocking discovery in the Black Sea."
    )
    assert ep0.hasFile is True
    assert ep0.monitored is True
    assert ep0.absoluteEpisodeNumber == 11
    assert ep0.unverifiedSceneNumbering is False
    assert ep0.id == 5276

    ep1 = dl1.episode
    assert ep1.seriesId == 60
    assert ep1.episodeFileId == 3464
    assert ep1.seasonNumber == 1
    assert ep1.episodeNumber == 11
    assert ep1.title == "Cease Forcing Enemy"
    assert ep1.airDate == date(2016, 2, 29)
    assert ep1.airDateUtc == datetime(2016, 3, 1, 1, tzinfo=UTC)
    assert ep1.overview == (
        "Jane reels from a series of massive revelations about her tattoos "
        "and grapples with whether to trust Oscar. Meanwhile, a tattoo leads "
        "the team to a shocking discovery in the Black Sea."
    )
    assert ep1.hasFile is True
    assert ep1.monitored is True
    assert ep1.absoluteEpisodeNumber == 11
    assert ep1.unverifiedSceneNumbering is False
    assert ep1.id == 5276

    # instance returned by /parse
    pass  # FIXME - need data

    # instance returned by /queue
    item = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    ep = item.episode
    assert ep.seriesId == 17
    assert ep.episodeFileId == 0
    assert ep.seasonNumber == 1
    assert ep.episodeNumber == 1
    assert ep.title == "The New Housekeeper"
    assert ep.airDate == date(1960, 10, 3)
    assert ep.airDateUtc == datetime(1960, 10, 3, 1, tzinfo=UTC)
    assert ep.overview == (
        "Sheriff Andy Taylor and his young son Opie are in need of a new "
        "housekeeper. Andy's Aunt Bee looks like the perfect candidate and "
        "moves in, but her presence causes friction with Opie."
    )
    assert ep.hasFile is False
    assert ep.monitored is False
    assert ep.absoluteEpisodeNumber == 1
    assert ep.unverifiedSceneNumbering is False
    assert ep.id == 889


@pytest.fixture
def episodes_server():
    yield from mock_server(
        uri="/api/episode?seriesId=1", body=EPISODES, match_query=True
    )


def test_get_episodes(episodes_server):
    """Test API call for SonarrClient.get_episodes()

    GET http://$HOST:8989/api/episode?seriesId=3
    """

    CLIENT.port = episodes_server.server_port
    response = CLIENT.get_episodes(seriesId=1)
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Episode)


@pytest.fixture
def episode_server():
    yield from mock_server(
        uri="/api/episode/1", body=EPISODE,
    )


def test_get_episode(episode_server):
    """Test API call for SonarrClient.get_episode()

    NEEDS EXAMPLE
    """

    CLIENT.port = episode_server.server_port
    response = CLIENT.get_episode(1)
    assert isinstance(response, models.Episode)


@pytest.fixture
def episode_echo_server():
    yield from mock_server(
        uri="/api/episode", body=EPISODE, method=HttpMethod.PUT, echo=True,
    )


def test_update_episode(episode_echo_server):
    """Test API call for SonarrClient.update_episode()

    PUT http://$HOST:8989/api/episode {"seriesId":205,"episodeFileId":46445,"seasonNumber":1,"episodeNumber":1,"title":"The Bone Orchard","airDate":"2017-04-30","airDateUtc":"2017-05-01T01:00:00Z","overview":"When Shadow Moon is released from prison early after the death of his wife, he meets Mr. Wednesday and is recruited as his bodyguard. Shadow discovers that this may be more than he bargained for.","episodeFile":{"seriesId":205,"seasonNumber":1,"relativePath":"Season 1/American Gods - S01E01 - The Bone Orchard WEBDL-720p.mp4","path":"/tank/video/TV/American Gods/Season 1/American Gods - S01E01 - The Bone Orchard WEBDL-720p.mp4","size":2352322048,"dateAdded":"2017-04-30T22:01:17.4243Z","quality":{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"revision":{"version":1,"real":0}},"mediaInfo":{"audioChannels":2,"audioCodec":"AAC","videoCodec":"x264"},"qualityCutoffNotMet":false,"id":46445},"hasFile":true,"monitored":false,"absoluteEpisodeNumber":1,"unverifiedSceneNumbering":false,"id":11937,"status":0}
    """

    CLIENT.port = episode_echo_server.server_port
    episode = models.Episode(
        seriesId=1,
        episodeFileId=0,
        seasonNumber=1,
        episodeNumber=1,
        title="Mole Hunt",
        airDate=date(2009, 9, 17),
        airDateUtc=datetime(2009, 9, 18, 2, tzinfo=UTC),
        overview=(
            "Archer is in trouble with his Mother and the Comptroller because his "
            "expense account is way out of proportion to his actual expenses. So "
            "he creates the idea that a Mole has breached ISIS and he needs to get"
            " into the mainframe to hunt him down (so he can cover his tracks!). "
            "All this leads to a surprising ending."
        ),
        hasFile=False,
        monitored=True,
        sceneEpisodeNumber=0,
        sceneSeasonNumber=0,
        tvDbEpisodeId=0,
        absoluteEpisodeNumber=1,
        id=1,
    )
    response = CLIENT.update_episode(episode)
    assert isinstance(response, models.Episode)
    assert response == episode

    echo = CLIENT._request("echo")
    assert echo == {
        "absoluteEpisodeNumber": 1,
        "airDate": "2009-09-17",
        "airDateUtc": "2009-09-18T02:00:00Z",
        "downloading": None,
        "episodeFile": None,
        "episodeFileId": 0,
        "episodeNumber": 1,
        "hasFile": False,
        "id": 1,
        "lastSearchTime": None,
        "monitored": True,
        "overview": "Archer is in trouble with his Mother and the Comptroller because "
        "his expense account is way out of proportion to his actual "
        "expenses. So he creates the idea that a Mole has breached ISIS "
        "and he needs to get into the mainframe to hunt him down (so he "
        "can cover his tracks!). All this leads to a surprising ending.",
        "sceneAbsoluteEpisodeNumber": None,
        "sceneEpisodeNumber": 0,
        "sceneSeasonNumber": 0,
        "seasonNumber": 1,
        "series": None,
        "seriesId": 1,
        "title": "Mole Hunt",
        "tvDbEpisodeId": 0,
        "unverifiedSceneNumbering": None,
    }


@pytest.fixture
def calendar_server():
    yield from mock_server(uri="/api/calendar", body=CALENDAR)


def test_calendar_basic(calendar_server):
    """Test API call for SonarrClient.get_calendar() without query args"""

    CLIENT.port = calendar_server.server_port
    response = CLIENT.get_calendar()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Episode)


@pytest.fixture
def calendar_server_start_end():
    yield from mock_server(
        uri="/api/calendar?start=2014-01-26&end=2014-01-27",
        body=CALENDAR,
        match_query=True,
    )


def test_calendar_start_end(calendar_server_start_end):
    """Test API call for SonarrClient.get_calendar() with query args

    GET http://$HOST:8989/api/calendar?start=2020-06-13T00%3A00%3A00.000Z&end=2020-06-19T00%3A00%3A00.000Z&unmonitored=false
    """
    CLIENT.port = calendar_server_start_end.server_port
    resp = CLIENT.get_calendar(date(2014, 1, 26), date(2014, 1, 27))

    assert isinstance(resp, tuple)
    assert len(resp) == 1
    assert isinstance(resp[0], models.Episode)

    with pytest.raises(ArrHttpError):
        CLIENT.get_calendar(date(2014, 1, 25), date(2014, 1, 27))


def test_episode_file() -> None:
    """Test the EpisodeFile model."""
    ep = models.EpisodeFile.from_dict(json.loads(EPISODEFILES)[0])

    assert ep
    assert ep.seriesId == 1
    assert ep.seasonNumber == 1
    assert ep.path == (
        "C:\\Test\\Breaking Bad\\Season 01\\"
        "Breaking Bad - S01E01 - Pilot [Bluray 720p].mkv"
    )
    assert ep.size == 2183157756
    assert ep.dateAdded == datetime(2013, 5, 29, 10, 42, 5, 133530, tzinfo=UTC)
    assert ep.sceneName == ""
    assert ep.quality.quality.id == 1
    assert ep.quality.quality.name == "Bluray 720p"
    assert ep.quality.proper is False
    assert ep.id == 1


def test_wanted_missing() -> None:
    """Test the WantedMissing model."""
    want = models.WantedMissing.from_dict(json.loads(WANTEDMISSING))

    assert want
    assert want.page == 1
    assert want.pageSize == 10
    assert want.sortDirection == SortDirection.DESCENDING
    assert want.totalRecords == 2
    assert len(want.records) == 2
    ep0, ep1 = want.records
    #  Episode tested in test_episode()
    assert isinstance(ep0, models.Episode)
    assert isinstance(ep1, models.Episode)


@pytest.fixture
def episodefiles_server():
    yield from mock_server(
        uri="/api/episodefile?seriesId=1", body=EPISODEFILES, match_query=True
    )


def test_get_episodefiles(episodefiles_server):
    """Test API call for SonarrClient.get_episode_files()

    GET http://$HOST:8989/api/episodefile?seriesId=112
    """

    CLIENT.port = episodefiles_server.server_port
    response = CLIENT.get_episode_files(seriesId=1)
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.EpisodeFile)


@pytest.fixture
def episodefile_server():
    yield from mock_server(
        uri="/api/episodefile/1", body=EPISODEFILE,
    )


def test_get_episodefile(episodefile_server):
    """Test API call for SonarrClient.get_episode_file()

    NEEDS EXAMPLE
    """

    CLIENT.port = episodefile_server.server_port
    response = CLIENT.get_episode_file(1)
    assert isinstance(response, models.EpisodeFile)


@pytest.fixture
def episodefile_delete_server():
    yield from mock_server(
        uri="/api/episodefile/1", body="{}", method=HttpMethod.DELETE,
    )


def test_delete_episode_file(episodefile_delete_server):
    """Test API call for SonarrClient.delete_episode_file()

    NEEDS EXAMPLE
    """

    CLIENT.port = episodefile_delete_server.server_port
    response = CLIENT.delete_episode_file(1)
    assert response is None


@pytest.fixture
def episodefile_echo_server():
    yield from mock_server(
        uri="/api/episodefile/1", body=EPISODEFILE, method=HttpMethod.PUT, echo=True,
    )


def test_update_episode_file(episodefile_echo_server):
    """Test API call for SonarrClient.update_episode_file()

    NEEDS EXAMPLE
    """

    CLIENT.port = episodefile_echo_server.server_port
    quality = models.QualityRevision(
        quality=models.Quality(id=8), revision=models.Revision(version=1, real=0)
    )
    response = CLIENT.update_episode_file(1, quality)
    assert isinstance(response, models.EpisodeFile)

    echo = CLIENT._request("echo")
    assert echo == {
        "quality": {
            "quality": {
                "id": 8,
                "name": None,
                "resolution": None,
                "source": None,
                "weight": None,
            },
            "revision": {"version": 1, "real": 0},
            "proper": None,
        },
    }


@pytest.fixture
def wanted_missing_server():
    yield from mock_server(
        uri="/api/wanted/missing?sortKey=airDateUtc&page=1&pageSize=10&sortDir=asc",
        body=WANTEDMISSING,
        match_query=True,
    )


def test_get_wanted_missing(wanted_missing_server):
    """Test API call for SonarrClient.get_wanted_missing() with default query args

    GET http://$HOST:8989/api/wanted/missing?page=1&pageSize=15&sortKey=airDateUtc&sortDir=desc&filterKey=monitored&filterValue=true
    """
    CLIENT.port = wanted_missing_server.server_port
    response = CLIENT.get_wanted_missing(sortKey=SortKey.AIRDATE)
    assert isinstance(response, models.WantedMissing)

    assert response.pageSize == 10
    assert response.totalRecords == 2
    assert response.sortKey is SortKey.AIRDATE
    assert response.sortDirection is SortDirection.DESCENDING

    assert isinstance(response.records, tuple)
    assert len(response.records) == 2

    for record in response.records:
        assert isinstance(record, models.Episode)
