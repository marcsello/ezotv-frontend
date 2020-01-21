#!/usr/bin/env python3
from flask import request, abort, render_template, current_app, redirect, url_for, flash
from flask_classful import FlaskView, route

from flask_login import login_required, current_user, logout_user

from urllib.parse import urljoin, quote

from model import db, User
from utils import DiscordBot


class AdminView(FlaskView):

    route_prefix = "/dashboard/"

    discord_bot = DiscordBot()
    decorators = [login_required]

    def index(self):

        return render_template("admin.html", users=User.query.all())

