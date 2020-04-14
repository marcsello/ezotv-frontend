#!/usr/bin/env python3
import requests
from requests_toolbelt.sessions import BaseUrlSession
import json
from flask import current_app
from urllib.parse import urljoin
from .redis_client import redis_client
import hashlib


# TODO: Schema checking


class LunaSource:

    def __init__(self, api_key: str, cache_timeout: int = 20):
        self._session = BaseUrlSession("https://luna.sch.bme.hu/ezoapi/")
        self._session.headers.update({
            "Authorization": api_key
        })
        self._cache_timeout = cache_timeout

    def _get_cached(self, path: str):
        cached_data = redis_client.get(path)

        if cached_data:
            current_app.logger.debug(f"Cache hit: {path}")
            data = cached_data

        else:
            current_app.logger.debug(f"Cache miss: {path}")
            r = self._session.get(path)
            r.raise_for_status()
            r.json()  # Test if de-serializable

            redis_client.set(path, r.content)
            redis_client.expire(path, self._cache_timeout)
            data = r.content

        return json.loads(data.decode('utf-8'))

    @property
    def latest_backup(self):
        return self._get_cached("latest_backup")

    @property
    def backup_list(self):
        return self._get_cached("backup_list")

    @property
    def server_status(self):
        return self._get_cached("server_status")

    @property
    def players_data(self):
        return self._get_cached("players_data")

    @property
    def is_online(self):  # This refers to Celestia actually
        return self._get_cached("is_online")

    @property
    def map_status(self):
        return self._get_cached("map_status")
