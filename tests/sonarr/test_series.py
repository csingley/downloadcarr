"""Tests for Sonarr API /series endpoint

https://github.com/Sonarr/Sonarr/wiki/Series
https://github.com/Sonarr/Sonarr/wiki/Series-Lookup
"""
from datetime import datetime, time
import json
from urllib.parse import urlencode

import pytest

import downloadcarr.sonarr.models as models
from downloadcarr.sonarr.client import SonarrClient
from downloadcarr.enums import HttpMethod
from downloadcarr.utils import UTC

from . import (
    ALLSERIES,
    SERIES,
    SERIESLOOKUP,
    SERIESPOST,
    HISTORY,
    QUEUE,
    WANTEDMISSING,
    TAG,
    mock_server,
)


CLIENT = SonarrClient("localhost", "MYKEY")


def test_season_statistics() -> None:
    """Test the SeasonStatistics model."""
    # instance returned by /series
    series = models.Series.from_dict(json.loads(ALLSERIES)[0])
    seasons = series.seasons
    assert isinstance(seasons, tuple)
    assert len(seasons) == 2
    seas0, seas1 = seasons

    stats0 = seas0.statistics
    assert stats0.previousAiring == datetime(2015, 4, 10, 4, 1, tzinfo=UTC)
    assert stats0.episodeFileCount == 13
    assert stats0.episodeCount == 13
    assert stats0.totalEpisodeCount == 13
    assert stats0.sizeOnDisk == 22738179333
    assert stats0.percentOfEpisodes == 100

    stats1 = seas1.statistics
    assert stats1.previousAiring == datetime(2016, 3, 18, 4, 1, tzinfo=UTC)
    assert stats1.episodeFileCount == 13
    assert stats1.episodeCount == 13
    assert stats1.totalEpisodeCount == 13
    assert stats1.sizeOnDisk == 56544094360
    assert stats1.percentOfEpisodes == 100


def test_season() -> None:
    """Test the Season model."""
    # instance returned by /series
    series = models.Series.from_dict(json.loads(ALLSERIES)[0])
    seasons = series.seasons
    assert isinstance(seasons, tuple)
    assert len(seasons) == 2
    seas0, seas1 = seasons

    assert seas0.seasonNumber == 1
    assert seas0.monitored is False
    # tested in test_season_statistics()
    assert isinstance(seas0.statistics, models.SeasonStatistics)

    assert seas1.seasonNumber == 2
    assert seas1.monitored is False
    # tested in test_season_statistics()
    assert isinstance(seas1.statistics, models.SeasonStatistics)

    # instance returned by /series/lookup
    series = models.Series.from_dict(json.loads(SERIESLOOKUP)[0])
    seasons = series.seasons
    assert isinstance(seasons, tuple)
    assert len(seasons) == 5
    seas0, seas1, seas2, seas3, seas4 = seasons

    assert seas0.seasonNumber == 0
    assert seas0.monitored is False

    assert seas1.seasonNumber == 1
    assert seas1.monitored is False

    assert seas2.seasonNumber == 2
    assert seas2.monitored is False

    assert seas3.seasonNumber == 3
    assert seas3.monitored is False

    assert seas4.seasonNumber == 4
    assert seas4.monitored is False

    # instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(json.loads(WANTEDMISSING))
    ep0, ep1 = want.records

    ser0 = ep0.series
    seasons = ser0.seasons
    assert isinstance(seasons, tuple)
    assert len(seasons) == 5
    seas0, seas1, seas2, seas3, seas4 = seasons
    assert seas0.seasonNumber == 4
    assert seas0.monitored is True
    assert seas1.seasonNumber == 3
    assert seas1.monitored is True
    assert seas2.seasonNumber == 2
    assert seas2.monitored is True
    assert seas3.seasonNumber == 1
    assert seas3.monitored is True
    assert seas4.seasonNumber == 0
    assert seas4.monitored is False

    ser1 = ep1.series
    seasons = ser1.seasons
    assert isinstance(seasons, tuple)
    assert len(seasons) == 9
    assert seasons[0].seasonNumber == 0
    assert seasons[0].monitored is False
    assert seasons[1].seasonNumber == 1
    assert seasons[1].monitored is False
    assert seasons[2].seasonNumber == 2
    assert seasons[2].monitored is True
    assert seasons[3].seasonNumber == 3
    assert seasons[3].monitored is False
    assert seasons[4].seasonNumber == 4
    assert seasons[4].monitored is False
    assert seasons[5].seasonNumber == 5
    assert seasons[5].monitored is True
    assert seasons[6].seasonNumber == 6
    assert seasons[6].monitored is True
    assert seasons[7].seasonNumber == 7
    assert seasons[7].monitored is True
    assert seasons[8].seasonNumber == 8
    assert seasons[8].monitored is True

    # instance returned by /queue
    pass  # Identical to 2nd series in /wanted/missing i.e. "Andy Griffith Show"


