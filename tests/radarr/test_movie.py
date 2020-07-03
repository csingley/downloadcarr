"""Tests for Radarr /movie endpoint.

https://github.com/Radarr/Radarr/wiki/API:Movie
https://github.com/Radarr/Radarr/wiki/API:Movie-Lookup
"""
import json
from datetime import datetime

import pytest

from downloadcarr.models import Image, Rating
import downloadcarr.radarr.models as models
from downloadcarr.radarr.client import RadarrClient
from downloadcarr.enums import HttpMethod
from downloadcarr.utils import UTC
from downloadcarr.client import ArrClientError

from . import (
    CALENDAR,
    MOVIE,
    MOVIES,
    MOVIEPOST,
    MOVIELOOKUP,
    HISTORY,
    QUEUE,
    mock_server,
)


CLIENT = RadarrClient("localhost", "MYKEY")


def test_alternative_title():
    """Test the AlternativeTitle model."""
    #  instance from /calendar
    movie = models.Movie.from_dict(json.loads(CALENDAR)[0])
    assert isinstance(movie, models.Movie)
    assert isinstance(movie.alternativeTitles, tuple)
    assert len(movie.alternativeTitles) == 1
    alt_title = movie.alternativeTitles[0]
    assert isinstance(alt_title, models.AlternativeTitle)
    assert alt_title.sourceType == "tmdb"
    assert alt_title.movieId == 1
    assert alt_title.title == "Resident Evil: Rising"
    assert alt_title.sourceId == 1111
    assert alt_title.votes == 0
    assert alt_title.voteCount == 0
    assert alt_title.language == "english"
    assert alt_title.id == 1

    #  instance from /movie GET
    movie = models.Movie.from_dict(json.loads(MOVIE))
    assert isinstance(movie.alternativeTitles, tuple)
    assert len(movie.alternativeTitles) == 1
    alt_title = movie.alternativeTitles[0]
    assert isinstance(alt_title, models.AlternativeTitle)
    assert alt_title.sourceType == "tmdb"
    assert alt_title.movieId == 1
    assert alt_title.title == "Assassin's Creed: The IMAX Experience"
    assert alt_title.sourceId == 1111
    assert alt_title.votes == 0
    assert alt_title.voteCount == 0
    assert alt_title.language == "english"
    assert alt_title.id == 1

    #  instance from /queue
    queue = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    assert isinstance(queue, models.QueueItem)
    movie = queue.movie
    assert isinstance(movie, models.Movie)
    assert isinstance(movie.alternativeTitles, tuple)
    assert len(movie.alternativeTitles) == 1
    title = movie.alternativeTitles[0]
    assert isinstance(title, models.AlternativeTitle)
    assert title.sourceType == "tmdb"
    assert title.movieId == 16
    assert title.title == "Mowgli"
    assert title.sourceId == 407436
    assert title.votes == 0
    assert title.voteCount == 0
    assert title.language == "english"
    assert title.id == 21


def test_movie_file():
    """Test the MovieFile model."""
    #  instance from /queue
    queue = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    assert isinstance(queue, models.QueueItem)
    movie = queue.movie
    assert isinstance(movie, models.Movie)
    mf = movie.movieFile
    assert mf.movieId == 0
    assert mf.relativePath == "Mowgli (2018) Web-Dl 1080p x264 AC3-NoTag.mkv"
    assert mf.size == 2948099499
    assert mf.dateAdded == datetime(2019, 8, 16, 8, 52, 55, 490036, tzinfo=UTC)
    assert mf.releaseGroup == "NoTag"
    assert isinstance(mf.quality, models.QualityRevision)  # tested elsewhere
    assert mf.edition == ""
    assert mf.id == 4


