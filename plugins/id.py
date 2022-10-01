from telethon import events
from plugins.commands import id
from userbot import templar


# Plugin to display IDs of user, message and chat
@templar.on(events.NewMessage(**id))
async def send_id(event):
    await event.edit(f"User ID: {event.sender_id}\nMessage ID: {event.id}\nChat ID: {event.chat_id}")
