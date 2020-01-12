#!/usr/bin/env python3
import requests
from urllib.parse import urljoin

# TODO: Schema checking


class LunaSource:

    def __init__(self, api_key: str):
        self._session = requests.Session()
        self._url_base = "https://luna.sch.bme.hu/ezoapi/{}/".format(api_key)

    def _from_request(self, path):
        r = self._session.get(urljoin(self._url_base, path))
        r.raise_for_status()

        return r.json()

    @property
    def latest_backup(self):
        return self._from_request("latest_backup")

    @property
    def backup_list(self):
        return self._from_request("backup_list")

    @property
    def server_status(self):
        return self._from_request("server_status")

    @property
    def players_data(self):
        return self._from_request("players_data")

    @property
    def is_online(self):  # This refers to Celestia actually
        return self._from_request("is_online")

    @property
    def map_status(self):  # Bruh...
        r = self._session.get("https://luna.sch.bme.hu/ezotv/map/status.json")  # This is public...
        r.raise_for_status()

        return r.json()


if __name__ == "__main__":
    import os
    import time

    start = time.time()
    l = LunaSource(os.environ['LUNA_API_KEY'])
    print(l.latest_backup)
    print(l.backup_list)
    print(l.server_status)
    print(l.players_data)
    print(l.is_online)
    print(l.map_status)

    print("total:", time.time() - start)
