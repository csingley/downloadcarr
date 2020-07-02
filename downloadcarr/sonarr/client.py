"""Python client for Sonarr

https://github.com/Sonarr/Sonarr/wiki/API
"""
import json
from typing import Tuple, Optional
from datetime import date

from downloadcarr.client import Client, ArrClientError
from downloadcarr.enums import (
    HttpMethod,
    SortKey,
    SortDirection,
    Protocol,
    ImportMode,
)
from .models import (
    Episode,
    EpisodeFile,
    WantedMissing,
    History,
    QueueItem,
    Tag,
    Series,
    QualityRevision,
    ParseResult,
    QualityAllowedProfile,
    Release,
    Season,
    RootFolder,
    SystemBackup,
)
from downloadcarr.models import (
    CommandStatus,
    Image,
    DiskSpace,
    SystemStatus,
    encode_dict,
)
from downloadcarr.utils import BOOL2JSON


class SonarrClient(Client):
    """Main class for handling connections with Sonarr API."""

    port_default = 8989

    #  https://github.com/Sonarr/Sonarr/wiki/Calendar
    def get_calendar(
        self, start: Optional[date] = None, end: Optional[date] = None
    ) -> Tuple[Episode, ...]:
        """Get upcoming episodes.

        If start/end are not supplied, episodes airing today and tomorrow
        will be returned.

        GET http://$HOST:8989/api/calendar?start=2020-06-13T00%3A00%3A00.000Z&end=2020-06-19T00%3A00%3A00.000Z&unmonitored=false
        """
        query = {}

        if start is not None:
            query["start"] = start.isoformat()

        if end is not None:
            query["end"] = end.isoformat()

        results = self._request("calendar", query=query)
        return tuple(Episode.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Command
    def get_all_commands_status(self) -> Tuple[CommandStatus, ...]:
        """Query the status of all currently started commands.

        NEEDS EXAMPLE
        """
        results = self._request("command")
        return tuple(CommandStatus.from_dict(result) for result in results)

    def get_command_status(self, command_id: int) -> CommandStatus:
        """Query the status of a previously started command.

        NEEDS EXAMPLE
        """
        result = self._request(f"command/{command_id}")
        return CommandStatus.from_dict(result)

    def refresh_all_series(self) -> CommandStatus:
        """Refresh all series information from trakt and rescan disk.

        POST http://$HOST:8989/api/command {"name":"refreshseries"}
        POST http://$HOST:8989/api/command {"name":"RefreshSeries"}
        """
        results = self._post_command("RefreshSeries")
        return results

    def refresh_series(self, seriesId: int) -> CommandStatus:
        """Refresh single series information from trakt and rescan disk.

        POST http://$HOST:8989/api/command {"name":"refreshSeries","seriesId":307}
        """
        results = self._post_command("RefreshSeries", seriesId=seriesId)
        return results

    def rescan_all_series(self) -> CommandStatus:
        """Refresh rescan disk for all series.

        NEEDS EXAMPLE
        """
        results = self._post_command("RescanSeries")
        return results

    def rescan_series(self, seriesId: int) -> CommandStatus:
        """Refresh rescan disk for a single series.

        NEEDS EXAMPLE
        """
        results = self._post_command("RescanSeries", seriesId=seriesId)
        return results

    def search_episodes(self, *episodeIds: int) -> CommandStatus:
        """Search for one or more episodes.

        POST http://$HOST:8989/api/command {"name":"episodeSearch","episodeIds":[19223]}
        """
        results = self._post_command("EpisodeSearch", episodeIds=list(episodeIds))
        return results

    def search_season(self, seriesId: int, seasonNumber: int) -> CommandStatus:
        """Search for all episodes of a particular season.

        POST http://$HOST:8989/api/command {"name":"seasonSearch","seriesId":3,"seasonNumber":5}
        """
        results = self._post_command(
            "SeasonSearch", seriesId=seriesId, seasonNumber=seasonNumber
        )
        return results

    def search_series(self, seriesId: int) -> CommandStatus:
        """Search for all episodes in a series.

        POST http://$HOST:8989/api/command {"name":"seriesSearch","seriesId":3}
        """
        results = self._post_command("SeriesSearch", seriesId=seriesId)
        return results

    def scan_downloaded_episodes(
        self,
        path: str,
        downloadClientId: Optional[str] = None,
        importMode: Optional[ImportMode] = None,
    ) -> CommandStatus:
        """Instruct Sonarr to scan and import the folder defined by the
        path variable set in the POSTed json body.

        A folder specified by the path variable is assumed to be a single
        download (job) and the folder name should be the release name.

        POST http://$HOST:8989/api/command {"name":"DownloadedEpisodesScan"}
        """
        params = {"path": path}
        if downloadClientId is not None:
            params["downloadClientId"] = downloadClientId
        if importMode is not None:
            params["importMode"] = importMode.value

        results = self._post_command("DownloadedEpisodesScan", **params)
        return results

    def sync_rss(self) -> CommandStatus:
        """Instruct Sonarr to perform an RSS sync with all enabled indexers.

        POST http://$HOST:8989/api/command {"name":"RssSync"}
        """
        results = self._post_command("RssSync")
        return results

    def rename_files(self, *files: int) -> CommandStatus:
        """Instruct Sonarr to rename the list of files provided.

        POST http://$HOST:8989/api/command {"name":"renameFiles","seriesId":205,"seasonNumber":-1,"files":[102036,101353,100458,50137,49744,49108,48545,47995,47549,47327,46445]}

        LIVETESTME
        """
        results = self._post_command("RenameFiles", files=list(files))
        return results

    def rename_series(self, *seriesIds: int) -> CommandStatus:
        """Instruct Sonarr to rename all files in the provided series.

        GET http://$HOST:8989/api/rename?seriesId=205
        """
        results = self._post_command("RenameSeries", seriesIds=list(seriesIds))
        return results

    def backup(self) -> CommandStatus:
        """Instruct Sonarr to perform a backup of its database and config file
        (nzbdrone.db and config.xml).

        POST http://$HOST:8989/api/command {"name":"backup","type":"manual"}
        POST http://$HOST:8989/api/command {"name":"Backup"}
        """
        results = self._post_command("Backup")
        return results

    def search_missing_episodes(self) -> CommandStatus:
        """Instruct Sonarr to perform a backlog search of missing episodes
        (Similar functionality to Sickbeard).

        POST http://$HOST:8989/api/command {"name":"missingEpisodeSearch"}
        """
        results = self._post_command("missingEpisodeSearch")
        return results

    #  UNDOCUMENTED COMMANDS
    #  POST http://$HOST:8989/api/command {"name":"ApplicationUpdate"}
    #  POST http://$HOST:8989/api/command {"name":"CheckForFinishedDownload"}
    #  POST http://$HOST:8989/api/command {"name":"CheckHealth"}
    #  POST http://$HOST:8989/api/command {"name":"DownloadedEpisodesScan"}
    #  POST http://$HOST:8989/api/command {"name":"Housekeeping"}
    #  POST http://$HOST:8989/api/command {"name":"MessagingCleanup"}
    #  POST http://$HOST:8989/api/command {"name":"UpdateSceneMapping"}

    #  https://github.com/Sonarr/Sonarr/wiki/Diskspace
    def get_diskspace(self) -> Tuple[DiskSpace, ...]:
        """
        GET http://$HOST:8989/api/diskspace
        """
        results = self._request("diskspace")
        return tuple(DiskSpace.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Episode
    def get_episodes(self, seriesId) -> Tuple[Episode, ...]:
        """Returns all episodes for the given series.

        GET http://$HOST:8989/api/episode?seriesId=3
        """
        query = {"seriesId": seriesId}
        results = self._request("episode", query=query)
        return tuple(Episode.from_dict(result) for result in results)

    def get_episode(self, episodeId: int) -> Episode:
        """Returns the episode with the matching id.

        NEEDS EXAMPLE
        """
        result = self._request(f"episode/{episodeId}")
        return Episode.from_dict(result)

    def update_episode(self, episode: Episode) -> Episode:
        """Update the given episodes.
        Currently only monitored is changed, all other modifications are ignored.

        PUT http://$HOST:8989/api/episode {"seriesId":205,"episodeFileId":46445,"seasonNumber":1,"episodeNumber":1,"title":"The Bone Orchard","airDate":"2017-04-30","airDateUtc":"2017-05-01T01:00:00Z","overview":"When Shadow Moon is released from prison early after the death of his wife, he meets Mr. Wednesday and is recruited as his bodyguard. Shadow discovers that this may be more than he bargained for.","episodeFile":{"seriesId":205,"seasonNumber":1,"relativePath":"Season 1/American Gods - S01E01 - The Bone Orchard WEBDL-720p.mp4","path":"/tank/video/TV/American Gods/Season 1/American Gods - S01E01 - The Bone Orchard WEBDL-720p.mp4","size":2352322048,"dateAdded":"2017-04-30T22:01:17.4243Z","quality":{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"revision":{"version":1,"real":0}},"mediaInfo":{"audioChannels":2,"audioCodec":"AAC","videoCodec":"x264"},"qualityCutoffNotMet":false,"id":46445},"hasFile":true,"monitored":false,"absoluteEpisodeNumber":1,"unverifiedSceneNumbering":false,"id":11937,"status":0}
        """
        data = episode.to_dict()
        result = self._request("episode", method=HttpMethod.PUT, data=data)
        return Episode.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/EpisodeFile
    def get_episode_files(self, seriesId) -> Tuple[EpisodeFile, ...]:
        """Returns all downloaded episode files for the given series.

        GET http://$HOST:8989/api/episodefile?seriesId=112
        """
        query = {"seriesId": seriesId}
        results = self._request("episodefile", query=query)
        return tuple(EpisodeFile.from_dict(result) for result in results)

    def get_episode_file(self, episodeFileId: int) -> EpisodeFile:
        """Returns the episode with the matching id.

        NEEDS EXAMPLE
        """
        result = self._request(f"episodefile/{episodeFileId}")

        return EpisodeFile.from_dict(result)

    def delete_episode_file(self, episodeFileId: int) -> None:
        """Delete the given episode file.

        NEEDS EXAMPLE

        LIVETESTME
        """
        result = self._request(f"episodefile/{episodeFileId}", method=HttpMethod.DELETE)
        if result != {}:
            msg = f"delete_episode_file() returned {result}"
            raise ArrClientError(msg)

    def update_episode_file(
        self, episodeFileId: int, qualityRevision: QualityRevision
    ) -> EpisodeFile:
        """ Updates the quality of the episode file and returns the episode file.

        NEEDS EXAMPLE

        LIVETESTME
        """
        data = {"quality": qualityRevision.to_dict()}
        result = self._request(
            f"episodefile/{episodeFileId}", method=HttpMethod.PUT, data=data
        )
        return EpisodeFile.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/History
    def get_history(
        self,
        sortKey: SortKey = SortKey.DATE,
        page: int = 1,
        pageSize: int = 10,
        sortDir: SortDirection = SortDirection.ASCENDING,
        episodeId: Optional[int] = None,
    ) -> History:
        """Gets history (grabs/failures/completed).
        If provided, episodeId filters to a specific episode ID.

        GET http://$HOST:8989/api/history?page=1&pageSize=15&sortKey=date&sortDir=desc
        GET http://$HOST:8989/api/history?page=1&pageSize=15&sortKey=date&sortDir=desc&episodeId=35

        LIVETESTME
        """
        query = {
            "page": str(page),
            "pageSize": str(pageSize),
            "sortKey": sortKey.value,
            "sortDir": sortDir.value,
        }
        if episodeId is not None:
            query["episodeId"] = episodeId

        result = self._request("history", query=query)
        return History.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/Images
    #   def get_image(self) -> Image:
    #      """FIXME"""
    #      pass

    #  https://github.com/Sonarr/Sonarr/wiki/Wanted-Missing
    def get_wanted_missing(
        self,
        sortKey: SortKey = SortKey.AIRDATE,
        page: int = 1,
        pageSize: int = 10,
        sortDir: SortDirection = SortDirection.ASCENDING,
    ) -> WantedMissing:
        """Get wanted missing episodes.

        GET http://$HOST:8989/api/wanted/missing?page=1&pageSize=15&sortKey=airDateUtc&sortDir=desc&filterKey=monitored&filterValue=true

        LIVETESTME
        """
        query = {
            "page": str(page),
            "pageSize": str(pageSize),
            "sortKey": sortKey.value,
            "sortDir": sortDir.value.replace("ending", ""),  # "asc"/"desc"
        }

        result = self._request("wanted/missing", query=query)
        return WantedMissing.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/Queue
    def get_queue(self) -> Tuple[QueueItem, ...]:
        """Get currently downloading info.

        GET http://$HOST:8989/api/queue?sort_by=timeleft&order=asc

        LIVETESTME
        """
        results = self._request("queue")

        return tuple(QueueItem.from_dict(result) for result in results)

    def delete_queue_item(self, queueItemId, blacklist=False) -> None:
        """Deletes an item from the queue and download client.
        Optionally blacklist item after deletion.

        DELETE http://$HOST:8989/api/queue/1242502863?blacklist=false

        LIVETESTME
        """
        query = {"blacklist": BOOL2JSON[blacklist]}
        result = self._request(
            f"queue/{queueItemId}", method=HttpMethod.DELETE, query=query
        )
        if result != {}:
            msg = f"delete_queue_item() returned {result}"
            raise ArrClientError(msg)

    #  https://github.com/Sonarr/Sonarr/wiki/Parse
    def parse_title(self, title: str) -> Optional[ParseResult]:
        """Returns the result of parsing a title.

        Series and episodes will be returned only if the parsing matches to a
        specific series and one or more episodes.

        NEEDS EXAMPLE

        LIVETESTME
        """
        query = {"title": title}
        try:
            result = self._request("parse", query=query)
            return ParseResult.from_dict(result)
        except json.JSONDecodeError:
            return None

    def parse_path(self, path: str) -> Optional[ParseResult]:
        """Returns the result of parsing a path.

        Series and episodes will be returned only if the parsing matches to a
        specific series and one or more episodes.

        NEEDS EXAMPLE

        LIVETESTME
        """
        query = {"path": path}
        try:
            result = self._request("parse", query=query)
            return ParseResult.from_dict(result)
        except json.JSONDecodeError:
            return None

    #  https://github.com/Sonarr/Sonarr/wiki/Profile
    def get_quality_profiles(self) -> Tuple[QualityAllowedProfile, ...]:
        """Gets all quality profiles.

        GET http://$HOST:8989/api/profile
        """
        results = self._request("profile")
        return tuple(QualityAllowedProfile.from_dict(result) for result in results)

        #  POST http://$HOST:8989/api/profile {"name":"Test","cutoff":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":true},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":true},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":false},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":false},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":false},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":false},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":false},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":false},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":false},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":false},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"}
        #  PUT http://$HOST:8989/api/profile/7 {"id":7,"name":"Test","cutoff":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":true},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":true},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":true},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":false},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":false},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":false},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":false},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":false},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":false},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":false},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"}
        #  DELETE http://$HOST:8989/api/profile/7

    #  https://github.com/Sonarr/Sonarr/wiki/Release
    def get_release(self, episodeId: int) -> Tuple[Release, ...]:
        """
        GET http://$HOST:8989/api/release?episodeId=35&sort_by=releaseWeight&order=asc

        LIVETESTME
        """
        query = {"episodeId": str(episodeId)}
        results = self._request("release", query=query)
        return tuple(Release.from_dict(result) for result in results)

    def add_release(self, guid: str, indexerId: int) -> Tuple[Release, ...]:
        """Adds a previously searched release to the download client,
        if the release is still in Sonarr's search cache (30 minute cache).
        If the release is not found in the cache Sonarr will return a 404.

        NEEDS EXAMPLE

        LIVETESTME
        """
        data = {"guid": guid, "indexerId": indexerId}

        try:
            results = self._request("release", method=HttpMethod.POST, data=data)
        except ArrClientError as err:
            if "404" in err.args[0]:
                msg = f"add_release(): {guid} not found"
                raise ArrClientError(msg)
            else:
                raise

        return tuple(Release.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Release-Push
    def push_release(
        self, title: str, downloadUrl: str, protocol: Protocol, publishDate: date
    ) -> Tuple[Release, ...]:
        """If the title is wanted, Sonarr will grab it.

        NEEDS EXAMPLE

        LIVETESTME
        """
        data = encode_dict(
            {
                "title": title,
                "downloadUrl": downloadUrl,
                "protocol": protocol,
                "publishDate": publishDate,
            }
        )
        results = self._request("release/push", method=HttpMethod.POST, data=data)
        return tuple(Release.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Rootfolder
    def get_rootfolders(self) -> Tuple[RootFolder, ...]:
        """
        GET http://$HOST:8989/api/rootfolder
        """
        results = self._request("rootfolder")
        return tuple(RootFolder.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Series
    def get_all_series(self) -> Tuple[Series, ...]:
        """Return all series.

        GET http://$HOST:8989/api/series?sort_by=sortTitle&order=asc
        """
        results = self._request("series")
        return tuple(Series.from_dict(result) for result in results)

    def get_series(self, seriesId) -> Series:
        """Return the series with the matching ID
        or 404 if no matching series is found.

        NEEDS EXAMPLE
        """
        try:
            result = self._request(f"series/{seriesId}")
        except ArrClientError as err:
            if "404" in err.args[0]:
                msg = f"get_series(): {seriesId} not found"
                raise ArrClientError(msg)
            else:
                raise

        return Series.from_dict(result)

    def add_series(
        self,
        tvdbId: int,
        title: str,
        profileId: int,
        titleSlug: str,
        images: Tuple[Image, ...] = (),
        seasons: Tuple[Season, ...] = (),
        path: Optional[str] = None,
        rootFolderPath: Optional[str] = None,
        tvRageId: Optional[int] = None,
        seasonFolder: bool = True,
        monitored: bool = True,
        ignoreEpisodesWithFiles: bool = False,
        ignoreEpisodesWithoutFiles: bool = False,
        searchForMissingEpisodes: bool = False,
    ) -> Series:
        """Add a new series to your collection.

        POST http://$HOST:8989/api/series {"title":"Monty Python's Flying Circus","sortTitle":"monty pythons flying circus","seasonCount":4,"status":"ended","overview":"And now for something completely different: Monty Python's Flying Circus was simply the most influential comedy program television has ever seen. Five Englishmen, all working under the constraints of conventional TV shows such as The Frost Report (for which the five Englishmen wrote), gathered together with an expatriate American in the spring of 1969 to break the rules. The result, first airing on BBC-1 on October 5, 1969, has influenced countless future men and women in the media and comedy since.","network":"BBC Two","airTime":"22:00","images":[{"coverType":"banner","url":"https://artworks.thetvdb.com/banners/graphical/3412-g.jpg"},{"coverType":"poster","url":"https://artworks.thetvdb.com/banners/posters/75853-5.jpg"},{"coverType":"fanart","url":"https://artworks.thetvdb.com/banners/fanart/original/75853-4.jpg"}],"remotePoster":"https://artworks.thetvdb.com/banners/posters/75853-5.jpg","seasons":[{"seasonNumber":0,"monitored":false},{"seasonNumber":1,"monitored":true},{"seasonNumber":2,"monitored":true},{"seasonNumber":3,"monitored":true},{"seasonNumber":4,"monitored":true}],"year":1969,"profileId":"1","seasonFolder":true,"monitored":true,"useSceneNumbering":false,"runtime":30,"tvdbId":75853,"tvRageId":4522,"tvMazeId":694,"firstAired":"1969-10-05T05:00:00Z","seriesType":"standard","cleanTitle":"montypythonsflyingcircus","imdbId":"tt0063929","titleSlug":"monty-pythons-flying-circus","certification":"TV-14","genres":["Comedy"],"tags":[],"added":"0001-01-01T00:00:00Z","ratings":{"votes":1879,"value":9.6},"qualityProfileId":0,"episodeFileCount":0,"episodeCount":0,"isExisting":false,"rootFolderPath":"/tank/video/TV/","addOptions":{"ignoreEpisodesWithFiles":true,"ignoreEpisodesWithoutFiles":false,"searchForMissingEpisodes":false}}
        """
        if (path or rootFolderPath) is None or (path and rootFolderPath):
            msg = "add_series(): must set exactly one of {path,rootFolderPath}"
            raise ValueError(msg)
        addOptions = {
            "ignoreEpisodesWithFiles": ignoreEpisodesWithFiles,
            "ignoreEpisodesWithoutFiles": ignoreEpisodesWithoutFiles,
            "searchForMissingEpisodes": searchForMissingEpisodes,
        }
        data = {
            "tvdbId": tvdbId,
            "title": title,
            "profileId": profileId,
            "titleSlug": titleSlug,
            "images": list(i.to_dict() for i in images),
            "seasons": list(s.to_dict() for s in seasons),
            "seasonFolder": seasonFolder,
            "monitored": monitored,
            "addOptions": addOptions,
        }

        if path is not None:
            data["path"] = path

        if rootFolderPath is not None:
            data["rootFolderPath"] = rootFolderPath

        if tvRageId is not None:
            data["tvRageId"] = tvRageId

        result = self._request("series", method=HttpMethod.POST, data=data)
        return Series.from_dict(result)

    def update_series(self, series: Series) -> Series:
        """Update an existing series.

        PUT http://$HOST:8989/api/series/113 {"title":"The Corner","alternateTitles":[],"sortTitle":"corner","seasonCount":1,"totalEpisodeCount":6,"episodeCount":0,"episodeFileCount":0,"sizeOnDisk":0,"status":"ended","overview":"Based on the nonfiction book \"The Corner: A Year in the Life of an Inner-City Neighborhood\", by journalists David Simon and Edward Burns, The Corner presents the world of Fayette Street using real names and real events. The Corner tells the true story of men, women and children living amid the open-air drug markets of West Baltimore. It chronicles a year in the lives of 15-year old DeAndre McCullough (Sean Nelson, \"THE WOOD\"), his mother Fran Boyd (Khandi Alexander), and his father Gary McCullough (T.K. Carter), as well as other addicts and low-level drug dealers caught up in the twin-engine economy of heroin and cocaine.","network":"HBO","images":[{"coverType":"banner","url":"/sonarr/MediaCover/113/banner.jpg?lastWrite=637122344761424010"},{"coverType":"poster","url":"/sonarr/MediaCover/113/poster.jpg?lastWrite=636101576081466180"},{"coverType":"fanart","url":"/sonarr/MediaCover/113/fanart.jpg?lastWrite=636101576079066170"}],"seasons":[{"seasonNumber":1,"monitored":true,"statistics":{"episodeFileCount":0,"episodeCount":0,"totalEpisodeCount":6,"sizeOnDisk":0,"percentOfEpisodes":0}}],"year":2000,"path":"/tank/video/TV/The Corner","profileId":"1","seasonFolder":true,"monitored":true,"useSceneNumbering":false,"runtime":60,"tvdbId":76897,"tvRageId":5696,"tvMazeId":5802,"firstAired":"2000-04-16T05:00:00Z","lastInfoSync":"2020-05-20T12:22:31.108946Z","seriesType":"standard","cleanTitle":"thecorner","imdbId":"tt0224853","titleSlug":"the-corner","genres":["Drama","Mini-Series"],"tags":[1],"added":"2016-09-22T16:13:27.620615Z","ratings":{"votes":315,"value":8.5},"qualityProfileId":1,"id":113,"isExisting":false,"statusWeight":3,"profiles":[{"id":1,"name":"Any","cutoff":{"id":1,"name":"SDTV","source":"television","resolution":480},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":true},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":true},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":true},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":true},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":true},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":true},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":true},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":true},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":true},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"},{"id":2,"name":"SD","cutoff":{"id":1,"name":"SDTV","source":"television","resolution":480},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":true},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":true},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":true},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":false},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":false},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":false},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":false},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":false},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":false},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"},{"id":3,"name":"HD-720p","cutoff":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":false},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":false},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":false},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":true},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":false},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":true},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":true},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":false},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":false},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"},{"id":4,"name":"HD-1080p","cutoff":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":false},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":false},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":false},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":false},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":true},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":false},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":false},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":true},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":true},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"},{"id":5,"name":"Ultra-HD","cutoff":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":false},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":false},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":false},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":false},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":false},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":false},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":false},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":false},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":false},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":true},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":true},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":true}],"language":"english"},{"id":6,"name":"HD - 720p/1080p","cutoff":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"items":[{"quality":{"id":0,"name":"Unknown","source":"unknown","resolution":0},"allowed":false},{"quality":{"id":1,"name":"SDTV","source":"television","resolution":480},"allowed":false},{"quality":{"id":8,"name":"WEBDL-480p","source":"web","resolution":480},"allowed":false},{"quality":{"id":2,"name":"DVD","source":"dvd","resolution":480},"allowed":false},{"quality":{"id":4,"name":"HDTV-720p","source":"television","resolution":720},"allowed":true},{"quality":{"id":9,"name":"HDTV-1080p","source":"television","resolution":1080},"allowed":true},{"quality":{"id":10,"name":"Raw-HD","source":"televisionRaw","resolution":1080},"allowed":false},{"quality":{"id":5,"name":"WEBDL-720p","source":"web","resolution":720},"allowed":true},{"quality":{"id":6,"name":"Bluray-720p","source":"bluray","resolution":720},"allowed":true},{"quality":{"id":3,"name":"WEBDL-1080p","source":"web","resolution":1080},"allowed":true},{"quality":{"id":7,"name":"Bluray-1080p","source":"bluray","resolution":1080},"allowed":true},{"quality":{"id":16,"name":"HDTV-2160p","source":"television","resolution":2160},"allowed":false},{"quality":{"id":18,"name":"WEBDL-2160p","source":"web","resolution":2160},"allowed":false},{"quality":{"id":19,"name":"Bluray-2160p","source":"bluray","resolution":2160},"allowed":false}],"language":"english"}]}

        LIVETESTME
        """
        data = series.to_dict()
        result = self._request(f"series/{series.id}", method=HttpMethod.PUT, data=data)
        return Series.from_dict(result)

    def delete_series(self, seriesId: int, deleteFiles: bool = False) -> None:
        """Delete the series with the given ID.

        DELETE http://$HOST:8989/api/series/345?deleteFiles=false
        """
        query = {"deleteFiles": json.dumps(deleteFiles)}
        result = self._request(
            f"series/{seriesId}", method=HttpMethod.DELETE, query=query
        )
        if result != {}:
            msg = f"delete_series() returned {result}"
            raise ArrClientError(msg)

    #  https://github.com/Sonarr/Sonarr/wiki/Series-Lookup
    def lookup_series(self, term: str) -> Tuple[Series, ...]:
        """Searches for new shows on TheTVDB.com
        utilizing sonarr.tv's caching and augmentation proxy.

        GET http://$HOST:8989/api/series/lookup?term=monty+python
        """
        query = {"term": term.replace(" ", "+")}
        results = self._request("series/lookup", query=query)
        return tuple(Series.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/System-Status
    def get_system_status(self) -> SystemStatus:
        """Return system status.

        GET http://$HOST:8989/api/system/status
        """
        result = self._request("system/status")
        return SystemStatus.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/System-Backup
    def get_system_backups(self) -> Tuple[SystemBackup, ...]:
        """Return the list of available backups.

        GET http://$HOST:8989/api/system/backup?sort_by=time&order=desc
        """
        results = self._request("system/backup")
        return tuple(SystemBackup.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Tag
    def get_tags(self) -> Tuple[Tag, ...]:
        """Return all tags.

        GET http://$HOST:8989/api/tag
        """
        results = self._request("tag")
        return tuple(Tag.from_dict(result) for result in results)

    def get_tag(self, tagId: int) -> Tag:
        """Return the tag with the matching ID
        or 404 if no matching tag is found.

        NEEDS EXAMPLE
        """
        try:
            result = self._request(f"tag/{tagId}")
        except ArrClientError as err:
            if "404" in err.args[0]:
                msg = f"get_tag(): {tagId} not found"
                raise ArrClientError(msg)
            else:
                raise

        return Tag.from_dict(result)

    def add_tag(self, label: str) -> Tag:
        """Add a new tag.

        POST http://$HOST:8989/api/tag {"label":"test"}
        """
        data = {"label": label.lower()}
        result = self._request("tag", method=HttpMethod.POST, data=data)
        return Tag.from_dict(result)

    def update_tag(self, tagId: int, label: str) -> Tag:
        """Update an existing tag.

        NEEDS EXAMPLE
        """
        data = {"label": label, "id": tagId}
        result = self._request("tag", method=HttpMethod.PUT, data=data)
        return Tag.from_dict(result)

    def delete_tag(self, tagId: int) -> None:
        """Delete the series with the given ID

        NEEDS EXAMPLE
        """
        result = self._request(f"tag/{tagId}", method=HttpMethod.DELETE)
        if result != {}:
            msg = f"delete_tag() returned {result}"
            raise ArrClientError(msg)

    #  UNDOCUMENTED API
    #  GET http://$HOST:8989/api/blacklist?page=1&pageSize=15&sortKey=date&sortDir=desc
    #  GET http://$HOST:8989/api/health
    #  POST http://$HOST:8989/api/system/restart
    #  GET http://$HOST:8989/api/system/task?sort_by=name&order=asc
    #  GET http://$HOST:8989/api/config/mediamanagement
    #  GET http://$HOST:8989/api/config/naming
    #  GET http://$HOST:8989/api/config/indexer
    #  GET http://$HOST:8989/api/config/downloadclient
    #  GET http://$HOST:8989/api/config/notification
    #  GET http://$HOST:8989/api/config/host
    #  GET http://$HOST:8989/api/config/ui
    #  GET http://$HOST:8989/api/config/naming/samples?renameEpisodes=true&replaceIllegalCharacters=true&multiEpisodeStyle=0&standardEpisodeFormat=%7BSeries+Title%7D+-+S%7Bseason%3A00%7DE%7Bepisode%3A00%7D+-+%7BEpisode+Title%7D+%7BRelease+Group%7D+%7BQuality+Full%7D&dailyEpisodeFormat=%7BSeries+Title%7D+-+%7BAir-Date%7D+-+%7BEpisode+Title%7D+%7BRelease+Group%7D+%7BQuality+Full%7D&animeEpisodeFormat=%7BSeries+Title%7D+-+S%7Bseason%3A00%7DE%7Bepisode%3A00%7D+-+%7BEpisode+Title%7D+%7BRelease+Group%7D+%7BQuality+Full%7D&seriesFolderFormat=%7BSeries+Title%7D&seasonFolderFormat=Season+%7Bseason%3A00%7D&includeSeriesTitle=false&includeEpisodeTitle=false&includeQuality=false&replaceSpaces=true&separator=+-+&numberStyle=S%7Bseason%3A00%7DE%7Bepisode%3A00%7D&id=1
    #  GET http://$HOST:8989/api/delayprofile
    #  GET http://$HOST:8989/api/qualitydefinition
    #  GET http://$HOST:8989/api/indexer
    #  GET http://$HOST:8989/api/Restriction
    #  GET http://$HOST:8989/api/remotePathMapping
    #  GET http://$HOST:8989/api/metadata
    #  GET http://$HOST:8989/api/indexer/test
    #  GET http://$HOST:8989/api/profile/schema
    #  GET http://$HOST:8989/api/update
