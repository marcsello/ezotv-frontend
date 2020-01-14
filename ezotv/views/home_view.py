#!/usr/bin/env python3
from flask import request, abort, render_template, current_app
from flask_classful import FlaskView
from utils import LunaSource


class HomeView(FlaskView):

    route_base = '/'

    def index(self):

        l = LunaSource(current_app.config['LUNA_API_KEY'])

        data = {
            "backup": {"latest": l.latest_backup},
            "map": l.map_status,
            "server": l.server_status,
            "players": l.players_data
        }

        return render_template('home.html', data=data)
