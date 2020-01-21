#!/usr/bin/env python3
from flask import request, abort, render_template, current_app, redirect, url_for, flash
from flask_classful import FlaskView, route

from flask_login import login_required, current_user, logout_user

from urllib.parse import urljoin, quote

from model import db, User, NameChange, NameStatus
from discordbot_tools import discord_bot


class AdminView(FlaskView):

    route_prefix = "/dashboard/"

    decorators = [login_required]

    @login_required
    def before_request(self, name):  # gagyi permission check
        if not discord_bot.instance.check_for_role(current_user.discord_id, current_app.config['DISCORD_ADMIN_ROLE']):
            abort(403)

    def index(self):

        members_lut = discord_bot.instance.get_members_lut()

        name_changes = NameChange.query.filter_by(active=True).all()
        extra_info = {}

        for name_change in name_changes:

            extra_info[name_change.id] = {
                "total_changes": NameChange.query.filter(NameChange.user == name_change.user).count()
            }

            discord_id = name_change.user.discord_id

            if discord_id in members_lut.keys():

                extra_info[name_change.id].update({
                    "discord_tag": "{}#{}".format(members_lut[discord_id]['user']['username'], members_lut[discord_id]['user']['discriminator']),
                    "discord_guild_joined": members_lut[discord_id]['joined_at']  # Ebbe bele kellene verni a gecit
                })

            else:

                extra_info[name_change.id].update({
                    "discord_tag": "N/A",
                    "discord_guild_joined": "N/A"
                })

        return render_template("admin.html", name_changes=name_changes, extra_info=extra_info)

    def post(self):  # TODO: Marshmallow? ?? ?

        approved = 'verdict_accept' in request.form
        try:
            namechange_id = int(request.form['id'])
        except ValueError:
            flash("Hiba a bevitt adatokban!", "danger")  # ezt valaki tuti humorosnak véli majd, tekintve, hogy a bevitt adatok az két gomb
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

        if approved:
            flash("{} név elfogadva!".format(user.minecraft_name), "success")
        else:
            flash("{} név elutasítva!".format(user.minecraft_name), "warning")

        return redirect(url_for("AdminView:index"))
