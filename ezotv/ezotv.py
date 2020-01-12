#!/usr/bin/env python3
from flask import Flask
from datetime import timedelta
import os


# import stuff
from model import db
from utils import register_all_error_handlers

# import views
from views import RegisterView, HomeView, BackupsView

from api_views import PlayerView

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
app.config["RECAPTCHA_SITEKEY"] = os.environ['EZOTV_RECAPTCHA_SITEKEY']
app.config["RECAPTCHA_PRIVATEKEY"] = os.environ['EZOTV_RECAPTCHA_PRIVATEKEY']

# initialize stuff
db.init_app(app)

with app.app_context():
	db.create_all()

# register error handlers
register_all_error_handlers(app)

# register views
for view in [RegisterView, HomeView, BackupsView]:
	view.register(app, trailing_slash=False)

# register views
for view in [PlayerView]:
	view.register(app, trailing_slash=False, route_prefix="/api/")

# start debuggig if needed
if __name__ == "__main__":
	app.run(debug=True)
