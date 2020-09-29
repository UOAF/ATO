import os
import json
import logging

from flask import Flask, redirect, url_for, send_from_directory
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

from tinydb import TinyDB, Query

dbFile = os.path.join(os.path.dirname(__file__), 'db.json')
db = TinyDB(dbFile)
events = db.table('Events')
events.insert(
{
    "EventName": "Test Event",
    "ShortDescription": "Does this thing even work?",
    "MissionDescription": "We are testing shit. And mostly breaking shit.",
    "Date": "2012-04-23",
    "StartTime": "1800Z",
    "EndTime": "2000Z",
    "Creator": "Krause#5727",
    "Controllers": [
        {
            "Type": "ATC",
            "Slots": [
                {
                    "SlotName": "Ramat David Tower",
                    "Players": [
                        {
                            "Player:": "Krause#5727",
                            "Remarks": "Gonna crash all you fuckers"
                        }
                    ]
                }
            ]
        }
    ],
    "Packages": [
        {
            "Commander": "Krause",
            "Flights": [
                {
                    "FlightName": "Satan 1-1",
                    "Tasking": "DEAD",
                    "Airframe": "F-16CM Blk50",
                    "Airbase": "Ramat David",
                    "Slots": [
                        {
                            "SlotName": "Satan 1-1",
                            "Players": [
                                {
                                    "Player:": "Krause#5727",
                                    "Type": "Pilot",
                                    "Remarks": "Sucks at agm-88"
                                },
                                {
                                    "Player:": "R2D2#5727",
                                    "Type": "Backseat",
                                    "Remarks": "Weird f-16D that snuck in"
                                }
                            ]
                        },
                        {
                            "SlotName": "Satan 1-2",
                            "Players": [
                                {
                                    "Player:": "Abe#6969",
                                    "Remarks": ""
                                }
                            ]
                        },
                        {
                            "SlotName": "Satan 1-3",
                            "Players": [
                                {
                                    "Player:": "Razgriz#911",
                                    "Remarks": "Likes to smell butts"
                                }
                            ]
                        },
                        {
                            "SlotName": "Satan 1-4",
                            "Players": [
                                {
                                    "Player:": "Floppy#6969",
                                    "Remarks": "Yolo growler"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
)
for item in db:
    print(item)

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = b"random bytes representing flask secret key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

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

@app.route("/getEvents/")
@requires_authorization
def getEvents():
    eventTable = db.table('Events')
    eventsList = eventTable.all()
    return {'events': eventsList}


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))
	
@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <div id="app">
                <div class="container">
                    <div class="row my-5 justify-content-center">
                        <div class="col-sm-6">
                            <h1 class="text-center">{{{{ message }}}}</h1>
                            <hello-component />
                        </div>
                    </div>
                </div>
            </div>
            <script src="/static/app.min.js"></script>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""


if __name__ == "__main__":
    app.run()
