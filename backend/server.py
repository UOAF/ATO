import os
import json

from flask import Flask, redirect, url_for, send_from_directory, send_file, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from tinydb import TinyDB, Query, where

dbFile = os.path.join(os.path.dirname(__file__), 'db.json')
db = TinyDB(dbFile)


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = b"random bytes representing flask secret key"
# !! Only in development environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

# app.config["DISCORD_CLIENT_ID"] =     # Discord client ID.
# app.config["DISCORD_CLIENT_SECRET"] = ""                # Discord client secret.
# app.config["DISCORD_REDIRECT_URI"] = ""                 # URL to your callback endpoint.
# app.config["DISCORD_BOT_TOKEN"] = ""                    # Required to access BOT resources.

discord = DiscordOAuth2Session(app)


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/getEvents/")
@requires_authorization
def getEvents():
    eventTable = db.table('Events')
    eventsList = eventTable.all()
    return {'events': eventsList}

@app.route("/getLatestEvents/")
@requires_authorization
def getLatestEvents():
    eventTable = db.table('Events')
    eventsList = eventTable.all()
    return {'events': eventsList[-4:]}

@app.route("/updateEvent/",methods=["PUT"])
@requires_authorization
def updateEvent():
    eventUpdate = request.json
    eventName = eventUpdate["EventName"]
    eventsTable = db.table('Events')
    dbQuery = Query()
    eventToUpdate = eventsTable.search(dbQuery.EventName == eventName)[0]
    #eventsTable.insert(eventUpdate)
    #data_as_json = request.get_json()
    #events.insert(data_as_json)
    return {}

@app.route("/putEvent/",methods=["PUT"])
@requires_authorization
def putEvent():
    events = db.table('Events')
    data_as_json = request.get_json()
    eventName = data_as_json["EventName"]
    dbQuery = Query()
    checkEventName = events.search(dbQuery.EventName == eventName)
    if (len (checkEventName) > 0):
        print (f"ERROR: {eventName} already found, not inserting.")
        return (f"ERROR: {eventName} already found, not inserting")
    events.insert(data_as_json)
    return data_as_json

@app.route("/user/")
@requires_authorization
def get_user_info():
    user = discord.fetch_user()
    return {
        'username': user.name,
        'avatar_url': user.avatar_url,
        'id': user.id
    }

@app.route("/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return send_file('static/index.html')


if __name__ == "__main__":
    app.run()
