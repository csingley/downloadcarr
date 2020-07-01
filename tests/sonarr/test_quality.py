"""Tests for Sonarr API /profile endpoint

https://github.com/Sonarr/Sonarr/wiki/Profile
"""
import json

import pytest

import downloadcarr.sonarr.models as models
from downloadcarr.sonarr.client import SonarrClient

from . import (
    EPISODEFILES,
    HISTORY,
    PARSE,
    PROFILE,
    QUEUE,
    RELEASE,
    WANTEDMISSING,
    mock_server,
)


CLIENT = SonarrClient("localhost", "MYKEY")


def test_quality() -> None:
    """Test the Quality model."""
    # instance returned by /episodefile
    ep = models.EpisodeFile.from_dict(json.loads(EPISODEFILES)[0])

    qp = ep.quality
    quality = qp.quality
    assert quality.id == 1
    assert quality.name == "Bluray 720p"

    # instance returned by /history
    hist = models.History.from_dict(json.loads(HISTORY))
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    qual0 = dl0.quality.quality
    assert qual0.id == 3
    assert qual0.name == "WEBDL-1080p"

    qual1 = dl1.quality.quality
    assert qual1.id == 9
    assert qual1.name == "HDTV-1080p"

    # instance returned by /parse
    parsed = models.ParseResult.from_dict(json.loads(PARSE))
    info = parsed.parsedEpisodeInfo
    qualrev = info.quality
    quality = qualrev.quality
    assert quality.id == 4
    assert quality.name == "HDTV-720p"

    # instance returned by /queue
    item = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    qualrev = item.quality
    assert quality.id == 4
    assert quality.name == "HDTV-720p"

    # instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(json.loads(WANTEDMISSING))
    assert len(want.records) == 2
    ep0, ep1 = want.records

    series = ep0.series
    assert isinstance(series, models.Series)
    qp0 = series.qualityProfile
    assert isinstance(qp0, models.QualityProfile)
    qval0 = qp0.value
    assert isinstance(qval0, models.QualityValue)
    allowed = qval0.allowed
    assert isinstance(allowed, tuple)
    assert len(allowed) == 3
    q0, q1, q2 = allowed

    assert q0.id == 1
    assert q0.name == "SDTV"
    assert q0.weight == 1
    assert q1.id == 8
    assert q1.name == "WEBDL-480p"
    assert q1.weight == 2
    assert q2.id == 2
    assert q2.name == "DVD"
    assert q2.weight == 3

    cutoff = qval0.cutoff
    assert cutoff.id == 1
    assert cutoff.name == "SDTV"
    assert cutoff.weight == 1

    series = ep1.series
    assert isinstance(series, models.Series)
    qp1 = series.qualityProfile
    assert isinstance(qp1, models.QualityProfile)
    qval1 = qp1.value
    assert isinstance(qval1, models.QualityValue)
    allowed = qval1.allowed
    assert isinstance(allowed, tuple)
    assert len(allowed) == 3
    q0, q1, q2 = allowed
    assert q0.id == 1
    assert q0.name == "SDTV"
    assert q0.weight == 1
    assert q1.id == 8
    assert q1.name == "WEBDL-480p"
    assert q1.weight == 2
    assert q2.id == 2
    assert q2.name == "DVD"
    assert q2.weight == 3

    cutoff = qval1.cutoff
    assert cutoff.id == 1
    assert cutoff.name == "SDTV"
    assert cutoff.weight == 1

    # instance returned by /profile
    profiles = [
        models.QualityAllowedProfile.from_dict(prof) for prof in json.loads(PROFILE)
    ]
    assert len(profiles) == 4

    # Quality items in each profile are all identical; the differences between
    # them lie in which qualities are allowed for the profile.
    for profile in profiles:
        items = profile.items
        assert isinstance(items, tuple)
        assert len(items) == 10
        qualities = [item.quality for item in items]
        assert qualities[0] == models.Quality(id=1, name="SDTV")
        assert qualities[1] == models.Quality(id=8, name="WEBDL-480p")
        assert qualities[2] == models.Quality(id=2, name="DVD")
        assert qualities[3] == models.Quality(id=4, name="HDTV-720p")
        assert qualities[4] == models.Quality(id=9, name="HDTV-1080p")
        assert qualities[5] == models.Quality(id=10, name="Raw-HD")
        assert qualities[6] == models.Quality(id=5, name="WEBDL-720p")
        assert qualities[7] == models.Quality(id=6, name="Bluray-720p")
        assert qualities[8] == models.Quality(id=3, name="WEBDL-1080p")
        assert qualities[9] == models.Quality(id=7, name="Bluray-1080p")

    cutoffs = [profile.cutoff for profile in profiles]
    assert cutoffs == [
        models.Quality(id=1, name="SDTV"),
        models.Quality(id=4, name="HDTV-720p"),
        models.Quality(id=9, name="HDTV-1080p"),
        models.Quality(id=4, name="HDTV-720p"),
    ]

    # instance returned by /release
    rel = models.Release.from_dict(json.loads(RELEASE)[0])
    quality = rel.quality.quality
    assert quality.id == 4
    assert quality.name == "HDTV-720p"