def test_rating() -> None:
    """Test the Rating model."""
    # instance returned by /series
    series = models.Series.from_dict(json.loads(ALLSERIES)[0])
    ratings = series.ratings
    assert ratings.votes == 461
    assert ratings.value == 8.9

    # instance returned by /series/lookup
    series = models.Series.from_dict(json.loads(SERIESLOOKUP)[0])
    ratings = series.ratings
    assert ratings.votes == 182
    assert ratings.value == 8.6

    # instance returned by /history
    hist = models.History.from_dict(json.loads(HISTORY))
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    ser0 = dl0.series
    rating0 = ser0.ratings
    assert rating0.votes == 51
    assert rating0.value == 8.1

    ser1 = dl1.series
    rating1 = ser1.ratings
    assert rating1.votes == 51
    assert rating1.value == 8.1

    # instance returned by /queue
    item = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    series = item.series
    rating = series.ratings
    assert rating.votes == 547
    assert rating.value == 8.6


def test_alternate_title() -> None:
    """Test the AlternateTitle model."""
    # instance returned by /series
    series = models.Series.from_dict(json.loads(ALLSERIES)[0])
    altTitles = series.alternateTitles
    assert isinstance(altTitles, tuple)
    assert len(altTitles) == 1
    altTitle = altTitles[0]
    assert altTitle.title == "Daredevil"
    assert altTitle.seasonNumber == -1


def test_image() -> None:
    """Test the Image model."""
    # instance returned by /series
    series = models.Series.from_dict(json.loads(ALLSERIES)[0])
    images = series.images
    assert isinstance(images, tuple)
    assert len(images) == 3
    img0, img1, img2 = images

    assert img0.coverType == "fanart"
    assert img0.url == "/sonarr/MediaCover/7/fanart.jpg?lastWrite=636072351904299472"

    assert img1.coverType == "banner"
    assert img1.url == "/sonarr/MediaCover/7/banner.jpg?lastWrite=636071666185812942"

    assert img2.coverType == "poster"
    assert img2.url == "/sonarr/MediaCover/7/poster.jpg?lastWrite=636071666195067584"

    # instance returned by /series/lookup
    series = models.Series.from_dict(json.loads(SERIESLOOKUP)[0])
    images = series.images
    assert isinstance(images, tuple)
    assert len(images) == 3
    img0, img1, img2 = images

    assert img0.coverType == "fanart"
    assert img0.url == "http://thetvdb.com/banners/fanart/original/266189-24.jpg"

    assert img1.coverType == "banner"
    assert img1.url == "http://thetvdb.com/banners/graphical/266189-g22.jpg"

    assert img2.coverType == "poster"
    assert img2.url == "http://thetvdb.com/banners/posters/266189-14.jpg"

    # instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(json.loads(WANTEDMISSING))
    ep0, ep1 = want.records

    ser0 = ep0.series
    images = ser0.images
    assert len(images) == 3
    img0, img1, img2 = images

    assert img0.coverType == "banner"
    assert img0.url == "http://slurm.trakt.us/images/banners/1387.6.jpg"

    assert img1.coverType == "poster"
    assert img1.url == "http://slurm.trakt.us/images/posters/1387.6-300.jpg"

    assert img2.coverType == "fanart"
    assert img2.url == "http://slurm.trakt.us/images/fanart/1387.6.jpg"

    ser1 = ep1.series
    images = ser1.images
    assert len(images) == 3
    img0, img1, img2 = images

    assert img0.coverType == "fanart"
    assert (
        img0.url == "https://artworks.thetvdb.com/banners/fanart/original/77754-5.jpg"
    )
    assert img1.coverType == "banner"
    assert img1.url == "https://artworks.thetvdb.com/banners/graphical/77754-g.jpg"
    assert img2.coverType == "poster"
    assert img2.url == "https://artworks.thetvdb.com/banners/posters/77754-4.jpg"

    # instance returned by /queue
    pass  # identical to 2nd series from /wanted/missing i.e. "Andy Griffith Show"


