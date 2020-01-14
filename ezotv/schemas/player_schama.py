#!/usr/bin/env python3
from marshmallow import fields, RAISE
from marshmallow_sqlalchemy import ModelSchema
from model import Player

from model import db, Player


class PlayerSchema(ModelSchema):

	class Meta:
		dump_only = ['id', 'registered']
		model = Player
		unknown = RAISE
