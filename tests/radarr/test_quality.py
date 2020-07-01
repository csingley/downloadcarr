"""Tests for downloadcarr.radarr.models.quality
"""
import json

import downloadcarr.radarr.models as models

from . import QUEUE


def test_quality() -> None:
    """Test the Quality model."""
    #  instance from /history
    #  instance from /queue
    queue = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    assert isinstance(queue, models.QueueItem)
    qualrev = queue.quality
    assert isinstance(qualrev, models.QualityRevision)
    quality = qualrev.quality
    assert isinstance(quality, models.Quality)
    assert quality.id == 3
    assert quality.name == "WEBDL-1080p"
    assert quality.source == "webdl"
    assert quality.resolution == "r1080P"
    assert quality.modifier == "none"

    movie = queue.movie
    assert isinstance(movie, models.Movie)
    mf = movie.movieFile
    assert isinstance(mf, models.MovieFile)
    qualrev = mf.quality
    assert isinstance(qualrev, models.QualityRevision)
    quality = qualrev.quality
    assert isinstance(quality, models.Quality)
    assert quality.id == 3
    assert quality.name == "WEBDL-1080p"
    assert quality.source == "webdl"
    assert quality.resolution == "r1080P"
    assert quality.modifier == "none"


def test_revision() -> None:
    """Test the Revision model."""
    #  instance from /history
    #  instance from /queue
    queue = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    assert isinstance(queue, models.QueueItem)
    qualrev = queue.quality
    assert isinstance(qualrev, models.QualityRevision)
    revision = qualrev.revision
    assert isinstance(revision, models.Revision)
    assert revision.version == 1
    assert revision.real == 0

    movie = queue.movie
    assert isinstance(movie, models.Movie)
    mf = movie.movieFile
    assert isinstance(mf, models.MovieFile)
    qualrev = mf.quality
    assert isinstance(qualrev, models.QualityRevision)
    revision = qualrev.revision
    assert isinstance(revision, models.Revision)
    assert revision.version == 1
    assert revision.real == 0


def test_quality_revision() -> None:
    """Test the QualityRevision model."""
    #  instance from /history
    #  instance from /queue
    queue = models.QueueItem.from_dict(json.loads(QUEUE)[0])
    assert isinstance(queue, models.QueueItem)
    qualrev = queue.quality
    assert isinstance(qualrev, models.QualityRevision)
    assert isinstance(qualrev.quality, models.Quality)  # tested elsewhere
    assert isinstance(qualrev.customFormats, tuple)
    assert len(qualrev.customFormats) == 0
    assert isinstance(qualrev.revision, models.Revision)  # tested elsewhere

    movie = queue.movie
    assert isinstance(movie, models.Movie)
    mf = movie.movieFile
    assert isinstance(mf, models.MovieFile)
    qualrev = mf.quality
    assert isinstance(qualrev, models.QualityRevision)
    assert isinstance(qualrev.quality, models.Quality)  # tested elsewhere
    assert isinstance(qualrev.customFormats, tuple)
    assert len(qualrev.customFormats) == 0
    assert isinstance(qualrev.revision, models.Revision)  # tested elsewhere