def test_series() -> None:
    """Test the Series model."""
    # instance returned by /series
    series = models.Series.from_dict(json.loads(ALLSERIES)[0])
    assert series.title == "Marvel's Daredevil"
    assert isinstance(series.alternateTitles, tuple)
    for at in series.alternateTitles:
        assert isinstance(at, models.AlternateTitle)  # tested in test_alternate_title()
    assert series.sortTitle == "marvels daredevil"
    assert series.seasonCount == 2
    assert series.totalEpisodeCount == 26
    assert series.episodeCount == 26
    assert series.episodeFileCount == 26
    assert series.sizeOnDisk == 79282273693
    assert series.status == "continuing"
    assert series.overview == (
        "Matt Murdock was blinded in a tragic accident as a boy, but imbued "
        "with extraordinary senses. Murdock sets up practice in his old "
        "neighborhood of Hell's Kitchen, New York, where he now fights "
        "against injustice as a respected lawyer by day and as the masked "
        "vigilante Daredevil by night."
    )
    assert series.previousAiring == datetime(2016, 3, 18, 4, 1, tzinfo=UTC)
    assert series.network == "Netflix"
    assert series.airTime == time(0, 1)
    assert isinstance(series.images, tuple)
    for at in series.images:
        assert isinstance(at, models.Image)  # tested in test_image()
    assert isinstance(series.seasons, tuple)
    for at in series.seasons:
        assert isinstance(at, models.Season)  # tested in test_season()
    assert series.year == 2015
    assert series.path == "F:\\TV_Shows\\Marvels Daredevil"
    assert series.profileId == 6
    assert series.seasonFolder is True
    assert series.monitored is True
    assert series.useSceneNumbering is False
    assert series.runtime == 55
    assert series.tvdbId == 281662
    assert series.tvRageId == 38796
    assert series.tvMazeId == 1369
    assert series.firstAired == datetime(2015, 4, 10, 4, tzinfo=UTC)
    # "lastInfoSync": "2016-09-09T09:02:49.4402575Z"
    # Round fractional seconds to microseconds
    assert series.lastInfoSync == datetime(2016, 9, 9, 9, 2, 49, 440258, tzinfo=UTC)
    assert series.seriesType == "standard"
    assert series.cleanTitle == "marvelsdaredevil"
    assert series.imdbId == "tt3322312"
    assert series.titleSlug == "marvels-daredevil"
    assert series.certification == "TV-MA"
    assert series.genres == ("Action", "Crime", "Drama")
    assert series.tags == ()
    #  "added": "2015-05-15T00:20:32.7892744Z"
    # Round fractional seconds to microseconds
    assert series.added == datetime(2015, 5, 15, 0, 20, 32, 789274, tzinfo=UTC)
    assert isinstance(series.ratings, models.Rating)  # tested in test_rating()
    assert series.qualityProfileId == 6
    assert series.id == 7

    # instance returned by /series/lookup
    series = models.Series.from_dict(json.loads(SERIESLOOKUP)[0])
    assert series.title == "The Blacklist"
    assert series.sortTitle == "blacklist"
    assert series.seasonCount == 4
    assert series.status == "continuing"
    assert series.overview == (
        """Raymond "Red" Reddington, one of the FBI's most wanted fugitives, """
        "surrenders in person at FBI Headquarters in Washington, D.C. He "
        "claims that he and the FBI have the same interests: bringing down "
        "dangerous criminals and terrorists. In the last two decades, he's "
        "made a list of criminals and terrorists that matter the most but the "
        "FBI cannot find because it does not know they exist. Reddington "
        'calls this "The Blacklist".\nReddington will co-operate, but insists '
        "that he will speak only to Elizabeth Keen, a rookie FBI profiler."
    )
    assert series.network == "NBC"
    assert series.airTime == time(21)
    assert isinstance(series.images, tuple)
    for at in series.images:
        assert isinstance(at, models.Image)  # tested in test_image()
    assert series.remotePoster == "http://thetvdb.com/banners/posters/266189-14.jpg"
    assert isinstance(series.seasons, tuple)
    for seas in series.seasons:
        assert isinstance(seas, models.Season)  # tested in test_season()
    assert series.year == 2013
    assert series.profileId == 0
    assert series.seasonFolder is False
    assert series.monitored is False
    assert series.useSceneNumbering is False
    assert series.runtime == 45
    assert series.tvdbId == 266189
    assert series.tvRageId == 35048
    assert series.tvMazeId == 69
    assert series.firstAired == datetime(2013, 9, 23, 5, tzinfo=UTC)
    assert series.seriesType == "standard"
    assert series.cleanTitle == "theblacklist"
    assert series.imdbId == "tt2741602"
    assert series.titleSlug == "the-blacklist"
    assert series.certification == "TV-14"
    assert series.genres == ("Action", "Crime", "Drama", "Mystery")
    assert series.tags == ()
    assert series.added == datetime(1, 1, 1, tzinfo=UTC)
    assert isinstance(series.ratings, models.Rating)  # tested in test_rating()
    assert series.qualityProfileId == 0

    # instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(json.loads(WANTEDMISSING))
    ep0, ep1 = want.records

    ser0 = ep0.series
    assert ser0.tvdbId == 194031
    assert ser0.tvRageId == 24607
    assert ser0.imdbId == "tt1561755"
    assert ser0.title == "Bob's Burgers"
    assert ser0.sortTitle == "bob burgers"
    assert ser0.cleanTitle == "bobsburgers"
    assert ser0.seasonCount == 4
    assert ser0.status == "continuing"
    assert ser0.overview == (
        "Bob's Burgers follows a third-generation restaurateur, Bob, as he "
        "runs Bob's Burgers with the help of his wife and their three kids. "
        "Bob and his quirky family have big ideas about burgers, but fall "
        "short on service and sophistication. Despite the greasy counters, "
        "lousy location and a dearth of customers, Bob and his family are "
        'determined to make Bob\'s Burgers "grand re-re-re-opening" a success.'
    )
    assert ser0.airTime == time(17, 30)
    assert ser0.monitored is True
    assert ser0.qualityProfileId == 1
    assert ser0.seasonFolder is True
    assert ser0.lastInfoSync == datetime(2014, 1, 26, 19, 25, 55, 455594, tzinfo=UTC)
    assert ser0.runtime == 30

    images = ser0.images
    assert isinstance(images, tuple)
    for img in images:
        assert isinstance(img, models.Image)  # tested in test_models_image()
    assert ser0.seriesType == "standard"
    assert ser0.network == "FOX"
    assert ser0.useSceneNumbering is False
    assert ser0.titleSlug == "bobs-burgers"
    assert ser0.certification == "TV-14"
    assert ser0.path == "T:\\Bob's Burgers"
    assert ser0.year == 2011
    assert ser0.firstAired == datetime(2011, 1, 10, 1, 30, tzinfo=UTC)
    assert ser0.genres == ("Animation", "Comedy")
    assert ser0.tags == ()
    assert ser0.added == datetime(2011, 1, 26, 19, 25, 55, 455594, tzinfo=UTC)

    #  QualityProfile tested in test_models_quality.test_quality_profile()
    assert isinstance(ser0.qualityProfile, models.QualityProfile)

    seasons = ser0.seasons
    assert isinstance(seasons, tuple)
    for seas in seasons:
        assert isinstance(seas, models.Season)  # tested in test_models_season()
    assert ser0.id == 66

    ser1 = ep1.series
    assert ser1.imdbId == ""
    assert ser1.tvdbId == 77754
    assert ser1.tvRageId == 5574
    assert ser1.tvMazeId == 3853
    assert ser1.title == "The Andy Griffith Show"
    assert ser1.sortTitle == "andy griffith show"
    assert ser1.cleanTitle == "theandygriffithshow"
    assert ser1.seasonCount == 8
    assert ser1.status == "ended"
    assert ser1.overview == (
        "Down-home humor and an endearing cast of characters helped make The "
        "Andy Griffith Show one of the most beloved comedies in the history "
        "of TV. The show centered around widower Andy Taylor, who divided his "
        "time between raising his young son Opie, and his job as sheriff of "
        "the sleepy North Carolina town, Mayberry. Andy and Opie live with "
        "Andy's Aunt Bee, who serves as a surrogate mother to both father and "
        "son. Andy's nervous cousin, Barney Fife, is his deputy sheriff whose "
        "incompetence is tolerated because Mayberry is virtually crime-free."
    )
    assert ser1.airTime == time(21, 30)
    assert ser1.monitored is True
    assert ser1.qualityProfileId == 1
    assert ser1.seasonFolder is True
    assert ser1.lastInfoSync == datetime(2016, 2, 5, 16, 40, 11, 614176, tzinfo=UTC)
    assert ser1.runtime == 25
    images = ser1.images
    assert isinstance(images, tuple)
    for img in images:
        assert isinstance(img, models.Image)  # tested in test_models_image()
    assert ser1.seriesType == "standard"
    assert ser1.network == "CBS"
    assert ser1.useSceneNumbering is False
    assert ser1.titleSlug == "the-andy-griffith-show"
    assert ser1.certification == "TV-G"
    assert ser1.path == "F:\\The Andy Griffith Show"
    assert ser1.year == 1960
    assert ser1.firstAired == datetime(1960, 2, 15, 6, tzinfo=UTC)
    assert ser1.genres == ("Comedy",)
    assert ser1.tags == ()
    assert ser1.added == datetime(2008, 2, 4, 13, 44, 24, 204583, tzinfo=UTC)
    # tested in test_models_quality.test_quality_profile()
    assert isinstance(ser1.qualityProfile, models.QualityProfile)
    seasons = ser1.seasons
    assert isinstance(seasons, tuple)
    for seas in seasons:
        assert isinstance(seas, models.Season)  # tested in test_season()
    assert ser1.id == 17

    # Series instance returned by /history
    hist = models.History.from_dict(json.loads(HISTORY))
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    ser0 = dl0.series
    assert ser0.title == "Blindspot"
    assert ser0.sortTitle == "blindspot"
    assert ser0.seasonCount == 0
    assert ser0.status == "continuing"
    assert ser0.overview == (
        "A vast international plot explodes when a beautiful Jane Doe is "
        "discovered naked in Times Square, completely covered in "
        "mysterious, intricate tattoos with no memory of who she is or how "
        "she got there. But there's one tattoo that is impossible to miss: "
        "the name of FBI agent Kurt Weller, emblazoned across her back. "
        '"Jane," Agent Weller and the rest of the FBI quickly realize that '
        "each mark on her body is a crime to solve, leading them closer to "
        "the truth about her identity and the mysteries to be revealed."
    )
    assert ser0.network == "NBC"
    assert ser0.airTime == time(20)
    assert ser0.images == ()
    assert ser0.seasons == ()
    assert ser0.year == 2015
    assert ser0.path == "F:\\TV_Shows\\Blindspot"
    assert ser0.profileId == 6
    assert ser0.seasonFolder is True
    assert ser0.monitored is True
    assert ser0.useSceneNumbering is False
    assert ser0.runtime == 45
    assert ser0.tvdbId == 295647
    assert ser0.tvRageId == 0
    assert ser0.tvMazeId == 1855
    assert ser0.firstAired == datetime(2015, 9, 21, 4, tzinfo=UTC)
    # "lastInfoSync": "2016-09-10T09:03:51.98498Z"
    # 0.98498 seconds == 984980 microseconds
    assert ser0.lastInfoSync == datetime(2016, 9, 10, 9, 3, 51, 984980, tzinfo=UTC)
    assert ser0.seriesType == "standard"
    assert ser0.cleanTitle == "blindspot"
    assert ser0.imdbId == "tt4474344"
    assert ser0.titleSlug == "blindspot"
    assert ser0.certification == "TV-14"
    assert ser0.genres == ()
    assert ser0.tags == (2,)
    # "added": "2015-08-13T01:36:54.4303036Z"
    # Round to milliseconds
    assert ser0.added == datetime(2015, 8, 13, 1, 36, 54, 430304, tzinfo=UTC)
    assert isinstance(ser0.ratings, models.Rating)  # tested in test_rating()
    assert ser0.qualityProfileId == 6
    assert ser0.id == 60

    ser1 = dl1.series
    assert ser1.title == "Blindspot"
    assert ser1.sortTitle == "blindspot"
    assert ser1.seasonCount == 0
    assert ser1.status == "continuing"
    assert ser1.overview == (
        "A vast international plot explodes when a beautiful Jane Doe is "
        "discovered naked in Times Square, completely covered in mysterious, "
        "intricate tattoos with no memory of who she is or how she got there. "
        "But there's one tattoo that is impossible to miss: the name of FBI "
        'agent Kurt Weller, emblazoned across her back. "Jane," Agent Weller '
        "and the rest of the FBI quickly realize that each mark on her body "
        "is a crime to solve, leading them closer to the truth about her "
        "identity and the mysteries to be revealed."
    )
    assert ser1.network == "NBC"
    assert ser1.airTime == time(20)
    assert ser1.images == ()
    assert ser1.seasons == ()
    assert ser1.year == 2015
    assert ser1.path == "F:\\TV_Shows\\Blindspot"
    assert ser1.profileId == 6
    assert ser1.seasonFolder is True
    assert ser1.monitored is True
    assert ser1.useSceneNumbering is False
    assert ser1.runtime == 45
    assert ser1.tvdbId == 295647
    assert ser1.tvRageId == 0
    assert ser1.tvMazeId == 1855
    assert ser1.firstAired == datetime(2015, 9, 21, 4, tzinfo=UTC)
    # "lastInfoSync": "2016-09-10T09:03:51.98498Z"
    # 0.98498 seconds == 984980 microseconds
    assert ser1.lastInfoSync == datetime(2016, 9, 10, 9, 3, 51, 984980, tzinfo=UTC)
    assert ser1.seriesType == "standard"
    assert ser1.cleanTitle == "blindspot"
    assert ser1.imdbId == "tt4474344"
    assert ser1.titleSlug == "blindspot"
    assert ser1.certification == "TV-14"
    assert ser1.genres == ()
    assert ser1.tags == (2,)
    # "added": "2015-08-13T01:36:54.4303036Z"
    # Round to microseconds
    assert ser1.added == datetime(2015, 8, 13, 1, 36, 54, 430304, tzinfo=UTC)
    assert isinstance(ser1.ratings, models.Rating)  # tested in test_rating()
    assert ser1.qualityProfileId == 6
    assert ser1.id == 60

    # Series instance returned by /parse
    pass  # FIXME - need data

    # Series instance returned by /queue
    item = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    series = item.series

    assert series.title == "The Andy Griffith Show"
    assert series.sortTitle == "andy griffith show"
    assert series.seasonCount == 8
    assert series.status == "ended"
    assert series.overview == (
        "Down-home humor and an endearing cast of characters helped make The "
        "Andy Griffith Show one of the most beloved comedies in the history "
        "of TV. The show centered around widower Andy Taylor, who divided his "
        "time between raising his young son Opie, and his job as sheriff of "
        "the sleepy North Carolina town, Mayberry. Andy and Opie live with "
        "Andy's Aunt Bee, who serves as a surrogate mother to both father and "
        "son. Andy's nervous cousin, Barney Fife, is his deputy sheriff whose "
        "incompetence is tolerated because Mayberry is virtually crime-free."
    )
    assert series.network == "CBS"
    assert series.airTime == time(21, 30)
    assert isinstance(series.images, tuple)
    for img in series.images:
        assert isinstance(img, models.Image)  # tested in test_image()
    assert isinstance(series.seasons, tuple)
    for seas in series.seasons:
        assert isinstance(seas, models.Season)  # tested in test_season()
    assert series.year == 1960
    assert series.path == "F:\\The Andy Griffith Show"
    assert series.profileId == 5
    assert series.seasonFolder is True
    assert series.monitored is True
    assert series.useSceneNumbering is False
    assert series.runtime == 25
    assert series.tvdbId == 77754
    assert series.tvRageId == 5574
    assert series.tvMazeId == 3853
    assert series.firstAired == datetime(1960, 2, 15, 6, tzinfo=UTC)
    assert series.lastInfoSync == datetime(2016, 2, 5, 16, 40, 11, 614176, tzinfo=UTC)
    assert series.seriesType == "standard"
    assert series.cleanTitle == "theandygriffithshow"
    assert series.imdbId == ""
    assert series.titleSlug == "the-andy-griffith-show"
    assert series.certification == "TV-G"
    assert series.genres == ("Comedy",)
    assert series.tags == ()
    assert series.added == datetime(2008, 2, 4, 13, 44, 24, 204583, tzinfo=UTC)
    assert isinstance(series.ratings, models.Rating)  # tested in test_rating()
    assert series.qualityProfileId == 5
    assert series.id == 17