def test_movie():
    """Test the Movie model."""
    #  instance from /movie GET
    movie = models.Movie.from_dict(json.loads(MOVIE))
    assert isinstance(movie, models.Movie)
    assert movie.title == "Assassin's Creed"
    assert movie.sortTitle == "assassins creed"
    assert movie.sizeOnDisk == 0
    assert movie.status == "released"
    assert movie.overview == (
        "Lynch discovers he is a descendant of the secret Assassins society "
        "through unlocked genetic memories that allow him to relive the "
        "adventures of his ancestor, Aguilar, in 15th Century Spain. After "
        "gaining incredible knowledge and skills he’s poised to take on the "
        "oppressive Knights Templar in the present day."
    )
    assert movie.inCinemas == datetime(2016, 12, 21, tzinfo=UTC)
    assert isinstance(movie.images, tuple)
    assert len(movie.images) == 2
    for image in movie.images:
        assert isinstance(
            image, Image
        )  # Image tested in downloadcarr.tests.models-common
    assert movie.website == "https://www.ubisoft.com/en-US/"
    assert movie.downloaded is False
    assert movie.year == 2016
    assert movie.hasFile is False
    assert movie.youTubeTrailerId == "pgALJgMjXN4"
    assert movie.studio == "20th Century Fox"
    assert movie.path == "/path/to/Assassin's Creed (2016)"
    assert movie.profileId == 6
    assert movie.monitored is True
    assert movie.minimumAvailability == "preDb"
    assert movie.runtime == 115
    assert movie.lastInfoSync == datetime(2017, 1, 23, 22, 5, 32, 365337, tzinfo=UTC)
    assert movie.cleanTitle == "assassinscreed"
    assert movie.imdbId == "tt2094766"
    assert movie.tmdbId == 121856
    assert movie.titleSlug == "assassins-creed-121856"
    assert isinstance(movie.genres, tuple)
    assert len(movie.genres) == 4
    assert movie.genres[0] == "Action"
    assert movie.genres[1] == "Adventure"
    assert movie.genres[2] == "Fantasy"
    assert movie.genres[3] == "Science Fiction"
    assert isinstance(movie.tags, tuple)
    assert len(movie.tags) == 0
    assert movie.added == datetime(2017, 1, 14, 20, 18, 52, 938244, tzinfo=UTC)
    assert isinstance(
        movie.ratings, Rating
    )  # Rating tested in downloadcarr.tests.models-common
    assert isinstance(movie.alternativeTitles, tuple)
    assert len(movie.alternativeTitles) == 1
    assert isinstance(movie.alternativeTitles[0], models.AlternativeTitle)
    assert movie.qualityProfileId == 6
    assert movie.id == 1

    #  instance from /movie POST
    movie = models.Movie.from_dict(json.loads(MOVIEPOST))
    assert isinstance(movie, models.Movie)
    assert movie.title == "Minions (2015)"
    assert movie.sortTitle == "minions 2015"
    assert movie.sizeOnDisk == 0
    assert movie.status == "tba"
    assert isinstance(movie.images, tuple)
    assert len(movie.images) == 2
    for image in movie.images:
        assert isinstance(
            image, Image
        )  # Image tested in downloadcarr.tests.models-common
    assert movie.downloaded is False
    assert movie.year == 0
    assert movie.hasFile is False
    assert movie.path == "/path/to/Minions (2015)"
    assert movie.profileId == 6
    assert movie.monitored is True
    assert movie.minimumAvailability == "preDb"
    assert movie.runtime == 0
    assert movie.cleanTitle == "minions2015"
    assert movie.imdbId == "tt2293640"
    assert movie.tmdbId == 211672
    assert movie.titleSlug == "minions-211672"
    assert isinstance(movie.genres, tuple)
    assert len(movie.genres) == 0
    assert isinstance(movie.tags, tuple)
    assert len(movie.tags) == 0
    assert movie.added == datetime(2017, 1, 24, 14, 26, 55, 165661, tzinfo=UTC)
    assert isinstance(movie.alternativeTitles, tuple)
    assert len(movie.alternativeTitles) == 0
    assert movie.qualityProfileId == 6
    assert movie.id == 11

    #  #  instance from /movie/lookup
    movie = models.Movie.from_dict(json.loads(MOVIELOOKUP)[0])
    assert isinstance(movie, models.Movie)
    assert movie.title == "Star Wars"
    assert isinstance(movie.alternativeTitles, tuple)
    assert len(movie.alternativeTitles) == 0
    assert movie.sortTitle == "star wars"
    assert movie.sizeOnDisk == 0
    assert movie.status == "released"
    assert movie.overview == (
        "Princess Leia is captured and held hostage by the evil Imperial "
        "forces in their effort to take over the galactic Empire. Venturesome "
        "Luke Skywalker and dashing captain Han Solo team together with the "
        "loveable robot duo R2-D2 and C-3PO to rescue the beautiful princess "
        "and restore peace and justice in the Empire."
    )
    assert movie.inCinemas == datetime(1977, 5, 25, tzinfo=UTC)
    assert isinstance(movie.images, tuple)
    assert len(movie.images) == 1
    assert isinstance(
        movie.images[0], Image
    )  # Image tested in downloadcarr.tests.models-common
    assert movie.downloaded is False
    assert (
        movie.remotePoster
        == "http://image.tmdb.org/t/p/original/btTdmkgIvOi0FFip1sPuZI2oQG6.jpg"
    )
    assert movie.year == 1977
    assert movie.hasFile is False
    assert movie.profileId == 0
    assert movie.pathState == "dynamic"
    assert movie.monitored is False
    assert movie.minimumAvailability == "tba"
    assert movie.isAvailable is True
    assert movie.folderName == ""
    assert movie.runtime == 0
    assert movie.tmdbId == 11
    assert movie.titleSlug == "star-wars-11"
    assert isinstance(movie.genres, tuple)
    assert len(movie.genres) == 0
    assert isinstance(movie.tags, tuple)
    assert len(movie.tags) == 0
    assert movie.added == datetime(1, 1, 1, tzinfo=UTC)
    assert isinstance(
        movie.ratings, Rating
    )  # Rating tested in downloadcarr.tests.models-common
    assert movie.qualityProfileId == 0

    #  #  instance from /history
    history = models.History.from_dict(json.loads(HISTORY))
    assert isinstance(history.records, tuple)
    assert len(history.records) == 1
    dl = history.records[0]
    assert isinstance(dl, models.Download)
    movie = dl.movie
    assert isinstance(movie, models.Movie)
    assert movie.title == "Minions"
    assert movie.sortTitle == "minions"
    assert movie.sizeOnDisk == 0
    assert movie.status == "released"
    assert (
        movie.overview
        == "Minions Stuart, Kevin and Bob are recruited by Scarlet Overkill, a super-villain who, alongside her inventor husband Herb, hatches a plot to take over the world."
    )
    assert movie.inCinemas == datetime(2015, 6, 17, tzinfo=UTC)
    assert len(movie.images) == 2
    for image in movie.images:
        assert isinstance(
            image, Image
        )  # Image tested in downloadcarr.tests.models-common
    assert movie.website == "http://www.minionsmovie.com/"
    assert movie.downloaded is False
    assert movie.year == 2015
    assert movie.hasFile is False
    assert movie.youTubeTrailerId == "jc86EFjLFV4"
    assert movie.studio == "Universal Pictures"
    assert movie.path == "/path/to/Minions (2015)"
    assert movie.profileId == 3
    assert movie.monitored is True
    assert movie.runtime == 91
    assert movie.lastInfoSync == datetime(2017, 1, 24, 14, 57, 0, 765931, tzinfo=UTC)
    assert movie.cleanTitle == "minions"
    assert movie.imdbId == "tt2293640"
    assert movie.tmdbId == 211672
    assert movie.titleSlug == "minions-2015"
    assert isinstance(movie.genres, tuple)
    assert len(movie.genres) == 4
    assert movie.genres[0] == "Family"
    assert movie.genres[1] == "Animation"
    assert movie.genres[2] == "Adventure"
    assert movie.genres[3] == "Comedy"
    assert isinstance(movie.tags, tuple)
    assert len(movie.tags) == 0
    assert movie.added == datetime(
        2017, 1, 24, 14, 57, 0, 425430, tzinfo=UTC
    )  # right-pad zeros
    assert isinstance(
        movie.ratings, Rating
    )  # Rating tested in downloadcarr.tests.models_common
    assert isinstance(movie.alternativeTitles, tuple)
    assert len(movie.alternativeTitles) == 0
    assert movie.qualityProfileId == 3
    assert movie.id == 13

    #  instance from /queue
    queue = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    assert isinstance(queue, models.QueueItem)
    movie = queue.movie
    assert isinstance(movie, models.Movie)
    assert movie.title == "Mowgli"
    assert isinstance(movie.alternativeTitles, tuple)
    assert len(movie.alternativeTitles) == 1
    assert isinstance(
        movie.alternativeTitles[0], models.AlternativeTitle
    )  # tested in test_alternative_title()
    assert movie.secondaryYearSourceId == 0
    assert movie.sortTitle == "mowgli"
    assert movie.sizeOnDisk == 2948099499
    assert movie.status == "released"
    assert movie.overview == "Mowgli lives in the jungle. Nice movie."
    assert movie.inCinemas == datetime(2018, 11, 24, 23, tzinfo=UTC)
    assert movie.physicalRelease == datetime(2018, 12, 7, tzinfo=UTC)
    assert movie.physicalReleaseNote == "Netflix"
    assert isinstance(movie.images, tuple)
    assert len(movie.images) == 2
    for img in movie.images:
        assert isinstance(img, Image)  # tested elsewhere
    assert movie.website == "https://www.netflix.com/title/80993105"
    assert movie.downloaded is True
    assert movie.year == 2018
    assert movie.hasFile is True
    assert movie.youTubeTrailerId == "ZZGQ0zftr-w"
    assert movie.studio == "The Imaginarium"
    assert movie.path == "/storage/movies/Mowgli (2018)"
    assert movie.profileId == 4
    assert movie.pathState == "static"
    assert movie.monitored is False
    assert movie.minimumAvailability == "released"
    assert movie.isAvailable is True
    assert movie.folderName == "/storage/movies/Mowgli (2018)"
    assert movie.runtime == 104
    assert movie.lastInfoSync == datetime(2019, 8, 12, 15, 34, 21, 823878, tzinfo=UTC)
    assert movie.cleanTitle == "mowgli"
    assert movie.imdbId == "tt2388771"
    assert movie.tmdbId == 407436
    assert movie.titleSlug == "mowgli-407436"
    assert isinstance(movie.genres, tuple)
    assert len(movie.genres) == 0
    assert isinstance(movie.tags, tuple)
    assert len(movie.tags) == 1
    assert movie.tags[0] == 1
    assert movie.added == datetime(2019, 8, 12, 15, 34, 18, 737789, tzinfo=UTC)
    assert isinstance(movie.ratings, Rating)  # tested elsewhere
    assert isinstance(movie.movieFile, models.MovieFile)  # tested elsewhere
    assert movie.qualityProfileId == 4
    assert movie.id == 16

    # instance from /calendar
    movie = models.Movie.from_dict(json.loads(CALENDAR)[0])
    assert movie.title == "Resident Evil: The Final Chapter"
    assert movie.sortTitle == "resident evil final chapter"
    assert movie.sizeOnDisk == 0
    assert movie.status == "announced"
    assert movie.overview == (
        "Alice, Jill, Claire, Chris, Leon, Ada, and Wesker rush to The Hive, "
        "where The Red Queen plots total destruction over the human race."
    )
    assert movie.inCinemas == datetime(2017, 1, 25, tzinfo=UTC)
    assert movie.physicalRelease == datetime(2017, 1, 27, tzinfo=UTC)
    assert isinstance(movie.images, tuple)
    assert len(movie.images) == 2
    for image in movie.images:
        assert isinstance(image, Image)  # tested elsewhere
    assert movie.website == ""
    assert movie.downloaded is False
    assert movie.year == 2017
    assert movie.hasFile is False
    assert movie.youTubeTrailerId == "B5yxr7lmxhg"
    assert movie.studio == "Impact Pictures"
    assert movie.path == "/path/to/Resident Evil The Final Chapter (2017)"
    assert movie.profileId == 3
    assert movie.monitored is False
    assert movie.runtime == 106
    assert movie.lastInfoSync == datetime(2017, 1, 24, 14, 52, 40, 315434, tzinfo=UTC)
    assert movie.cleanTitle == "residentevilfinalchapter"
    assert movie.imdbId == "tt2592614"
    assert movie.tmdbId == 173897
    assert movie.titleSlug == "resident-evil-the-final-chapter-2017"
    assert isinstance(movie.genres, tuple)
    assert len(movie.genres) == 3
    assert movie.genres[0] == "Action"
    assert movie.genres[1] == "Horror"
    assert movie.genres[2] == "Science Fiction"
    assert isinstance(movie.tags, tuple)
    assert len(movie.tags) == 0
    assert movie.added == datetime(2017, 1, 24, 14, 52, 39, 989964, tzinfo=UTC)
    assert isinstance(movie.ratings, Rating)
    assert movie.ratings.votes == 363
    assert movie.ratings.value == 4.3
    assert isinstance(movie.alternativeTitles, tuple)
    assert len(movie.alternativeTitles) == 1
    assert isinstance(movie.alternativeTitles[0], models.AlternativeTitle)
    assert movie.qualityProfileId == 3
    assert movie.id == 12


