import os
import json

from quart import Quart, redirect, url_for, send_from_directory, send_file, request, render_template
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import discord
from tinydb import TinyDB, Query, where
from bot import Bot

from util import requires_membership, MissingMembership

import asyncio

import logging


# !! Only in development environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

# app.config["DISCORD_CLIENT_ID"] =     # Discord client ID.
# app.config["DISCORD_CLIENT_SECRET"] = ""                # Discord client secret.
# app.config["DISCORD_REDIRECT_URI"] = ""                 # URL to your callback endpoint.
# app.config["DISCORD_BOT_TOKEN"] = ""                    # Required to access BOT resources.

UOAF_GUILD_ID = 582602200619024406


def get_mod_path():
    filepath = os.path.abspath(__file__)
    dirname, fname = os.path.split(filepath)
    return dirname


def create_app(config_file_name='config.py'):
    asyncio.set_event_loop(asyncio.new_event_loop())
    dbFile = os.path.join(os.path.dirname(__file__), 'db.json')
    db = TinyDB(dbFile)
    app = Quart(__name__)
    app.config.from_pyfile('config.py')
    discord_auth = DiscordOAuth2Session(app)

    try:
        verbose_debug = app.config["VERBOSE_DEBUG"]
    except KeyError:
        verbose_debug = False
    if verbose_debug:
        LOG_FORMAT = "[%(levelname)-8s][%(filename)24s:%(lineno)-4s "
        LOG_FORMAT += "%(funcName)32s() ]%(name)s: %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    app.secret_key = b"random bytes representing Quart secret key"

    @app.route('/static/<path:path>')
    async def send_js(path):
        return send_from_directory('js', path)

    @app.route("/login/")
    async def login():
        result = await discord_auth.create_session()
        return result

    @app.route("/callback/")
    async def callback():
        await discord_auth.callback()
        return redirect(url_for(".index"))

    @app.errorhandler(Unauthorized)
    async def redirect_unauthorized(e):
        return redirect(url_for("login"))

    @app.errorhandler(MissingMembership)
    async def render_missing_membership(e):
        return render_template('unauthorized.html'), 401

    @app.route("/getEvents/")
    @requires_membership(UOAF_GUILD_ID)
    async def getEvents():
        eventTable = db.table('Events')
        eventsList = eventTable.all()
        return {'events': eventsList}

    @app.route("/getLatestEvents/")
    @requires_membership(UOAF_GUILD_ID)
    async def getLatestEvents():
        eventTable = db.table('Events')
        eventsList = eventTable.all()
        return {'events': eventsList[-4:]}

    @app.route("/updateEvent/", methods=["PUT"])
    @requires_membership(UOAF_GUILD_ID)
    async def updateEvent():
        eventUpdate = await request.get_json()
        eventName = eventUpdate["EventName"]
        eventsTable = db.table('Events')
        dbQuery = Query()
        eventToUpdate = eventsTable.search(dbQuery.EventName == eventName)[0]
        #eventsTable.insert(re)
        #data_as_json = request.get_json()
        #events.insert(data_as_json)
        return {}

    @app.route("/putEvent/", methods=["PUT"])
    @requires_membership(UOAF_GUILD_ID)
    async def putEvent():
        events = db.table('Events')
        data_as_json = await request.get_json()
        eventName = data_as_json["EventName"]
        dbQuery = Query()
        checkEventName = events.search(dbQuery.EventName == eventName)
        if (len(checkEventName) > 0):
            print(f"ERROR: {eventName} already found, not inserting.")
            return (f"ERROR: {eventName} already found, not inserting")
        events.insert(data_as_json)
        return data_as_json

    @app.route("/user/")
    @requires_membership(UOAF_GUILD_ID)
    async def get_user_info():
        user = await discord_auth.fetch_user()
        return {
            'username': user.name,
            'avatar_url': user.avatar_url,
            'id': user.id
        }

    @app.route("/")
    @requires_authorization
    async def index():
        x = await send_file('static/index.html')
        return x

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
