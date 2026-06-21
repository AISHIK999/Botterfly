from telethon import events

from plugins.commands import hello
from plugins.utils import safe_handler
from userbot import botterfly

COMMAND_NAME = "hello"


@botterfly.on(events.NewMessage(**hello))
@safe_handler
async def send_hello(event):
    """
    Print 'Hello World!' That's it

    USAGE:
    $hello
    """
    await event.edit("Hello World!")