def test_revision() -> None:
    """Test the Revision model."""
    # instance returned by /history
    hist = models.History.from_dict(json.loads(HISTORY))
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    qualrev0 = dl0.quality
    assert isinstance(qualrev0, models.QualityRevision)
    rev0 = qualrev0.revision
    assert isinstance(rev0, models.Revision)
    assert rev0.version == 1
    assert rev0.real == 0

    qualrev1 = dl1.quality
    assert isinstance(qualrev1, models.QualityRevision)
    rev1 = qualrev1.revision
    assert isinstance(rev1, models.Revision)
    assert rev1.version == 2
    assert rev1.real == 0

    # instance returned by /parse
    parsed = models.ParseResult.from_dict(json.loads(PARSE))
    info = parsed.parsedEpisodeInfo
    qualrev = info.quality
    assert isinstance(qualrev, models.QualityRevision)
    revision = qualrev.revision
    assert isinstance(revision, models.Revision)
    assert revision.version == 1
    assert revision.real == 0

    # instance returned by /queue
    item = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    qualrev = item.quality
    assert isinstance(qualrev, models.QualityRevision)
    revision = qualrev.revision
    assert isinstance(revision, models.Revision)
    assert revision.version == 1
    assert revision.real == 0


def test_quality_revision() -> None:
    """Test the QualityRevision model."""
    # instance returned by /history
    hist = models.History.from_dict(json.loads(HISTORY))
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    qualrev0 = dl0.quality
    assert isinstance(qualrev0.quality, models.Quality)  # tested by test_quality()
    assert isinstance(qualrev0.revision, models.Revision)  # tested by test_revision()

    qualrev1 = dl1.quality
    assert isinstance(qualrev1.quality, models.Quality)  # tested by test_quality()
    assert isinstance(qualrev1.revision, models.Revision)  # tested by test_revision()

    # instance returned by /parse
    parsed = models.ParseResult.from_dict(json.loads(PARSE))
    info = parsed.parsedEpisodeInfo
    qualrev = info.quality
    assert isinstance(qualrev.quality, models.Quality)  # tested by test_quality()
    assert isinstance(qualrev.revision, models.Revision)  # tested by test_revision()

    # instance returned by /queue
    item = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    qualrev = item.quality
    assert isinstance(qualrev.quality, models.Quality)  # tested by test_quality()
    assert isinstance(qualrev.revision, models.Revision)  # tested by test_revision()


def test_quality_value() -> None:
    """Test the QualityValue model."""
    # QualityValue instance returned by /calendar
    pass  # /calendar JSON response (Bob's Burgers S04E11) duplicates /wanted/missing

    # QualityValue instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(json.loads(WANTEDMISSING))
    assert len(want.records) == 2
    ep0, ep1 = want.records

    series = ep0.series
    assert isinstance(series, models.Series)
    qual0 = series.qualityProfile
    assert isinstance(qual0, models.QualityProfile)
    qval0 = qual0.value
    assert qval0.name == "SD"
    allowed = qval0.allowed
    assert isinstance(allowed, tuple)
    for q in allowed:
        assert isinstance(q, models.Quality)  # tested by test_quality()
    cutoff = qval0.cutoff
    assert isinstance(cutoff, models.Quality)  # tested by test_quality()
    assert qval0.id == 1

    series = ep1.series
    assert isinstance(series, models.Series)
    qual1 = series.qualityProfile
    assert isinstance(qual1, models.QualityProfile)
    qval1 = qual1.value
    assert qval1.name == "SD"
    allowed = qval1.allowed
    assert isinstance(allowed, tuple)
    for q in allowed:
        assert isinstance(q, models.Quality)  # tested by test_quality()
    cutoff = qval1.cutoff
    assert isinstance(cutoff, models.Quality)  # tested by test_quality()
    assert qval1.id == 1


