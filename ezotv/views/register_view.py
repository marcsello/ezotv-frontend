#!/usr/bin/env python3
from flask import request, abort, render_template, current_app
from flask_classful import FlaskView

import bleach

from model import db


class RegisterView(FlaskView):

    def get(self):

        return render_template('register.html', error="Bele van szarva a bablevesbe!", config={"recaptcha_sitekey": current_app.config["RECAPTCHA_SITEKEY"]})

    def post(self):

        return render_template('register_success.html')
