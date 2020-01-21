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

        extra_info = {1: {
            "discord_tag": "Test#1234",
            "discord_membership": True,
            "discord_guild_joined": "yesterday"
        }}

        return render_template("admin.html", name_changes=NameChange.query.all(), extra_info=extra_info)

