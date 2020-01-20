#!/usr/bin/env python3
from marshmallow import Schema, fields, validates_schema, ValidationError, pre_load, validates, RAISE
from marshmallow.validate import Regexp, Length


class MinecraftFormSchema(Schema):

    minecraft_name = fields.Str(required=True, validate=[Length(min=3, max=16), Regexp("^[A-Za-z0-9_]*$")])

    password = fields.Str(required=True, validate=Length(min=6))
    password_verify = fields.Str(load_only=True, required=True, validate=Length(min=6))

    submit = fields.Str(load_only=True, required=False, allow_none=True)

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["password"] != data["password_verify"]:
            raise ValidationError("Passwords do not match!")

    class Meta:
        unknown = RAISE