@pytest.fixture
def all_series_server():
    yield from mock_server(
        uri="/api/series", body=ALLSERIES,
    )


def test_get_all_series(all_series_server):
    """Test API call for SonarrClient.get_all_series()

    GET http://$HOST:8989/api/series?sort_by=sortTitle&order=asc
    """

    CLIENT.port = all_series_server.server_port
    response = CLIENT.get_all_series()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Series)
    assert isinstance(response[0].seasons, tuple)
    assert len(response[0].seasons) == 2
    for season in response[0].seasons:
        assert isinstance(season, models.Season)


@pytest.fixture
def series_server():
    yield from mock_server(
        uri="/api/series/3", body=SERIES,
    )


def test_get_series(series_server):
    """Test API call for SonarrClient.get_series()

    NEEDS EXAMPLE
    """

    CLIENT.port = series_server.server_port
    response = CLIENT.get_series(3)

    assert isinstance(response, models.Series)
    assert isinstance(response.seasons, tuple)
    assert len(response.seasons) == 3
    for season in response.seasons:
        assert isinstance(season, models.Season)


@pytest.fixture
def add_series_echo_server():
    yield from mock_server(
        uri="/api/series", body=SERIESPOST, method=HttpMethod.POST, echo=True,
    )


def test_add_series(add_series_echo_server):
    """Test API call for SonarrClient.add_series()

    NEEDS EXAMPLE
    """

    CLIENT.port = add_series_echo_server.server_port
    response = CLIENT.add_series(
        tvdbId=110381,
        title="Archer (2009)",
        profileId=1,
        titleSlug="archer-2009",
        seasons=(
            models.Season(seasonNumber=5, monitored=True),
            models.Season(seasonNumber=4, monitored=True),
            models.Season(seasonNumber=3, monitored=True),
            models.Season(seasonNumber=2, monitored=True),
            models.Season(seasonNumber=1, monitored=True),
            models.Season(seasonNumber=0, monitored=False),
        ),
        path="T:\\Archer (2009)",
    )
    assert isinstance(response, models.Series)
    assert len(response.seasons) == 6
    for season in response.seasons:
        assert isinstance(season, models.Season)

    echo = CLIENT._request("echo")
    assert echo == {
        "tvdbId": 110381,
        "title": "Archer (2009)",
        "profileId": 1,
        "titleSlug": "archer-2009",
        "seasons": [
            {"monitored": True, "seasonNumber": 5, "statistics": None},
            {"monitored": True, "seasonNumber": 4, "statistics": None},
            {"monitored": True, "seasonNumber": 3, "statistics": None},
            {"monitored": True, "seasonNumber": 2, "statistics": None},
            {"monitored": True, "seasonNumber": 1, "statistics": None},
            {"monitored": False, "seasonNumber": 0, "statistics": None},
        ],
        "path": "T:\\Archer (2009)",
        "images": [],
        "monitored": True,
        "seasonFolder": True,
        "addOptions": {
            "ignoreEpisodesWithFiles": False,
            "ignoreEpisodesWithoutFiles": False,
            "searchForMissingEpisodes": False,
        },
    }


