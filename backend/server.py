import os
import json

from quart import Quart, redirect, url_for, send_from_directory, send_file, \
    request, render_template, abort
from quart_discord import DiscordOAuth2Session, \
    requires_authorization, Unauthorized
import discord
from bot import Bot
from store import Store

from util import requires_membership, MissingMembership

import functools
import asyncio

import logging


# !! Only in development environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

# app.config["DISCORD_CLIENT_ID"] =     # Discord client ID.
# app.config["DISCORD_CLIENT_SECRET"] = ""                # Discord client secret.
# app.config["DISCORD_REDIRECT_URI"] = ""                 # URL to your callback endpoint.
# app.config["DISCORD_BOT_TOKEN"] = ""                    # Required to access BOT resources.


def get_mod_path():
    filepath = os.path.abspath(__file__)
    dirname, fname = os.path.split(filepath)
    return dirname


def create_app(config_file_name='config.py'):
    asyncio.set_event_loop(asyncio.new_event_loop())
    dbFile = os.path.join(os.path.dirname(__file__), 'db.json')
    db = Store(dbFile)
    app = Quart(__name__)
    app.config.from_pyfile('config.py')
    discord_auth = DiscordOAuth2Session(app)
    bot = Bot(app.config["ATO_PRIMARY_GUILD_ID"])

    try:
        verbose_debug = app.config["VERBOSE_DEBUG"]
    except KeyError:
        verbose_debug = False
    if verbose_debug:
        LOG_FORMAT = "[%(levelname)-8s][%(filename)24s:%(lineno)-4s "
        LOG_FORMAT += "%(funcName)32s() ]%(name)s: %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    app.secret_key = b"random bytes representing Quart secret key"

    def requires_role(role_name):
        def decorator(view_func):
            @functools.wraps(view_func)
            async def wrapper(*args, **kwargs):
                if not await discord_auth.authorized():
                    raise Unauthorized()
                user = await discord_auth.fetch_user()
                roles = bot.get_roles_of_user(user.id)
                role_names = [r.name for r in roles]
                if role_name not in role_names:
                    raise MissingMembership()
                else:
                    return await view_func(*args, **kwargs)
            return wrapper
        return decorator

    @app.before_serving
    async def startup():
        asyncio.create_task(bot.run())

    @app.route("/login/")
    async def login():
        result = await discord_auth.create_session()
        return result

    @app.route("/logout/")
    async def logout():
        discord_auth.revoke()
        return redirect("/")

    @app.route("/callback/")
    async def callback():
        await discord_auth.callback()
        return redirect(url_for(".index"))

    @app.errorhandler(Unauthorized)
    async def redirect_unauthorized(e):
        return redirect(url_for("login"))

    @app.errorhandler(MissingMembership)
    async def render_missing_membership(e):
        return await render_template('unauthorized.html'), 401

    @app.route("/all_events/", methods=["GET"])
    @requires_membership
    async def all_events():
        return {'events': db.get_all_events()}

    @app.route('/upcoming_events/', defaults={'n': 4})
    @app.route("/upcoming_events/<n>")
    @requires_membership
    async def getLatestEvents(n=4):
        n = int(n)
        return {'events': db.get_upcoming_events(n)}

    @app.route("/event/")
    @app.route("/event/<event_id>", methods=["GET", "PUT", "POST", "DELETE"])
    @requires_membership
    async def event(event_id=None):
        event_id = int(event_id) if event_id else None

        if request.method == "GET":
            event = db.get_event(event_id)
            if event is None:
                await abort(404, "Event not found.")
            return event

        elif request.method == "PUT":
            event = db.get_event(event_id)
            if event is None:
                await abort(404, "Event not found.")
            event_data = await request.get_json()
            db.update_event(event_id, event_data)

        elif request.method == "POST":
            event_data = await request.get_json()
            db.update_event(event_data)

        elif request.method == "DELETE":
            db.delete_event(event_id)

    @app.route("/user/")
    @requires_membership
    async def get_user_info():
        user = await discord_auth.fetch_user()
        roles = bot.get_roles_of_user(user.id)
        role_names = [r.name for r in roles]

        return {
            'username': user.name,
            'avatar_url': user.avatar_url,
            'id': user.id,
            'roles': role_names,
            'admin': ('Roster' in role_names)
        }

    @app.route("/admin_test")
    @requires_role('Roster')
    async def admin_test():
        return "You are an admin!!!"

    @app.route("/admin_test_negative")
    @requires_role('Rooster')
    async def admin_test_negative():
        return "You are an admin!!!"

    @app.route("/")
    @requires_authorization
    async def index():
        x = await send_file('static/index.html')
        return x

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
