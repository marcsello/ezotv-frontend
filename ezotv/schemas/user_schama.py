#!/usr/bin/env python3
from marshmallow import fields, RAISE
from marshmallow_sqlalchemy import ModelSchema
from model import Player

from model import db, User


class UserSchema(ModelSchema):

	class Meta:
		dump_only = ['id', 'registered']
		model = User
		unknown = RAISE
