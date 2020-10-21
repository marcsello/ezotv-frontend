#!/usr/bin/env python3
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# import stuff
from model import db
from utils import register_all_error_handlers, login_manager, discord_blueprint

from cache_tools import redis_client
from discordbot_tools import discord_bot

# import views
from views import HomeView, BackupsView, DashboardView, AdminView

from api_views import UserView

 ##### ##### ##### #### #  # ##### #    # ##### ####  ##### #     #####  #     #     ####  ##### #     # ##### ####   #
 #       #   #   # #    # #  #   # #    # #     #   # #     #     #   #  #  #  #     #   # #   # #  #  # #     #   #  #
 #####   #   ##### #    ##   #   # #    # ####  ####  ###   #     #   #  #  #  #     ####  #   # #  #  # ####  ####   #
     #   #   #   # #    # #  #   #  #  #  #     ##    #     #     #   #  #  #  #     #     #   # #  #  # #     ##
 #####   #   #   # #### #  # #####   #    ##### #  #  #     ##### #####  #######     #     ##### ####### ##### #  #   #

# Setup sentry
SENTRY_DSN = os.environ.get("EZOTV_SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        send_default_pii=True
    )

# create flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

# configure flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('EZOTV_DATABASE_URI', "sqlite://")  # Default to memory db
app.config['LOCAL_API_KEY'] = os.environ['EZOTV_LOCAL_API_KEY']
app.config['LUNA_API_KEY'] = os.environ['EZOTV_LUNA_API_KEY']
app.config['LUNA_API_URL'] = os.environ['EZOTV_LUNA_API_URL']
app.config['SERVER_NAME'] = os.environ['EZOTV_SERVER_NAME']  # ezotv.marcsello.com

# important stuff
app.secret_key = os.environ.get('EZOTV_SECRET_KEY', os.urandom(12))
app.config['DISCORD_OAUTH_CLIENT_ID'] = os.environ['EZOTV_DISCORD_OAUTH_CLIENT_ID']
app.config['DISCORD_OAUTH_CLIENT_SECRET'] = os.environ['EZOTV_DISCORD_OAUTH_CLIENT_SECRET']
app.config['DISCORD_BOT_TOKEN'] = os.environ['EZOTV_DISCORD_BOT_TOKEN']
app.config['DISCORD_GUILD_ID'] = os.environ['EZOTV_DISCORD_GUILD_ID']
app.config['DISCORD_ADMIN_ROLE'] = os.environ['EZOTV_DISCORD_ADMIN_ROLE']
app.config['DISCORD_ADMIN_CHAT'] = os.environ['EZOTV_DISCORD_ADMIN_CHAT']
app.config['REDIS_URL'] = os.environ['EZOTV_REDIS_URL']
app.config['CACHE_TIMEOUT'] = os.environ['EZOTV_CACHE_TIMEOUT']

# wtf
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PREFERRED_URL_SCHEME'] = 'https'


# initialize stuff
db.init_app(app)
redis_client.init_app(app)
discord_bot.init_app(app)

# register error handlers
register_all_error_handlers(app)

# register views
for view in [DashboardView, HomeView, BackupsView, AdminView]:
    view.register(app, trailing_slash=False)

# register views
for view in [UserView]:
    view.register(app, trailing_slash=False, route_prefix="/api/")


app.register_blueprint(discord_blueprint, url_prefix="/dashboard/login")

login_manager.init_app(app)


@app.before_first_request
def initial_setup():
    db.create_all()


# start debugging if needed
if __name__ == "__main__":
    app.run(debug=True)
