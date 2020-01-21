#!/usr/bin/env python3
from .db import db
from sqlalchemy.sql import func
from flask_login import UserMixin
from discordbot_tools import discord_bot
import enum


class NameStatus(enum.Enum):
    NEW = 0
    CHANGED = 1
    APPROVED = 2
    UNAPPROVED = 3


class User(UserMixin, db.Model):

    # Identification
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)

    # recieved via oauth2 memery; It's actually duplicated here
    discord_id = db.Column(db.String(32), unique=True, nullable=False)

    # Important data
    minecraft_name = db.Column(db.String(16), unique=True, nullable=True)

    password = db.Column(db.String(255), unique=False, nullable=True)
    salt = db.Column(db.String(50), unique=False, nullable=True)

    # administrative
    registered = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    in_sync = db.Column(db.Boolean, default=False, nullable=False)
    name_status = db.Column(db.Enum(NameStatus), default=NameStatus.NEW, nullable=False)

    @property
    def is_member(self) -> bool:
        return discord_bot.instance.check_membership(self.discord_id)

    @property
    def is_admin(self) -> bool:
        return discord_bot.instance.check_is_admin(self.discord_id)
