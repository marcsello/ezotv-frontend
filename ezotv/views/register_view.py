#!/usr/bin/env python3
from flask import request, abort, render_template, current_app
from flask_classful import FlaskView

import requests
import sys

from schemas import RegisterFormSchema
from marshmallow import ValidationError

from model import db


class RegisterView(FlaskView):

    register_form_schema = RegisterFormSchema(many=False)

    def get(self):

        return render_template('register.html', config={"recaptcha_sitekey": current_app.config["RECAPTCHA_SITEKEY"]})

    def post(self):

        try:
            form_contents = self.register_form_schema.load(dict(request.form))
        except ValidationError as e:
            return render_template('register.html', error=str(e), config={"recaptcha_sitekey": current_app.config["RECAPTCHA_SITEKEY"]})

        return render_template('register_success.html')
