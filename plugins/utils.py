"""Shared helpers for plugins."""

import asyncio
import functools

from telethon.errors import FloodWaitError

from userbot import logger


def safe_handler(func):
    """Wrap an event handler so FloodWaitError and unexpected exceptions
    are logged instead of silently killing the handler / crashing the bot."""

    @functools.wraps(func)
    async def wrapper(event, *args, **kwargs):
        try:
            return await func(event, *args, **kwargs)
        except FloodWaitError as e:
            logger.warning(f"{func.__name__}: flood wait, sleeping {e.seconds}s")
            await asyncio.sleep(e.seconds)
        except Exception:
            logger.exception(f"{func.__name__}: unhandled error")
            try:
                await event.edit(f"`Error in {func.__name__}, check logs`")
            except Exception:
                pass

    return wrapper
