#!/usr/bin/env python3
from cache_tools import CachedBaseHttpSession


# TODO: Schema checking

class LunaSource:

    def __init__(self, api_key: str):
        self._session = CachedBaseHttpSession("LUNA", "https://luna.sch.bme.hu/ezoapi/")
        self._session.headers.update({
            "Authorization": api_key
        })

    def _get_json(self, path: str):
        r = self._session.get(path)
        r.raise_for_status()
        return r.json()

    @property
    def latest_backup(self):
        return self._get_json("latest_backup")

    @property
    def backup_list(self):
        return self._get_json("backup_list")

    @property
    def server_status(self):
        return self._get_json("server_status")

    @property
    def players_data(self):
        return self._get_json("players_data")

    @property
    def is_online(self):  # This refers to Celestia actually
        return self._get_json("is_online")

    @property
    def map_status(self):
        return self._get_json("map_status")
