"""Python client for Radarr

https://github.com/Radarr/Radarr/wiki/API
"""
import json
from datetime import date
from typing import Tuple, Optional, Sequence

from downloadcarr.client import Client, ArrClientError
from downloadcarr.models import (
    CommandStatus,
    DiskSpace,
    SystemStatus,
    Image,
)
from downloadcarr.radarr.models import (
    History,
    Movie,
    QueueItem,
)
from downloadcarr.radarr.enums import MovieStatus
from downloadcarr.enums import (
    SortKey,
    SortDirection,
    HttpMethod,
    ImportMode,
)
from downloadcarr.utils import BOOL2JSON


class RadarrClient(Client):
    """Main class for handling connections with Radarr API."""

    port_default = 7878

    #  https://github.com/Radarr/Radarr/wiki/API:Calendar
    def get_calendar(
        self, start: Optional[date] = None, end: Optional[date] = None
    ) -> Tuple[Movie, ...]:
        """Get upcoming movies.

        If start/end are not supplied, episodes airing today and tomorrow
        will be returned.
        """
        query = {}

        if start is not None:
            query["start"] = start.isoformat()

        if end is not None:
            query["end"] = end.isoformat()

        results = self._request("calendar", query=query)
        return tuple(Movie.from_dict(result) for result in results)

    #  https://github.com/Radarr/Radarr/wiki/API:Command
    def get_all_commands_status(self) -> Tuple[CommandStatus, ...]:
        """Query the status of all currently started commands.
        """
        results = self._request("command")
        return tuple(CommandStatus.from_dict(result) for result in results)

    def get_command_status(self, command_id: int) -> CommandStatus:
        """Query the status of a previously started command.
        """
        result = self._request(f"command/{command_id}")
        return CommandStatus.from_dict(result)

    def refresh_movies(self) -> CommandStatus:
        """Refresh all movie information from TMDb and rescan disk.
        """
        results = self._post_command("RefreshMovie")
        return results

    def refresh_movie(self, movieId: int) -> CommandStatus:
        """Refresh single movie information from TMDb and rescan disk.

        POST http://$HOST:7878/api/command {"name":"refreshMovie","movieId":604}
        """
        results = self._post_command("RefreshMovie", movieId=movieId)
        return results

    def rescan_movies(self) -> CommandStatus:
        """Rescan disk for all movies.
        """
        results = self._post_command("RescanMovie")
        return results

    def rescan_movie(self, movieId: int) -> CommandStatus:
        """Rescan disk for single movie.
        """
        results = self._post_command("RescanMovie", movieId=movieId)
        return results

    def search_movies(self, *movieIds: int) -> CommandStatus:
        """Search for one or more movies.
        """
        results = self._post_command("MoviesSearch", movieIds=list(movieIds))
        return results

    def scan_downloaded_movies(
        self,
        path: str,
        downloadClientId: Optional[str] = None,
        importMode: Optional[ImportMode] = None,
    ) -> CommandStatus:
        """Instruct Radarr to scan the DroneFactoryFolder or a folder defined
        by the path variable.  Each file and folder in the DroneFactoryFolder
        is interpreted as separate download.  But a folder specified by the
        path variable is assumed to be a single download (job) and the folder
        name should be the release name.

        The downloadClientId can be used to support this API endpoint in
        conjunction with Completed Download Handling, so Radarr knows that a
        particular download has already been imported.

        LIVETESTME
        """
        params = {"path": path}
        if downloadClientId is not None:
            params["downloadClientId"] = downloadClientId
        if importMode is not None:
            params["importMode"] = importMode.value

        results = self._post_command("DownloadedMoviesScan", **params)
        return results

    def sync_rss(self) -> CommandStatus:
        """Instruct Radarr to perform an RSS sync with all enabled indexers.
        """
        results = self._post_command("RssSync")
        return results

    def rename_files(self, *files: int) -> CommandStatus:
        """Instruct Radarr to rename the list of files provided.

        LIVETESTME
        """
        results = self._post_command("RenameFiles", files=list(files))
        return results

    def rename_movies(self, *movieIds: int) -> CommandStatus:
        """Instruct Radarr to rename all files in the provided movies.

        http://$HOST:7878/api/renameMovie?movieId=604

        LIVETESTME
        """
        results = self._post_command("RenameMovie", movieIds=list(movieIds))
        return results

    def search_cutoff_unmet_movies(
        self, filterBy: MovieStatus = MovieStatus.MONITORED
    ) -> CommandStatus:
        """Instructs Radarr to search all cutoff unmet movies.
        """
        params = filterBy.value
        results = self._post_command("CutOffUnmetMoviesSearch", **params)
        return results

    def sync_net_import(self) -> CommandStatus:
        """Instructs Radarr to search all lists for movies not yet added to Radarr.
        """
        results = self._post_command("NetImportSync")
        return results

    def search_missing_movies(
        self, filterBy: MovieStatus = MovieStatus.MONITORED
    ) -> CommandStatus:
        """Instructs Radarr to search all missing movies.
        This functionality is similar to what CouchPotato does and runs a
        backlog search for all your missing movies.
        """
        params = filterBy.value
        results = self._post_command("missingMoviesSearch", **params)
        return results

    #  https://github.com/Radarr/Radarr/wiki/API:Diskspace
    def get_diskspace(self) -> Tuple[DiskSpace, ...]:
        """
        """
        results = self._request("diskspace")
        return tuple(DiskSpace.from_dict(result) for result in results)

    #  https://github.com/Radarr/Radarr/wiki/API:History
    def get_history(
        self,
        sortKey: SortKey = SortKey.DATE,
        page: int = 1,
        pageSize: int = 10,
        sortDir: SortDirection = SortDirection.ASCENDING,
    ) -> History:
        """Gets history (grabs/failures/completed).

        GET http://$HOST:7878/api/history?page=1&pageSize=15&sortKey=date&sortDir=desc&filterType=equal
        """
        query = {
            "page": str(page),
            "pageSize": str(pageSize),
            "sortKey": sortKey.value,
            "sortDir": sortDir.value,
        }
        result = self._request("history", query=query)
        return History.from_dict(result)

    #  https://github.com/Radarr/Radarr/wiki/API:Movie
    def get_movies(self) -> Tuple[Movie, ...]:
        """Returns all Movies in your collection
        """
        results = self._request("movie")
        return tuple(Movie.from_dict(result) for result in results)

    def get_movie(self, movieId: int) -> Movie:
        """Returns the movie with the matching ID
        or 404 if no matching movie is found
        """
        result = self._request(f"movie/{movieId}")
        return Movie.from_dict(result)

    def add_movie(
        self,
        title: str,
        qualityProfileId: int,
        titleSlug: str,
        tmdbId: int,
        profileId: int,
        year: int,  # release year. Very important needed for the correct path!
        path: str,  # full path to the movie on disk
        images: Sequence[Image] = (),
        monitored: bool = True,
        searchForMovie: bool = False,
    ) -> Movie:
        """Add a new movie to your collection.

        LIVETESTME
        """
        data = {
            "title": title,
            "qualityProfileId": qualityProfileId,
            "titleSlug": titleSlug,
            "images": list(i.to_dict() for i in images),
            "tmdbId": tmdbId,
            "profileId": profileId,
            "year": year,
            "path": path,
            "monitored": monitored,
            "addOptions": {"searchForMovie": searchForMovie},
        }

        result = self._request("movie", method=HttpMethod.POST, data=data)
        return Movie.from_dict(result)

    def update_movie(self, movie: Movie) -> Movie:
        """Update an existing Movie.
        """
        data = movie.to_dict()
        result = self._request(f"movie/{movie.id}", method=HttpMethod.PUT, data=data)
        return Movie.from_dict(result)

    def delete_movie(
        self, movieId: int, deleteFiles: bool = False, addExclusion: bool = False,
    ) -> None:
        """Delete the movie with the given ID.
        """
        query = {
            "deleteFiles": json.dumps(deleteFiles),
            "addExclusion": json.dumps(addExclusion),
        }
        result = self._request(
            f"movie/{movieId}", method=HttpMethod.DELETE, query=query
        )
        if result != {}:
            msg = f"delete_movie() returned {result}"
            raise ArrClientError(msg)

    #  https://github.com/Radarr/Radarr/wiki/API:Movie-Lookup
    def lookup_movie(self, term: str) -> Tuple[Movie, ...]:
        """Searches for new movies on trakt
        """
        query = {"term": term}
        results = self._request("movie/lookup", query=query)
        return tuple(Movie.from_dict(result) for result in results)

    def lookup_movie_tmdb(self, tmdbId: int) -> Tuple[Movie, ...]:
        """Searches for new movies on trakt

        LIVETESTME
        """
        query = {"tmdbId": str(tmdbId)}
        results = self._request("movie/lookup", query=query)
        return tuple(Movie.from_dict(result) for result in results)

    def lookup_movie_imdb(self, imdbId: str) -> Tuple[Movie, ...]:
        """Searches for new movies on trakt

        LIVETESTME
        """
        query = {"imdbId": imdbId}
        results = self._request("movie/lookup", query=query)
        return tuple(Movie.from_dict(result) for result in results)

    #  https://github.com/Radarr/Radarr/wiki/API:Queue
    def get_queue(self) -> Tuple[QueueItem, ...]:
        """Get currently downloading info.

        http://$HOST:7878/api/queue?sort_by=timeleft&order=asc

        LIVETESTME
        """
        results = self._request("queue")

        return tuple(QueueItem.from_dict(result) for result in results)

    def delete_queue_item(self, queueItemId, blacklist=False) -> None:
        """Deletes an item from the queue and download client.
        Optionally blacklist item after deletion.

        LIVETESTME
        """
        query = {"blacklist": BOOL2JSON[blacklist]}
        result = self._request(
            f"queue/{queueItemId}", method=HttpMethod.DELETE, query=query
        )
        if result != {}:
            msg = f"delete_queue_item() returned {result}"
            raise ArrClientError(msg)

    #  https://github.com/Radarr/Radarr/wiki/API:System-Status
    def get_system_status(self) -> SystemStatus:
        """Return system status.
        """
        result = self._request("system/status")
        return SystemStatus.from_dict(result)

    #  UNDOCUMENTED API
    #  http://$HOST:7878/api/config/mediamanagement
    #  http://$HOST:7878/api/config/naming
    #  http://$HOST:7878/api/config/host
    #  http://$HOST:7878/api/notification
    #  http://$HOST:7878/api/config/downloadclient
    #  http://$HOST:7878/api/config/indexer
    #  http://$HOST:7878/api/config/netimport
    #  http://$HOST:7878/api/config/ui
    #  http://$HOST:7878/api/config/naming/samples?renameEpisodes=false&replaceIllegalCharacters=true&colonReplacementFormat=delete&standardMovieFormat=%7BMovie+Title%7D+(%7BRelease+Year%7D)+%7BQuality+Full%7D&movieFolderFormat=%7BMovie+Title%7D+(%7BRelease+Year%7D)&multiEpisodeStyle=0&includeSeriesTitle=false&includeEpisodeTitle=false&includeQuality=false&replaceSpaces=false&id=1
    #  http://$HOST:7878/api/delayprofile
    #  http://$HOST:7878/api/profile
    #  http://$HOST:7878/api/qualitydefinition
    #  http://$HOST:7878/api/customformat
    #  http://$HOST:7878/api/Restriction
    #  http://$HOST:7878/api/customformat/test?title=A.Movie.2018.Directors.Cut.2160p.UHD.BluRay.REMUX.HDR.HEVC.Atmos-EPSiLON&sort_by=matches&order=desc
    #  http://$HOST:7878/api/remotePathMapping
    #  http://$HOST:7878/api/metadata
    #  http://$HOST:7878/api/exclusions
    #  http://$HOST:7878/api/rootfolder
    #  http://$HOST:7878/api/wanted/missing?page=1&pageSize=50&sortKey=title&sortDir=asc&filterKey=monitored&filterValue=true&filterType=equal
    #  http://$HOST:7878/api/wanted/cutoff?page=1&pageSize=50&sortKey=title&sortDir=asc&filterKey=monitored&filterValue=true&filterType=equal
    #  http://$HOST:7878/api/extrafile?movieId=604&sort_by=relativePath&order=asc
    #  DELETE http://$HOST:7878/api/moviefile/575
