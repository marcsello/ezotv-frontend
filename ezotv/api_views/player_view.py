#!/usr/bin/env python3
from flask import request, abort
from flask_classful import FlaskView
from utils import json_required, apikey_required
import bleach

from model import db


class PlayerView(FlaskView):

    @apikey_required
    @json_required
    def post(self):
        return "Hello api"

