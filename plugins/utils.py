"""Shared helpers for plugins."""

import asyncio
import functools
import importlib
import inspect

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


def get_command_registry():
    """
    Build {command_name: help_text} by importing every plugin module and
    reading its COMMAND_NAME + the docstring of whichever function inside
    it is the event handler (decorated with @botterfly.on(...)).

    A plugin only needs to declare COMMAND_NAME = "foo" and write a normal
    docstring on its handler; nothing needs to be registered by hand and
    help text never goes stale relative to the code.
    """
    # Local import to dodge a circular import (plugins -> utils -> plugins)
    from plugins import All_PLUGINS

    registry = {}
    for plugin_name in All_PLUGINS:
        try:
            module = importlib.import_module("plugins." + plugin_name)
        except Exception:
            logger.exception(f"help: failed to inspect plugin '{plugin_name}'")
            continue

        command_name = getattr(module, "COMMAND_NAME", None)
        if not command_name:
            continue

        handler = None
        for _, obj in inspect.getmembers(module, inspect.iscoroutinefunction):
            if obj.__doc__:
                handler = obj
                break

        doc = inspect.cleandoc(handler.__doc__) if handler and handler.__doc__ else "No description available."
        registry[command_name] = doc

    return registry