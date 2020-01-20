import pytest

from schemas import MinecraftFormSchema, UserSchema
from marshmallow.exceptions import ValidationError


@pytest.fixture
def minecraft_form_schema():
    yield MinecraftFormSchema(many=False)


def test_valid(minecraft_form_schema):

        original = {
            "minecraft_name": "abcd",
            "password": "123456",
            "password_verify": "123456"
        }

        loaded = minecraft_form_schema.load(original)

        assert original == loaded


def test_invalid_name(minecraft_form_schema):
    with pytest.raises(ValidationError):
        loaded = minecraft_form_schema.load({
            "minecraft_name": "ábcd",
            "password": "123456",
            "password_verify": "123456"
        })


def test_toolong_name(minecraft_form_schema):
    with pytest.raises(ValidationError):
        minecraft_form_schema.load({
            "minecraft_name": "111dfqafgae39f9f93f9j3f9j3fj93f3f3f3f3",
            "password": "123456",
            "password_verify": "123456"
        })


def test_tooshort_name(minecraft_form_schema):
    with pytest.raises(ValidationError):
        minecraft_form_schema.load({
            "minecraft_name": "a",
            "password": "123456",
            "password_verify": "123456"
        })


def test_tooshort_password(minecraft_form_schema):
    with pytest.raises(ValidationError):
        minecraft_form_schema.load({
            "minecraft_name": "abcd",
            "password": "1234",
            "password_verify": "1234"
        })


def test_mismatchnig_password(minecraft_form_schema):
    with pytest.raises(ValidationError):
        minecraft_form_schema.load({
            "minecraft_name": "abcd",
            "password": "123456",
            "password_verify": "1234567"
        })
