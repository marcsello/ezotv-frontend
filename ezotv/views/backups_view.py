#!/usr/bin/env python3
from flask import request, abort, render_template, current_app, flash
from flask_classful import FlaskView
from utils import LunaSource
from urllib.parse import urljoin
from json import JSONDecodeError

import os.path

import requests.exceptions


class BackupsView(FlaskView):

    def index(self):

        l = LunaSource(current_app.config['LUNA_API_URL'], current_app.config['LUNA_API_KEY'])

        backup_list = []  # Oké... ez így nagyon szar lesz
        try:
            backup_list = l.backup_list

        except requests.exceptions.ConnectionError as e:
            current_app.logger.error(f"Luna connection error: {e}")
            flash("Nem sikerült kapcsolatba lépni Lunával", "danger")

        except (requests.exceptions.HTTPError, JSONDecodeError) as e:
            current_app.logger.error(f"Luna communication error: {e}")
            flash("Luna nem érzi jól magát...", "danger")

        backup_list.sort(reverse=True)

        data = []
        for filename in backup_list:
            backup_data = {
                "link": urljoin("https://luna.marcsello.com/ezotv/backups/", filename),
                "name": os.path.basename(filename)
            }
            data.append(backup_data)

        return render_template('backups.html', data=data)
