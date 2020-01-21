#!/usr/bin/env python3
from flask import current_app
from urllib.parse import urljoin

import requests

from functools import wraps

#
# Fogadok egy sörben magammal, hogy ha valami elromlik prodban.... az ebben a fájlban lesz...  -- Marcsello 2020-01-21 01:33
#


class DiscordBot(object):

    def __init__(self):
        self._session = requests.Session()
        self._roles_ilut = {}  # inverse lookup table
        self._app_initialized = False

    def init_app(self, app):  # Configured by Flask
        self._session.headers.update({"Authorization": "Bot {}".format(app.config['DISCORD_BOT_TOKEN'])})
        self._url_base = "https://discordapp.com/api/guilds/{}/".format(app.config['DISCORD_GUILD_ID'])

        self._app_initialized = True

    def __autoinit(func):  # Highly magician thingy

        @wraps(func)
        def call(self, *args, **kwargs):

            if not self._app_initialized:
                self.init_app(current_app)

            return func(self, *args, **kwargs)

        return call

    @__autoinit  # this looks like a snail lol
    def check_membership(self, userid: str) -> bool:
        r = self._session.get(urljoin(self._url_base, "members/{}".format(userid)))

        if r.status_code == 404:
            return False
        elif r.status_code == 200:
            return True
        else:
            r.raise_for_status()

    @__autoinit
    def check_for_role(self, userid: str, rolename: str) -> bool:

        if not self._roles_ilut:
            r = self._session.get(urljoin(self._url_base, "roles?limit=1000"))
            r.raise_for_status()

            roles = r.json

            self._roles_ilut = {role['name']: role['id'] for role in roles}

        if rolename not in self._roles_ilut.keys():
            return False

        r = self._session.get(urljoin(self._url_base, "members/{}".format(userid)))

        if r.status_code == 404:
            return False
        else:
            r.raise_for_status()

        return self._roles_ilut[rolename] in r.json['roles']

    @__autoinit
    def get_members(self) -> list:
        r = self._session.get(urljoin(self._url_base, "members?limit=1000"))
        r.raise_for_status()

        return r.json()  # WTF ?!

    @__autoinit
    def get_members_lut(self) -> dict:

        members = self.get_members()

        return {member['user']['id']: member for member in members}
