#!/usr/bin/env python3
from flask import Flask
from datetime import timedelta
import os

# import stuff
from model import db
from utils import register_all_error_handlers, login_manager, discord_blueprint

# import views
from views import HomeView, BackupsView, DashboardView

from api_views import UserView

 ##### ##### ##### #### #  # ##### #    # ##### ####  ##### #     #####  #     #     ####  ##### #     # ##### ####   #
 #       #   #   # #    # #  #   # #    # #     #   # #     #     #   #  #  #  #     #   # #   # #  #  # #     #   #  #
 #####   #   ##### #    ##   #   # #    # ####  ####  ###   #     #   #  #  #  #     ####  #   # #  #  # ####  ####   #
     #   #   #   # #    # #  #   #  #  #  #     ##    #     #     #   #  #  #  #     #     #   # #  #  # #     ##
 #####   #   #   # #### #  # #####   #    ##### #  #  #     ##### #####  #######     #     ##### ####### ##### #  #   #


# create flask app
app = Flask(__name__)

# configure flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['EZOTV_DATABASE_URI']
app.config['LOCAL_API_KEY'] = os.environ['EZOTV_LOCAL_API_KEY']
app.config['LUNA_API_KEY'] = os.environ['EZOTV_LUNA_API_KEY']
app.config['SERVER_NAME'] = os.environ['EZOTV_SERVER_NAME']  # ezotv.marcsello.com

# important stuff
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(12))
app.config["DISCORD_OAUTH_CLIENT_ID"] = os.environ.get("EZOTV_DISCORD_OAUTH_CLIENT_ID")
app.config["DISCORD_OAUTH_CLIENT_SECRET"] = os.environ.get("EZOTV_DISCORD_OAUTH_CLIENT_SECRET")


# initialize stuff
db.init_app(app)

with app.app_context():
	db.create_all()

# register error handlers
register_all_error_handlers(app)

# register views
for view in [DashboardView, HomeView, BackupsView]:
	view.register(app, trailing_slash=False)

# register views
for view in [UserView]:
	view.register(app, trailing_slash=False, route_prefix="/api/")


app.register_blueprint(discord_blueprint, url_prefix="/dashboard/login")


login_manager.init_app(app)


# start debuggig if needed
if __name__ == "__main__":
	app.run(debug=True)
