#!/usr/bin/env python3
from marshmallow import fields, RAISE
from marshmallow_sqlalchemy import ModelSchema
from marshmallow_enum import EnumField
from model import User, NameStatus

from model import db, User


class UserSchema(ModelSchema):

	name_status = EnumField(NameStatus)

	class Meta:
		dump_only = ['id', 'discord_id', 'minecraft_name', 'password', 'salt', 'registered', 'name_status']  # keeping in_sync modifiable only
		model = User
		unknown = RAISE
