#!/usr/bin/env python3
from .db import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class User(UserMixin, db.Model):

    # Identification
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)

    # Important data
    minecraft_name = db.Column(db.String(16), unique=True, nullable=True)

    password = db.Column(db.String(255), unique=False, nullable=True)
    salt = db.Column(db.String(50), unique=False, nullable=True)

    # recieved via oauth2 memery
    discord_id = db.Column(db.String(32), unique=True, nullable=False)

    # administrative
    registered = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
