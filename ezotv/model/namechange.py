#!/usr/bin/env python3#!/usr/bin/env python3
from .db import db
from sqlalchemy.sql import func

from .user import User


class NameChange(db.Model):

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)

    old_name = db.Column(db.String(16), nullable=True)

    created = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)  # NO BACKREF

    active = db.Column(db.Boolean, default=True, nullable=False)