@pytest.fixture
def movies_server():
    yield from mock_server(
        uri="/api/movie", body=MOVIES,
    )


def test_get_movies(movies_server):
    """Test API call for RadarrClient.get_movies()
    """

    CLIENT.port = movies_server.server_port
    response = CLIENT.get_movies()
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Movie)


@pytest.fixture
def movie_server():
    yield from mock_server(
        uri="/api/movie/1", body=MOVIE,
    )


def test_get_movie(movie_server):
    """Test API call for RadarrClient.get_movie()
    """

    CLIENT.port = movie_server.server_port
    response = CLIENT.get_movie(1)
    assert isinstance(response, models.Movie)


@pytest.fixture
def add_movie_server():
    yield from mock_server(
        uri="/api/movie", body=MOVIEPOST, method=HttpMethod.POST, echo=True,
    )


def test_add_movie(add_movie_server):
    """Test API call for RadarrClient.add_movie()
    """

    CLIENT.port = add_movie_server.server_port
    movie = models.Movie.from_dict(json.loads(MOVIEPOST))
    response = CLIENT.add_movie(
        movie=movie, qualityProfileId=6, profileId=6, path="/path/to/Minions (2015)",
    )
    assert isinstance(response, models.Movie)

    echo = CLIENT._request("echo")
    assert echo == {
        "title": "Minions (2015)",
        "images": [
            {"coverType": "poster", "url": "/radarr/MediaCover/11/poster.jpg"},
            {"coverType": "banner", "url": "/radarr/MediaCover/11/banner.jpg"},
        ],
        "year": 0,
        "path": "/path/to/Minions (2015)",
        "profileId": 6,
        "monitored": True,
        "tmdbId": 211672,
        "titleSlug": "minions-211672",
        "qualityProfileId": 6,
        "addOptions": {"searchForMovie": False},
    }


