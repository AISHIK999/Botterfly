from datetime import datetime

from telethon import events

from plugins.commands import ping as ping_pattern
from plugins.utils import safe_handler
from userbot import botterfly

COMMAND_NAME = "ping"


@botterfly.on(events.NewMessage(**ping_pattern))
@safe_handler
async def ping(event):
    """
    Returns latency value

    USAGE:
    $ping
    """
    start = datetime.now()
    await event.edit("`Pong!`")
    end = datetime.now()
    latency = (end - start).microseconds / 1000
    await event.edit(f"`Pong!\n{latency}ms`")
