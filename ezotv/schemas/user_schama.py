#!/usr/bin/env python3
from marshmallow import fields, RAISE
from marshmallow_sqlalchemy import ModelSchema
from model import User

from model import db, User


class UserSchema(ModelSchema):

	class Meta:
		dump_only = ['id', 'discord_id', 'minecraft_name', 'password', 'salt', 'registered', 'name_approved']  # keeping in_sync modifiable only
		model = User
		unknown = RAISE
