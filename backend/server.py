import os

from flask import Flask, redirect, url_for, send_from_directory, send_file
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

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
