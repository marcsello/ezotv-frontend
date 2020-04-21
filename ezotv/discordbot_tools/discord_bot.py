#!/usr/bin/env python3
from urllib.parse import urljoin
from requests_toolbelt.sessions import BaseUrlSession


class DiscordBot(object):

    def __init__(self, bot_token: str, guild_id: str, admin_role_name: str, admin_chat_id: str):
        self._session = BaseUrlSession(f"https://discordapp.com/api/")
        self._session.headers.update({"Authorization": "Bot {}".format(bot_token)})

        self._roles_ilut = {}  # inverse lookup table

        self._admin_role_name = admin_role_name
        self._admin_chat_id = admin_chat_id
        self._guild_id = guild_id

    def check_membership(self, userid: str) -> bool:
        r = self._session.get(f"guilds/{self._guild_id}/members/{userid}")

        if r.status_code == 404:
            return False
        elif r.status_code == 200:
            return True
        else:
            r.raise_for_status()

    def check_for_role(self, userid: str, rolename: str) -> bool:

        if not self._roles_ilut:
            r = self._session.get(f"guilds/{self._guild_id}/roles?limit=1000")
            r.raise_for_status()

            roles = r.json()

            self._roles_ilut = {role['name']: role['id'] for role in roles}

        if rolename not in self._roles_ilut.keys():
            return False

        r = self._session.get(f"guilds/{self._guild_id}/members/{userid}")

        if r.status_code == 404:
            return False
        else:
            r.raise_for_status()

        return self._roles_ilut[rolename] in r.json()['roles']

    def check_is_admin(self, userid: str) -> bool:
        return self.check_for_role(userid, self._admin_role_name)

    def get_members(self) -> list:
        r = self._session.get(f"guilds/{self._guild_id}/members?limit=1000")
        r.raise_for_status()

        return r.json()  # WTF ?!

    def get_members_lut(self) -> dict:

        members = self.get_members()

        return {member['user']['id']: member for member in members}

    def post_log(self, msg: str):
        data = {
            "content": msg,
            "tts": False
        }

        r = self._session.post(f"channels/{self._admin_chat_id}/messages", json=data)
        r.raise_for_status()
