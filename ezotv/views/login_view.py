#!/usr/bin/env python3
from flask import request, abort, render_template, current_app
from flask_classful import FlaskView

from urllib.parse import urljoin, quote


class LoginView(FlaskView):

    route_prefix = "/dashboard/"

    def get(self):

        oauth_link = "https://discordapp.com/api/oauth2/authorize?client_id={}&redirect_uri={}&response_type=code&scope=identify&state={}".format(
            current_app.config['DISCORD_CLIENT_ID'],
            quote(urljoin(current_app.config['BASE_URL'], 'dashboard/login'), safe=''),
            "hunting_ducks"
        )

        return render_template('login.html', oauth_link=oauth_link)
