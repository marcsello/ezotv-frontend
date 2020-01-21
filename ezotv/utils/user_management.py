#!/usr/bin/env python3
from flask import flash, redirect, url_for
from flask_dance.contrib.discord import make_discord_blueprint

from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound

from flask_login import LoginManager, current_user, login_user
from model import db, User, OAuth


import requests.exceptions


discord_blueprint = make_discord_blueprint(
    scope="identify",
    redirect_to="DashboardView:index",
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user
    )
)

login_manager = LoginManager()
login_manager.login_view = "DashboardView:loginfo"
login_manager.login_message = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# create/login local user on successful OAuth login
@oauth_authorized.connect_via(discord_blueprint)
def discord_logged_in(blueprint, token):
    if not token:
        flash("Sikertelen bejelentkezés.", "danger")
        return redirect(url_for(login_manager.login_view))  # go back to loginfo

    try:
        resp = blueprint.session.get("/api/users/@me")  # <- Ez amugy Discord specifikus
    except requests.exceptions.ConnectionError:
        flash("Nem sikerült kapcsolatba lépni a {} szervereivel.".format(blueprint.name), "danger")
        return redirect(url_for(login_manager.login_view))  # go back to loginfo

    if not resp.ok:
        flash("Nem sikerült megkapni az adataidat a {} szervereitől".format(blueprint.name), "danger")
        return redirect(url_for(login_manager.login_view))  # go back to loginfo

    info = resp.json()
    user_id = info["id"]

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=user_id, token=token)

    if oauth.user:  # <- ez itt gecihülyén van megcsinálva
        login_user(oauth.user)

    else:
        # Create a new local user account for this user
        user = User(discord_id=info["id"])
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False  # proceed to dashboard index


# notify on OAuth provider error
@oauth_error.connect_via(discord_blueprint)
def discord_error(blueprint, error, error_description, error_uri):

    if error == 'access_denied':
        flash("A hozzáférési engedély nem lett megadva!", "warning")
    else:

        msg = ("OAuth error from {name}! {error}: {error_description}").format(
            name=blueprint.name, error=error, error_description=error_description
        )
        flash(msg, "danger")
