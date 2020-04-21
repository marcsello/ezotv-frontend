#!/usr/bin/env python3
from marshmallow import Schema, fields, RAISE
from marshmallow import ValidationError
from marshmallow.validate import Range


class BytesField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError('Invalid input type.')

        if value is None or value == b'':
            raise ValidationError('Invalid value')


class CacheSchema(Schema):
    content = BytesField(required=True)
    status_code = fields.Integer(required=True, validate=Range(min=100, max=599))
    headers = fields.Dict(required=True)

    class Meta:
        unknown = RAISE
