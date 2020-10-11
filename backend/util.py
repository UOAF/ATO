import logging
import functools
import asyncio
from quart import current_app as app
from quart_discord import DiscordOAuth2Session, requires_authorization, \
    exceptions as disc_exceptions, current_app
from datetime import datetime

import threading

log = logging.getLogger(__name__)


class AsioLockWrapper(object):

    def __init__(self):
        self._lock = None
        self._loop = None

    def create(self):
        self._lock = asyncio.Lock()
        self._loop = self._lock._loop

    async def acquire(self):
        assert(self._lock is not None)
        await self._lock.acquire()

    def release(self):
        assert(self._lock is not None)
        self._lock.release()

    def __repr__(self):
        return repr(self._lock)

    def locked(self):
        """Return True if lock is acquired."""
        return self._lock.locked()

    def _wake_up_first(self):
        return self._wake_up_first()

    async def __aenter__(self):
        await self.acquire()
        # We have no use for the "as ..."  clause in the with
        # statement for locks.
        return None

    async def __aexit__(self, exc_type, exc, tb):
        self.release()


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


def requires_membership(lock):
    """Decorator to be used to enforce authorization. Top-level flask server
    needs to register an error handler for a MissingMembership exception to
    inform the user that they're not a member of the required guild.
    """
    def decorator(view):
        @functools.wraps(view)
        async def wrapper(*args, **kwargs):
            async with lock:
                guild_id = get_guild_id()
                # Internals of this patterened on
                # flask_discord.requires_authorization.
                if not current_app.discord.authorized:
                    raise disc_exceptions.Unauthorized()
                if not await user_is_member_of(guild_id):
                    raise MissingMembership(guild_id)
                return await view(*args, **kwargs)
        return wrapper
    return decorator


_DATETIME_FORMAT_STR = '%Y-%m-%dT%H:%M:%S.%fZ'


def json_to_datetime(json_timestamp):
    return datetime.strptime(json_timestamp, _DATETIME_FORMAT_STR)


def datetime_to_json(dt_obj):
    return dt_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
