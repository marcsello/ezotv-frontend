#!/usr/bin/env python3
from flask import request, abort, render_template, current_app
from flask_classful import FlaskView

import sqlalchemy.exc

import requests
import random
import string
import hashlib

from schemas import RegisterFormSchema, PlayerSchema
from marshmallow import ValidationError

from model import db, Player


class RegisterView(FlaskView):

    register_form_schema = RegisterFormSchema(many=False)

    friendly_field_names = {
        "name": "Név",
        "minecraft_name": "Minecraft játékosnév",
        "email": "E-mail cím",
        "discord": "Discord tag",
        "password": "Jelszó",
        "password_verify": "Jelszó mégegyszer",
        "g-recaptcha-response": "CAPTCHA",
    }

    player_schema = PlayerSchema(many=False, session=db.session)

    def get(self):

        return render_template('register.html', config={"recaptcha_sitekey": current_app.config["RECAPTCHA_SITEKEY"]}, prefill={})

    def post(self):

        form_raw_data = dict(request.form)

        # check validity
        try:
            form_data = self.register_form_schema.dump(  # mer' ez így jó
                self.register_form_schema.load(form_raw_data)
            )
        except ValidationError as e:

            mistakes = [self.friendly_field_names[k] for k in e.normalized_messages().keys() if k != "_schema"]

            if "_schema" in e.normalized_messages().keys():
                mistakes += e.normalized_messages()['_schema']

            return render_template('register.html', mistakes=mistakes, config={"recaptcha_sitekey": current_app.config["RECAPTCHA_SITEKEY"]}, prefill=form_raw_data)

        # TODO: resolve discord id
        player_data = form_data.copy()
        discord = player_data['discord']
        del player_data['discord']
        player_data['discord_id'] = '123'

        # Hash password for AuthMe RSA512SALTED format
        password_clear = player_data['password']
        del player_data['password']

        password_salt = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(16))
        password_hashed = hashlib.sha512(password_clear.encode() + password_salt.encode()).hexdigest()

        player_data['password'] = password_hashed
        player_data['salt'] = password_salt
        # perform registration

        ply = Player(**player_data)

        db.session.add(ply)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return render_template('register.html', error="Ilyen adatokkal már létezik regisztráció", config={"recaptcha_sitekey": current_app.config["RECAPTCHA_SITEKEY"]}, prefill=form_raw_data)

        return render_template('register_success.html')