@pytest.fixture
def update_series_echo_server():
    yield from mock_server(
        uri="/api/series/1", body=SERIESPOST, method=HttpMethod.PUT, echo=True,
    )


def test_update_series(update_series_echo_server):
    """Test API call for SonarrClient.update_series()

    PUT http://$HOST:8989/api/series/113 {"title":"The Corner","alternateTitles":[],"sortTitle":"corner","seasonCount":1,"totalEpisodeCount":6,"episodeCount":0,"episodeFileCount":0,"sizeOnDisk":0,"status":"ended","overview":"Based on the nonfiction book \"The Corner: A Year in the Life of an Inner-City Neighborhood\", by journalists David Simon and Edward Burns, The Corner presents the world of Fayette Street using real names and real events. The Corner tells the true story of men, women and children living amid the open-air drug markets of West Baltimore. It chronicles a year in the lives of 15-year old DeAndre McCullough (Sean Nelson, \"THE WOOD\"), his mother Fran Boyd (Khandi Alexander), and his father Gary McCullough (T.K. Carter), as well as other addicts and low-level drug dealers caught up in the twin-engine economy of heroin and cocaine.","network":"HBO","images":[{"coverType":"banner","url":"/sonarr/MediaCover/113/banner.jpg?lastWrite=637122344761424010"},{"coverType":"poster","url":"/sonarr/MediaCover/113/poster.jpg?lastWrite=636101576081466180"},{"coverType":"fanart","url":"/sonarr/MediaCover/113/fanart.jpg?lastWrite=636101576079066170"}],"seasons":[{"seasonNumber":1,"monitored":true,"statistics":{"episodeFileCount":0,"episodeCount":0,"totalEpisodeCount":6,"sizeOnDisk":0,"percentOfEpisodes":0}}],"year":2000,"path":"/tank/video/TV/The Corner","profileId":"1","seasonFolder":true,"monitored":true,"useSceneNumbering":false,"runtime":60,"tvdbId":76897,"tvRageId":5696,"tvMazeId":5802,"firstAired":"2000-04-16T05:00:00Z","lastInfoSync":"2020-05-20T12:22:31.108946Z","seriesType":"standard","cleanTitle":"thecorner","imdbId":"tt0224853","titleSlug":"the-corner","genres":["Drama","Mini-Series"],"tags":[1],"added":"2016-09-22T16:13:27.620615Z","ratings":{"votes":315,"value":8.5},"qualityProfileId":1,"id":113,"isExisting":false,"statusWeight":3,"profiles":[{"id":1,"name":"Any","cutoff":{"id":1,"name":"SDTV","source":"television","resolution":480},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":true},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":true},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":true},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":true},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":true},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":true},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":true},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":true},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":true},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"},{"id":2,"name":"SD","cutoff":{"id":1,"name":"SDTV","source":"television","resolution":480},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":true},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":true},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":true},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":false},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":false},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":false},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":false},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":false},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":false},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"},{"id":3,"name":"HD-720p","cutoff":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":false},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":false},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":false},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":true},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":false},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":true},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":true},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":false},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":false},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"},{"id":4,"name":"HD-1080p","cutoff":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":false},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":false},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":false},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":false},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":true},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":false},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":false},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":true},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":true},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"},{"id":5,"name":"Ultra-HD","cutoff":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":false},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":false},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":false},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":false},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":false},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":false},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":false},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":false},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":false},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":true},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":true},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":true}],"language":"english"},{"id":6,"name":"HD - 720p/1080p","cutoff":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":false},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":false},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":false},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":true},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":true},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":true},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":true},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":true},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":true},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"}]}
    """

    CLIENT.port = update_series_echo_server.server_port

    series = models.Series(
        tvdbId=110381,
        title="Archer (2009)",
        cleanTitle="archer2009",
        monitored=True,
        seasonFolder=True,
        titleSlug="archer-2009",
        profileId=1,
        seasons=(
            models.Season(seasonNumber=5, monitored=True),
            models.Season(seasonNumber=4, monitored=True),
            models.Season(seasonNumber=3, monitored=True),
            models.Season(seasonNumber=2, monitored=True),
            models.Season(seasonNumber=1, monitored=True),
            models.Season(seasonNumber=0, monitored=False),
        ),
        path="T:\\Archer (2009)",
        id=1,
    )

    response = CLIENT.update_series(series)
    assert isinstance(response, models.Series)
    assert len(response.seasons) == 6
    for season in response.seasons:
        assert isinstance(season, models.Season)

    echo = CLIENT._request("echo")
    assert echo == {
        "addOptions": None,
        "added": None,
        "airTime": None,
        "alternateTitles": [],
        "certification": None,
        "cleanTitle": "archer2009",
        "episodeCount": None,
        "episodeFileCount": None,
        "firstAired": None,
        "genres": [],
        "id": 1,
        "images": [],
        "imdbId": None,
        "lastInfoSync": None,
        "monitored": True,
        "network": None,
        "nextAiring": None,
        "overview": None,
        "path": "T:\\Archer (2009)",
        "previousAiring": None,
        "profileId": 1,
        "qualityProfile": None,
        "qualityProfileId": None,
        "ratings": None,
        "remotePoster": None,
        "runtime": None,
        "seasonCount": None,
        "seasonFolder": True,
        "seasons": [
            {"monitored": True, "seasonNumber": 5, "statistics": None},
            {"monitored": True, "seasonNumber": 4, "statistics": None},
            {"monitored": True, "seasonNumber": 3, "statistics": None},
            {"monitored": True, "seasonNumber": 2, "statistics": None},
            {"monitored": True, "seasonNumber": 1, "statistics": None},
            {"monitored": False, "seasonNumber": 0, "statistics": None},
        ],
        "seriesType": None,
        "sizeOnDisk": None,
        "sortTitle": None,
        "status": None,
        "tags": [],
        "title": "Archer (2009)",
        "titleSlug": "archer-2009",
        "totalEpisodeCount": None,
        "tvMazeId": None,
        "tvRageId": None,
        "tvdbId": 110381,
        "useSceneNumbering": None,
        "year": None,
    }


@pytest.fixture
def delete_series_server():
    yield from mock_server(
        uri="/api/series/1", body="{}", method=HttpMethod.DELETE,
    )


def test_delete_series(delete_series_server):
    """Test API call for SonarrClient.delete_series()

    DELETE http://$HOST:8989/api/series/345?deleteFiles=false
    """

    CLIENT.port = delete_series_server.server_port
    response = CLIENT.delete_series(1)
    assert response is None


@pytest.fixture
def lookup_series_server():
    yield from mock_server(
        uri="/api/series/lookup?" + urlencode({"term": "The+Blacklist"}),
        body=SERIESLOOKUP,
        match_query=True,
    )


def test_lookup_series(lookup_series_server):
    """Test API call for SonarrClient.lookup_series()

    GET http://$HOST:8989/api/series/lookup?term=monty+python
    """

    CLIENT.port = lookup_series_server.server_port
    response = CLIENT.lookup_series("The Blacklist")
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Series)
