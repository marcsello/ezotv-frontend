#!/usr/bin/env python3
from flask import request, abort, render_template, current_app
from flask_classful import FlaskView
from utils import LunaSource
from urllib.parse import urljoin

import os.path


class BackupsView(FlaskView):

    def get(self):

        l = LunaSource(current_app.config['LUNA_API_KEY'])

        data = {}
        for key, value in l.backup_list.items():

       #     key_readable = key.replace('_', ' ').capitalize()  # dunno

            value.sort(reverse=True)

            data[key] = []
            for filename in value:
                backup_data = {
                    "link": urljoin("https://luna.marcsello.com/ezotv/backups/", filename),
                    "name": os.path.basename(filename)
                }
                data[key].append(backup_data)

        return render_template('backups.html', data=data)
