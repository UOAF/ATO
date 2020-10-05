import functools

from flask_discord import DiscordOAuth2Session, requires_authorization, current_app, exceptions as disc_exceptions
#from flask import exceptions

class MissingMembership(disc_exceptions.HttpException):
    "Exception when required guild membership is missing."

def user_is_member_of(guild_id):
    user = current_app.discord.fetch_user()
    guilds = current_app.discord.fetch_guilds()
    return any(g.id == guild_id for g in guilds)

def requires_membership(guild_id):
    """Decorator to be used to enforce authorization. Top-level flask server needs
    to register an error handler for a MissingMembership exception to inform the 
    user that they're not a member of the required guild.
    """
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            # Internals of this patterened on flask_discord.requires_authorization.
            if not current_app.discord.authorized:
                raise disc_exceptions.Unauthorized()
            if not user_is_member_of(guild_id):
                raise MissingMembership(guild_id)
            return view(*args, **kwargs)
        return wrapper
    return decorator
