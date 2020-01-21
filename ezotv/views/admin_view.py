#!/usr/bin/env python3
from flask import request, abort, render_template, current_app, redirect, url_for, flash
from flask_classful import FlaskView, route

from flask_login import login_required, current_user, logout_user

from urllib.parse import urljoin, quote

from model import db, User, NameChange
from utils import DiscordBot


class AdminView(FlaskView):

    route_prefix = "/dashboard/"

    discord_bot = DiscordBot()
    decorators = [login_required]

    def index(self):

        members_lut = self.discord_bot.get_members_lut()

        name_changes = NameChange.query.all()
        extra_info = {}

        for name_change in name_changes:

            discord_id = name_change.user.discord_id

            if discord_id in members_lut.keys():

                extra_info[name_change.id] = {
                    "discord_tag": "{}#{}".format(members_lut[discord_id]['user']['username'], members_lut[discord_id]['user']['discriminator']),
                    "discord_membership": True,
                    "discord_guild_joined": members_lut[discord_id]['joined_at']  # Ebbe bele kellene verni a gecit
                }

            else:

                extra_info[name_change.id] = {
                    "discord_tag": "N/A",
                    "discord_membership": False,
                    "discord_guild_joined": "N/A"
                }

        return render_template("admin.html", name_changes=name_changes, extra_info=extra_info)

