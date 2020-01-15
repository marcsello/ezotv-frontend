#!/usr/bin/env python3
from .db import db
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from .user import User


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)
