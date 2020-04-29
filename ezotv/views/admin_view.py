#!/usr/bin/env python3
from flask import request, abort, render_template, current_app, redirect, url_for, flash
from flask_classful import FlaskView, route

from flask_login import login_required, current_user, logout_user

from flask_dance.contrib.discord import discord
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError
import requests.exceptions

from model import db, User, NameChange, NameStatus
from discordbot_tools import discord_bot

from utils import admin_required
from datetime import datetime


class AdminView(FlaskView):
    route_prefix = "/dashboard/"

    decorators = [login_required, admin_required]

    def index(self):

        members_lut = discord_bot.instance.get_members_lut()  # This is a lookup table, to resolve discord ids to names

        name_changes = NameChange.query.filter_by(active=True).all()
        extra_info = {}

        for name_change in name_changes:

            extra_info[name_change.id] = {
                "total_changes": NameChange.query.filter(NameChange.user == name_change.user).count()
            }

            discord_id = name_change.user.discord_id

            if discord_id in members_lut.keys():

                extra_info[name_change.id].update({
                    "discord_guild_joined": datetime.strptime(  # Ebbe bele kellene verni a gecit
                        members_lut[discord_id]['joined_at'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M:%S")
                })

            else:

                extra_info[name_change.id].update({
                    "discord_tag": "N/A",
                    "discord_guild_joined": "N/A"
                })

        users = User.query.all()

        return render_template(
            "admin.html",
            name_changes=name_changes,
            extra_info=extra_info,
            users=users,
            members_lut=members_lut
        )

    def post(self):  # TODO: Marshmallow? ?? ?

        # Figure out who did this...

        try:
            r = discord.get("/api/users/@me")
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            flash("Nem sikerült kommunikálni a Discord szervereivel!", "danger")
            logout_user()
            return redirect(url_for("DashboardView:loginfo"))
        except (InvalidGrantError, TokenExpiredError):
            logout_user()
            return redirect(url_for("DashboardView:loginfo"))

        committer_user_info = r.json()
        committer_user_discord_tag = f"{committer_user_info['username']}#{committer_user_info['discriminator']}"

        # Perform accepting...

        approved = 'verdict_accept' in request.form
        try:
            namechange_id = int(request.form['id'])
        except ValueError:
            # ezt valaki tuti humorosnak véli majd, tekintve, hogy a bevitt adatok az két gomb
            flash("Hiba a bevitt adatokban!", "danger")
            return redirect(url_for("AdminView:index"))

        namechange = NameChange.query.get(namechange_id)
        user = namechange.user

        if not namechange:
            flash("Ismeretlen kérvény!", "danger")
            return redirect(url_for("AdminView:index"))

        if approved:
            user.name_status = NameStatus.APPROVED
        else:
            user.name_status = NameStatus.UNAPPROVED

        user.name_status.in_sync = False

        db.session.add(user)

        namechange.active = False
        db.session.add(namechange)

        db.session.commit()  # Itt nem sérthetünk meg constraint

        # Administrate the administration

        if approved:
            flash(f"{user.minecraft_name} név elfogadva!", "success")
            discord_bot.instance.post_log(
                f"New administraion event!\nName {user.minecraft_name} is accepted by {committer_user_discord_tag}"
            )
        else:
            flash(f"{user.minecraft_name} név elutasítva!", "warning")
            discord_bot.instance.post_log(
                f"New administraion event!\nName {user.minecraft_name} is rejected by {committer_user_discord_tag}"
            )

        # Done...

        return redirect(url_for("AdminView:index"))
