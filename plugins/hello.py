# A simple plugin that says "Hello World!"
# I used this to test whether the plugin system worked :)

from telethon import events
from userbot import templar
from plugins.commands import hello


@templar.on(events.NewMessage(**hello))
async def send_hello(event):
    await event.edit("Hello World!")
