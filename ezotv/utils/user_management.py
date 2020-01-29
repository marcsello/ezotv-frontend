#!/usr/bin/env python3
from flask import flash, redirect, url_for
from flask_dance.contrib.discord import make_discord_blueprint

from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage

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
    oauth = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=user_id).first()

    if oauth:
        oauth.token = token  # update the token
    else:
        oauth = OAuth(provider=blueprint.name, provider_user_id=user_id, token=token)

    if not oauth.user:

        # check if the user with this discord id exists: (It's possible... and this is a very bad and ugly solution!)
        user = User.query.filter_by(discord_id=info["id"]).first()

        if not user:
            # if not, create a new local user account for this user
            user = User(discord_id=info["id"])
            db.session.add(user)

        oauth.user = user

    db.session.add(oauth)  # add anyways
    db.session.commit()

    login_user(oauth.user)  # must happen after commit

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
