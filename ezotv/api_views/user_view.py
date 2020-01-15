#!/usr/bin/env python3
from flask import request, abort, jsonify
from flask_classful import FlaskView
from utils import json_required, apikey_required
import bleach

from model import db, User
from schemas import UserSchema

from marshmallow import ValidationError


class UserView(FlaskView):

    decorators = [apikey_required]

    # faszom sok schema instance... mert a marshamllow buzi és nem lehet on the fly beállítani a fieldeket
    user_schama_unsafe = UserSchema(many=False)
    users_schama_unsafe = UserSchema(many=True)

    user_schama_safe = UserSchema(many=False, exclude=['password', 'salt'], session=db.session)
    users_schama_safe = UserSchema(many=True, exclude=['password', 'salt'])

    def index(self):
        with_password = 'withpassword' in request.args
        unsynced_only = 'unsyncedonly' in request.args

        if unsynced_only:
            users = User.query.filter_by(in_sync=False).all()
        else:
            users = User.query.all()

        if with_password:
            dumper = self.users_schama_unsafe
        else:
            dumper = self.users_schama_safe

        return jsonify(dumper.dump(users))

    def get(self, id: int):
        with_password = 'withpassword' in request.args

        user = User.query.get(id)

        if not user:
            abort(404)

        if with_password:
            dumper = self.user_schama_unsafe
        else:
            dumper = self.user_schama_safe

        return jsonify(dumper.dump(user))

    @json_required
    def patch(self, id: int):  # to update in_sync flag

        user = User.query.get(id)

        if not user:
            abort(404)

        try:
            updated_user = self.user_schama_safe.load(request.json, instance=user, partial=True)
        except ValidationError as e:
            abort(400, str(e))

        db.session.commit()

        return jsonify(self.user_schama_safe.dump(updated_user))

