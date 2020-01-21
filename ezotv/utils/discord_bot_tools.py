#!/usr/bin/env python3
from flask import current_app, _app_ctx_stack
from urllib.parse import urljoin

import requests

from functools import wraps

#
# Fogadok egy sörben magammal, hogy ha valami elromlik prodban.... az ebben a fájlban lesz...  -- Marcsello 2020-01-21 01:33
#


class DiscordBot(object):

    def __init__(self, bot_token: str, guild_id: str):
        self._session = requests.Session()
        self._session.headers.update({"Authorization": "Bot {}".format(bot_token)})
        self._url_base = "https://discordapp.com/api/guilds/{}/".format(guild_id)
        self._roles_ilut = {}  # inverse lookup table

    def check_membership(self, userid: str) -> bool:
        r = self._session.get(urljoin(self._url_base, "members/{}".format(userid)))

        if r.status_code == 404:
            return False
        elif r.status_code == 200:
            return True
        else:
            r.raise_for_status()

    def check_for_role(self, userid: str, rolename: str) -> bool:

        if not self._roles_ilut:
            r = self._session.get(urljoin(self._url_base, "roles?limit=1000"))
            r.raise_for_status()

            roles = r.json()

            self._roles_ilut = {role['name']: role['id'] for role in roles}

        if rolename not in self._roles_ilut.keys():
            return False

        r = self._session.get(urljoin(self._url_base, "members/{}".format(userid)))

        if r.status_code == 404:
            return False
        else:
            r.raise_for_status()

        return self._roles_ilut[rolename] in r.json()['roles']

    def get_members(self) -> list:
        r = self._session.get(urljoin(self._url_base, "members?limit=1000"))
        r.raise_for_status()

        return r.json()  # WTF ?!

    def get_members_lut(self) -> dict:

        members = self.get_members()

        return {member['user']['id']: member for member in members}


class FlaskDiscordBot(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):  # Configured by Flask
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'discordbot'):
            del ctx.discordbot

    @property
    def instance(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'discordbot'):
                ctx.discordbot = DiscordBot(current_app.config['DISCORD_BOT_TOKEN'], current_app.config['DISCORD_GUILD_ID'])
            return ctx.discordbot


# Meme
discord_bot = FlaskDiscordBot()
