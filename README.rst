Python Client for Sonarr, Radarr, etc.
======================================
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

    from downloadcarr import SonarrClient, RadarrClient

    SONARR_HOST = "192.168.1.100"
    SONARR_API_KEY = "deadbeefdeadbeefdeadbeefdeadbeef"

    RADARR_HOST = "192.168.1.100"
    RADARR_API_KEY = "cafebabecafebabecafebabecafebabe"

    series = SonarrClient.get_all_series()
    print(series)

    movies = RadarrClient.get_all_series()
    print(movies)