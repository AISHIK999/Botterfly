# A simple plugin that says "Hello World!"
# I used this to test whether the plugin system worked :)

from telethon import events

from plugins.commands import hello
from plugins.utils import safe_handler
from userbot import botterfly


@botterfly.on(events.NewMessage(**hello))
@safe_handler
async def send_hello(event):
    await event.edit("Hello World!")
