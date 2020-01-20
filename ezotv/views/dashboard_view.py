#!/usr/bin/env python3
from flask import request, abort, render_template, current_app, redirect, url_for, flash
from flask_classful import FlaskView, route

from flask_login import login_required, current_user, logout_user

from urllib.parse import urljoin, quote

from flask_dance.contrib.discord import discord
import requests.exceptions


class DashboardView(FlaskView):

    route_prefix = "/dashboard/"
    route_base = '/'

    def loginfo(self):
        if current_user.is_authenticated:
            return redirect(url_for("DashboardView:index"))
        return render_template('loginfo.html')

    @route("/logout", methods=['POST'])  # POST to prevent redirect attack.... altrough not very good solution
    @login_required
    def logout(self):
        logout_user()
        # TODO: revoke token???? Lehet ez nem kell
        return redirect(url_for("DashboardView:loginfo"))

    @login_required  # redirects to loginfo
    def index(self):

        try:
            r = discord.get("/api/users/@me")
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            flash("Nem sikerült kommunikálni a Discord szervereivel", "danger")
            logout_user()
            return redirect(url_for("DashboardView:loginfo"))

        return render_template('dashboard.html', discord_tag="{}#{}".format(r.json()['username'], r.json()['discriminator']))


