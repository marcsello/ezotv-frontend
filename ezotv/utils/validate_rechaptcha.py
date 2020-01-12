#!/usr/bin/env python3

from flask import current_app
import requests


def validate_rechaptcha(recaptcha_response: str) -> bool:
    verify_data = {'secret': current_app.config['RECAPTCHA_PRIVATEKEY'], 'response': recaptcha_response}

    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=verify_data)

    return r.json()['success']

