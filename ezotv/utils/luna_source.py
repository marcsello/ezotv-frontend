#!/usr/bin/env python3
from cache_tools import CachedBaseHttpSession


# TODO: Schema checking

class LunaSource:

    def __init__(self, api_url: str, api_key: str):
        self._session = CachedBaseHttpSession("LUNA", api_url)
        self._session.headers.update({
            "Authorization": api_key
        })

    def _get_json(self, path: str):
        r = self._session.get(path)
        r.raise_for_status()
        return r.json()

    @property
    def latest_backup(self):
        return self._get_json("backups/$latest")

    @property
    def backup_list(self):
        return self._get_json("backups")

    @property
    def server_status(self):
        return self._get_json("status")

    @property
    def players_data(self):
        return self._get_json("playerdata")

    @property
    def map_status(self):
        return self._get_json("maprender")
