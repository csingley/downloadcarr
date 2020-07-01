"""
"""
import enum


class MovieStatus(enum.Enum):
    """Possible values to filter RadarrClient.search_cutoff_unmet_movies()
    """
    ALL = {"filterKey": "all", "filterValue": "all"}
    MONITORED = {"filterKey": "monitored", "filterValue": "true"}
    UNMONITORED = {"filterKey": "monitored", "filterValue": "false"}
    AVAILABLE = {"filterKey": "status", "filterValue": "available"}
    RELEASED = {"filterKey": "status", "filterValue": "released"}
    INCINEMAS = {"filterKey": "status", "filterValue": "inCinemas"}
    ANNOUNCED = {"filterKey": "status", "filterValue": "announced"}
