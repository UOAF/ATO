import os

from flask import Flask, redirect, url_for, send_from_directory
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

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


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))
	
@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()

    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <script src="/static/index-bundle.js"></script>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""


if __name__ == "__main__":
    app.run()
