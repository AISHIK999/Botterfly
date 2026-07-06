from telethon import events

from plugins.commands import id
from plugins.utils import safe_handler
from userbot import botterfly

COMMAND_NAME = "id"


@botterfly.on(events.NewMessage(**id))
@safe_handler
async def send_id(event):
    """
    Returns user, message and chat ID

    USAGE:
    $id
    """
    await event.edit(
        f"User ID: {event.sender_id}\nMessage ID: {event.id}\nChat ID: {event.chat_id}"
    )
