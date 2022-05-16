from datetime import datetime

from telethon import events

from plugins.commands import ping
from userbot import templar


# Ping test
@templar.on(events.NewMessage(**ping))
async def ping(event):
    start = datetime.now()
    await event.edit("`Pong!`")
    end = datetime.now()
    latency = (end - start).microseconds / 1000
    await event.edit(f"`Pong!\n{latency}ms`")
