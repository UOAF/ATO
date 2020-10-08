import functools
import asyncio

import logging
log = logging.getLogger(__name__)

from quart_discord import DiscordOAuth2Session, requires_authorization, current_app, exceptions as disc_exceptions
#from flask import exceptions

class MissingMembership(disc_exceptions.HttpException):
    "Exception when required guild membership is missing."

async def user_is_member_of(guild_id):
    log.debug(f"users cache is {current_app.discord.users_cache}")
    user = await current_app.discord.fetch_user()
    guilds = user.guilds
    if guilds is None:
        log.debug("guilds is None, fetching")
        guilds = await user.fetch_guilds()
    return any(g.id == guild_id for g in guilds)

def requires_membership(guild_id):
    """Decorator to be used to enforce authorization. Top-level flask server needs
    to register an error handler for a MissingMembership exception to inform the 
    user that they're not a member of the required guild.
    """
    def decorator(view):
        @functools.wraps(view)
        async def wrapper(*args, **kwargs):
            # Internals of this patterened on flask_discord.requires_authorization.
            if not current_app.discord.authorized:
                raise disc_exceptions.Unauthorized()
            if not await user_is_member_of(guild_id):
                raise MissingMembership(guild_id)
            return await view(*args, **kwargs)
        return wrapper
    return decorator
