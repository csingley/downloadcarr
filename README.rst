.. image:: https://github.com/csingley/downloadcarr/raw/master/car-download.png

Python Client for Sonarr, Radarr, etc.
======================================

.. image:: https://travis-ci.org/csingley/downloadcarr.svg?branch=master
    :target: https://travis-ci.org/csingley/downloadcarr

.. image:: https://coveralls.io/repos/github/csingley/downloadcarr/badge.svg?branch=master
    :target: https://coveralls.io/github/csingley/downloadcarr?branch=master

.. image:: https://img.shields.io/badge/python-3.7-brightgreen.svg
    :target: https://www.python.org/dev/peps/pep-0373/

.. image:: https://img.shields.io/badge/dependencies-None-green.svg
    :target: https://github.com/csingley/downloadcarr/blob/master/requirements.txt 


Python client for JSON API provided by Sonarr and its derivatives (Radarr, etc.)

This package targets 100% coverage of the API (GET, POST, PUT, DELETE), with
close alignment between the Python syntax and the JSON API.

Installation
------------
``downloadcarr`` requires Python version 3.7+, and depends only on the standard
libary (no external dependencies).

Usage
-----

.. code-block:: python

    import dataclasses

    from downloadcarr import SonarrClient, RadarrClient

    SONARR_HOST = "192.168.1.100"
    SONARR_API_KEY = "deadbeefdeadbeefdeadbeefdeadbeef"

    RADARR_HOST = "192.168.1.100"
    RADARR_API_KEY = "cafebabecafebabecafebabecafebabe"

    sonarr_client = SonarrClient(SONARR_HOST, SONARR_API_KEY)
    all_series = sonarr_client.get_all_series()
    series = all_series[5]
    series_unmonitored = dataclasses.replace(series, monitored=False)
    sonarr_client.update_series(series_unmonitored)


    radarr_client = RadarrClient(RADARR_HOST, RADARR_API_KEY)
    movies = radarr_client.get_movies()
    movie = movies[-1]
    radarr_client.refresh_movie(movie.id)
    radarr_client.search_cutoff_unmet_movies()