@pytest.fixture
def update_movie_echo_server():
    yield from mock_server(
        uri="/api/movie/1", body=MOVIE, method=HttpMethod.PUT, echo=True,
    )


def test_update_movie(update_movie_echo_server):
    """Test API call for RadarrClient.update_movie()
    """
    CLIENT.port = update_movie_echo_server.server_port
    movie = models.Movie(
        title="Assassin's Creed",
        sortTitle="assassins creed",
        sizeOnDisk=0,
        status="released",
        overview="Lynch discovers he is a descendant of the secret Assassins society through unlocked genetic memories that allow him to relive the adventures of his ancestor, Aguilar, in 15th Century Spain. After gaining incredible knowledge and skills he’s poised to take on the oppressive Knights Templar in the present day.",
        inCinemas=datetime(2016, 12, 21, tzinfo=UTC),
        images=(
            Image(
                coverType="poster",
                url="/radarr/MediaCover/1/poster.jpg?lastWrite=636200219330000000",
            ),
            Image(
                coverType="banner",
                url="/radarr/MediaCover/1/banner.jpg?lastWrite=636200219340000000",
            ),
        ),
        website="https://www.ubisoft.com/en-US/",
        downloaded=False,
        year=2016,
        hasFile=False,
        youTubeTrailerId="pgALJgMjXN4",
        studio="20th Century Fox",
        path="/path/to/Assassin's Creed (2016)",
        profileId=6,
        monitored=True,
        minimumAvailability="preDb",
        runtime=115,
        lastInfoSync=datetime(2017, 1, 23, 22, 5, 32, 365337, tzinfo=UTC),
        cleanTitle="assassinscreed",
        imdbId="tt2094766",
        tmdbId=121856,
        titleSlug="assassins-creed-121856",
        genres=("Action", "Adventure", "Fantasy", "Science Fiction"),
        added=datetime(2017, 1, 14, 20, 18, 52, 938244, tzinfo=UTC),
        ratings=Rating(votes=711, value=5.2),
        #  alternativeTitles=("Assassin's Creed: The IMAX Experience", ),
        alternativeTitles=(
            models.AlternativeTitle(
                sourceType="tmdb",
                movieId=1,
                title="Assassin's Creed: The IMAX Experience",
                sourceId=1111,
                votes=0,
                voteCount=0,
                language="english",
                id=1,
            ),
        ),
        qualityProfileId=6,
        id=1,
    )

    response = CLIENT.update_movie(movie)
    assert isinstance(response, models.Movie)

    echo = CLIENT._request("echo")
    assert echo == {
        "title": "Assassin's Creed",
        "sortTitle": "assassins creed",
        "sizeOnDisk": 0,
        "status": "released",
        "overview": "Lynch discovers he is a descendant of the secret Assassins society through unlocked genetic memories that allow him to relive the adventures of his ancestor, Aguilar, in 15th Century Spain. After gaining incredible knowledge and skills he’s poised to take on the oppressive Knights Templar in the present day.",
        "inCinemas": "2016-12-21T00:00:00Z",
        "images": [
            {
                "coverType": "poster",
                "url": "/radarr/MediaCover/1/poster.jpg?lastWrite=636200219330000000",
            },
            {
                "coverType": "banner",
                "url": "/radarr/MediaCover/1/banner.jpg?lastWrite=636200219340000000",
            },
        ],
        "website": "https://www.ubisoft.com/en-US/",
        "downloaded": False,
        "year": 2016,
        "hasFile": False,
        "youTubeTrailerId": "pgALJgMjXN4",
        "studio": "20th Century Fox",
        "path": "/path/to/Assassin's Creed (2016)",
        "profileId": 6,
        "monitored": True,
        "minimumAvailability": "preDb",
        "runtime": 115,
        "lastInfoSync": "2017-01-23T22:05:32.365337Z",
        "cleanTitle": "assassinscreed",
        "imdbId": "tt2094766",
        "tmdbId": 121856,
        "titleSlug": "assassins-creed-121856",
        "genres": ["Action", "Adventure", "Fantasy", "Science Fiction"],
        "tags": [],
        "added": "2017-01-14T20:18:52.938244Z",
        "ratings": {"votes": 711, "value": 5.2},
        "alternativeTitles": [
            {
                "sourceType": "tmdb",
                "movieId": 1,
                "title": "Assassin's Creed: The IMAX Experience",
                "sourceId": 1111,
                "votes": 0,
                "voteCount": 0,
                "language": "english",
                "id": 1,
            },
        ],
        "qualityProfileId": 6,
        "id": 1,
        "secondaryYearSourceId": None,
        "remotePoster": None,
        "pathState": None,
        "isAvailable": None,
        "folderName": None,
        "movieFile": None,
        "physicalRelease": None,
        "physicalReleaseNote": None,
        "secondaryYear": None,
    }


