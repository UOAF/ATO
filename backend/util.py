import logging
import functools
import asyncio
from quart import current_app as app
from quart_discord import DiscordOAuth2Session, requires_authorization, \
    exceptions as disc_exceptions, current_app
from datetime import datetime

log = logging.getLogger(__name__)


class MissingMembership(disc_exceptions.HttpException):
    "Exception when required guild membership is missing."


def get_guild_id():
    try:
        return app.config['ATO_PRIMARY_GUILD_ID']
    except KeyError:
        raise ValueError(
            "You need to set ATO_PRIMARY_GUILD_ID in the app config.")


async def user_is_member_of(guild_id):
    log.debug(f"users cache is {current_app.discord.users_cache}")
    user = await current_app.discord.fetch_user()
    guilds = user.guilds
    if guilds is None:
        log.debug("guilds is None, fetching")
        guilds = await user.fetch_guilds()
    return any(g.id == guild_id for g in guilds)


def requires_membership(view):
    """Decorator to be used to enforce authorization. Top-level flask server needs
    to register an error handler for a MissingMembership exception to inform the 
    user that they're not a member of the required guild.
    """
    @functools.wraps(view)
    async def wrapper(*args, **kwargs):
        guild_id = get_guild_id()
        # Internals of this patterened on flask_discord.requires_authorization.
        if not current_app.discord.authorized:
            raise disc_exceptions.Unauthorized()
        if not await user_is_member_of(guild_id):
            raise MissingMembership(guild_id)
        return await view(*args, **kwargs)
    return wrapper


_DATETIME_FORMAT_STR = '%Y-%m-%dT%H:%M:%S.%fZ'
def json_to_datetime(json_timestamp):
    return datetime.strptime(json_timestamp, _DATETIME_FORMAT_STR)

def datetime_to_json(dt_obj):
    return dt_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
