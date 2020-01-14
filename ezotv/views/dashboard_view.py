#!/usr/bin/env python3
from flask import request, abort, render_template, current_app
from flask_classful import FlaskView

from urllib.parse import urljoin, quote


class DashboardView(FlaskView):

    route_prefix = "/dashboard/"
    route_base = '/'

    def index(self):

        return render_template('login.html')