@pytest.fixture
def delete_movie_server():
    yield from mock_server(
        uri="/api/movie/1", body="{}", method=HttpMethod.DELETE,
    )


def test_delete_movie(delete_movie_server):
    """Test API call for RadarrClient.delete_movie()
    """

    CLIENT.port = delete_movie_server.server_port
    response = CLIENT.delete_movie(1)
    assert response is None


@pytest.fixture
def delete_movie_bad_server():
    yield from mock_server(
        uri="/api/movie/1", body="[1, 2, 3]", method=HttpMethod.DELETE,
    )


def test_delete_movie_bad(delete_movie_bad_server):
    """RadarrClient.delete_movie() raises error if return value
    isn't empty JSON array.
    """

    CLIENT.port = delete_movie_bad_server.server_port
    with pytest.raises(ArrClientError):
        CLIENT.delete_movie(1)


@pytest.fixture
def lookup_movie_server():
    yield from mock_server(
        uri="/api/movie/lookup?term=Star%20Wars", body=MOVIELOOKUP, match_query=True,
    )


def test_lookup_movie(lookup_movie_server):
    """Test API call for RadarrClient.lookup_movie()
    """

    CLIENT.port = lookup_movie_server.server_port
    response = CLIENT.lookup_movie("Star Wars")
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Movie)


@pytest.fixture
def lookup_movie_tmdb_server():
    yield from mock_server(
        uri="/api/movie/lookup?tmdbId=348350", body=MOVIELOOKUP, match_query=True,
    )


def test_lookup_movie_tmdb(lookup_movie_tmdb_server):
    """Test API call for RadarrClient.lookup_movie_tmdb()
    """

    CLIENT.port = lookup_movie_tmdb_server.server_port
    response = CLIENT.lookup_movie_tmdb("348350")
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Movie)


@pytest.fixture
def lookup_movie_imdb_server():
    yield from mock_server(
        uri="/api/movie/lookup?imdbId=tt3778644", body=MOVIELOOKUP, match_query=True,
    )


def test_lookup_movie_imdb(lookup_movie_imdb_server):
    """Test API call for RadarrClient.lookup_movie_imdb()
    """

    CLIENT.port = lookup_movie_imdb_server.server_port
    response = CLIENT.lookup_movie_imdb("tt3778644")
    assert isinstance(response, tuple)
    assert len(response) == 1
    assert isinstance(response[0], models.Movie)
