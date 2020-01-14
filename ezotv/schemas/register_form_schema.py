#!/usr/bin/env python3
from marshmallow import Schema, fields, validates_schema, ValidationError, pre_load, validates, RAISE
from marshmallow.validate import Regexp, Length, NoneOf

import bleach

from utils import validate_rechaptcha


class RegisterFormSchema(Schema):

    name = fields.Str(required=True, validate=Length(min=3, max=50))
    minecraft_name = fields.Str(required=True, validate=[Length(min=3, max=16), Regexp("[A-Za-z0-9_]*")])
    email = fields.Email(required=True, validate=Length(max=500))
    discord = fields.Str(required=True, validate=[Length(min=1, max=32), Regexp(".*#[0-9]{4}"), NoneOf(["discordtag", "everyone", "here"])])  # Kinda pointless being this strict
    password = fields.Str(required=True)
    password_verify = fields.Str(load_only=True, required=True)
    g_recaptcha_response = fields.Str(data_key="g-recaptcha-response", load_only=True)
    submit = fields.Str(load_only=True, required=False, allow_none=True)

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["password"] != data["password_verify"]:
            raise ValidationError("Passwords do not match!")

    @pre_load(pass_many=False)
    def sanitize_input(self, data, **kwargs):
        data['name'] = bleach.clean(data['name'], tags=[])
        return data

    @validates("g_recaptcha_response")  # True magic
    def validate_chaptcha(self, value):
        if not validate_rechaptcha(value):
            raise ValidationError("CHAPTCHA verification failed!")

    class Meta:
        unknown = RAISE
