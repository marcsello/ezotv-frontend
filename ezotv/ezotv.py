#!/usr/bin/env python3
from flask import Flask
from datetime import timedelta
import os

# import stuff
from model import db
from utils import register_all_error_handlers, login_manager, discord_blueprint
from discordbot_tools import discord_bot

# import views
from views import HomeView, BackupsView, DashboardView, AdminView

from api_views import UserView

 ##### ##### ##### #### #  # ##### #    # ##### ####  ##### #     #####  #     #     ####  ##### #     # ##### ####   #
 #       #   #   # #    # #  #   # #    # #     #   # #     #     #   #  #  #  #     #   # #   # #  #  # #     #   #  #
 #####   #   ##### #    ##   #   # #    # ####  ####  ###   #     #   #  #  #  #     ####  #   # #  #  # ####  ####   #
     #   #   #   # #    # #  #   #  #  #  #     ##    #     #     #   #  #  #  #     #     #   # #  #  # #     ##
 #####   #   #   # #### #  # #####   #    ##### #  #  #     ##### #####  #######     #     ##### ####### ##### #  #   #


# create flask app
app = Flask(__name__)

# configure flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('EZOTV_DATABASE_URI', "sqlite://")  # Default to memory db
app.config['LOCAL_API_KEY'] = os.environ['EZOTV_LOCAL_API_KEY']
app.config['LUNA_API_KEY'] = os.environ['EZOTV_LUNA_API_KEY']
app.config['SERVER_NAME'] = os.environ['EZOTV_SERVER_NAME']  # ezotv.marcsello.com

# important stuff
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(12))
app.config['DISCORD_OAUTH_CLIENT_ID'] = os.environ['EZOTV_DISCORD_OAUTH_CLIENT_ID']
app.config['DISCORD_OAUTH_CLIENT_SECRET'] = os.environ['EZOTV_DISCORD_OAUTH_CLIENT_SECRET']
app.config['DISCORD_BOT_TOKEN'] = os.environ['EZOTV_DISCORD_BOT_TOKEN']
app.config['DISCORD_GUILD_ID'] = os.environ['EZOTV_DISCORD_GUILD_ID']
app.config['DISCORD_ADMIN_ROLE'] = os.environ['EZOTV_DISCORD_ADMIN_ROLE']

# wtf
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# initialize stuff
db.init_app(app)

with app.app_context():
	db.create_all()

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


# start debuggig if needed
if __name__ == "__main__":
	app.run(debug=True)
