#!/usr/bin/env python3
from flask import request, current_app, abort
from flask_login import current_user

from functools import wraps


def apikey_required(f):

    @wraps(f)
    def call(*args, **kwargs):

        apikey_recieved = request.headers.get('Authorization', None)

        if apikey_recieved == current_app.config['LOCAL_API_KEY']:
            return f(*args, **kwargs)
        else:
            abort(401, "Unauthorized")

    return call


def json_required(f):

    @wraps(f)
    def call(*args, **kwargs):

        if request.is_json:
            return f(*args, **kwargs)
        else:
            abort(400, "JSON required")

    return call


def admin_required(f):

    @wraps(f)
    def call(*args, **kwargs):

        if current_user.is_admin:
            return f(*args, **kwargs)
        else:
            abort(403)

    return call