def test_quality_profile() -> None:
    """Test the QualityProfile model."""
    # QualityProfile instance returned by /calendar
    pass  # /calendar JSON response (Bob's Burgers S04E11) duplicates /wanted/missing

    # QualityProfile instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(json.loads(WANTEDMISSING))
    assert len(want.records) == 2
    ep0, ep1 = want.records

    series = ep0.series
    assert isinstance(series, models.Series)
    qual0 = series.qualityProfile
    assert isinstance(qual0, models.QualityProfile)
    qval0 = qual0.value
    assert isinstance(qval0, models.QualityValue)  # tested by test_quality_value()
    assert qual0.isLoaded is True

    series = ep1.series
    assert isinstance(series, models.Series)
    qual1 = series.qualityProfile
    assert isinstance(qual1, models.QualityProfile)
    qval1 = qual1.value
    assert isinstance(qval1, models.QualityValue)  # tested by test_quality_value()
    assert qual1.isLoaded is True


#  def test_quality_proper() -> None:
#      """Test the QualityProper model."""
#      # instance returned by /episodefile
#      ep = models.EpisodeFile.from_dict(EPISODEFILES[0])

#      qp = ep.quality
#      assert isinstance(qp.quality, models.Quality)  # tested by test_quality()
#      assert qp.proper is False

#      # instance returned by /release
#      rel = models.Release.from_dict(RELEASE[0])
#      qp = rel.quality
#      assert isinstance(qp.quality, models.Quality)  # tested by test_quality()
#      assert qp.proper is False


def test_quality_allowed() -> None:
    """Test the QualityAllowed model."""
    # instance returned by /profile
    profiles = [
        models.QualityAllowedProfile.from_dict(prof) for prof in json.loads(PROFILE)
    ]
    assert len(profiles) == 4
    prof0, prof1, prof2, prof3 = profiles

    items0 = prof0.items
    assert isinstance(items0, tuple)
    for item in items0:
        assert isinstance(item.quality, models.Quality)  # Tested in test_quality()
    assert len(items0) == 10
    assert [i.allowed for i in items0] == [
        True,
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    ]

    items1 = prof1.items
    assert isinstance(items1, tuple)
    for item in items1:
        assert isinstance(item.quality, models.Quality)  # Tested in test_quality()
    assert len(items1) == 10
    assert [i.allowed for i in items1] == [
        False,
        False,
        False,
        True,
        False,
        False,
        True,
        True,
        False,
        False,
    ]

    items2 = prof2.items
    assert isinstance(items2, tuple)
    for item in items2:
        assert isinstance(item.quality, models.Quality)  # Tested in test_quality()
    assert len(items2) == 10
    assert [i.allowed for i in items2] == [
        False,
        False,
        False,
        False,
        True,
        False,
        False,
        False,
        True,
        True,
    ]

    items3 = prof3.items
    assert isinstance(items3, tuple)
    for item in items3:
        assert isinstance(item.quality, models.Quality)  # Tested in test_quality()
    assert len(items3) == 10
    assert [i.allowed for i in items3] == [
        False,
        False,
        False,
        True,
        True,
        False,
        True,
        True,
        True,
        True,
    ]


def test_quality_allowed_profile() -> None:
    """Test the QualityAllowedProfile model."""
    # instance returned by /profile
    profiles = [
        models.QualityAllowedProfile.from_dict(prof) for prof in json.loads(PROFILE)
    ]
    assert len(profiles) == 4
    prof0, prof1, prof2, prof3 = profiles

    assert prof0.name == "SD"
    assert isinstance(prof0.cutoff, models.Quality)  # tested in test_quality()
    assert prof0.id == 1

    assert prof1.name == "HD 720p"
    assert isinstance(prof1.cutoff, models.Quality)  # tested in test_quality()
    assert prof1.id == 2

    assert prof2.name == "HD 1080p"
    assert isinstance(prof2.cutoff, models.Quality)  # tested in test_quality()
    assert prof2.id == 3

    assert prof3.name == "HD - All"
    assert isinstance(prof3.cutoff, models.Quality)  # tested in test_quality()
    assert prof3.id == 4


@pytest.fixture
def profile_server():
    yield from mock_server(
        uri="/api/profile", body=PROFILE,
    )


def test_get_quality_profiles(profile_server):
    """Test API call for SonarrClient.get_quality_profiles()

    GET http://$HOST:8989/api/profile
    """

    CLIENT.port = profile_server.server_port
    response = CLIENT.get_quality_profiles()
    assert isinstance(response, tuple)
    assert len(response) == 4
    for profile in response:
        assert isinstance(profile, models.QualityAllowedProfile)
