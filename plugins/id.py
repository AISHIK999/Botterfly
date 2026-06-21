from telethon import events

from plugins.commands import id
from plugins.utils import safe_handler
from userbot import botterfly


# Plugin to display IDs of user, message and chat
@botterfly.on(events.NewMessage(**id))
@safe_handler
async def send_id(event):
    await event.edit(
        f"User ID: {event.sender_id}\nMessage ID: {event.id}\nChat ID: {event.chat_id}"
    )
