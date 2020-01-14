#!/usr/bin/env python3
from flask import request, abort, render_template, current_app
from flask_classful import FlaskView

from urllib.parse import urljoin, quote

from flask_dance.contrib.discord import discord
import requests.exceptions


class DashboardView(FlaskView):

    route_prefix = "/dashboard/"
    route_base = '/'

    def index(self):

        if not discord.authorized:
            return render_template('login.html')

        try:
            r = discord.get("/api/users/@me")
            r.raise_for_status()
        except requests.exceptions.ConnectionError:
            return render_template('login.html', error="Nem sikerült kommunikálni a Discord szervereivel!")

        except requests.exceptions.HTTPError:
            return render_template('login.html', error="A Discord nem várt hibával tért vissza. Esetleg megpróbálkozhatsz újra be jelentkezni.")

        return render_template('dashboard.html', discord_tag="{}#{}".format(r.json()['username'], r.json()['discriminator']))


