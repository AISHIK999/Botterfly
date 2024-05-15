from telethon import events

from plugins.commands import help, trigger
from userbot import templar

tr = trigger[-1]
help_text = f"""
Available commands:

`{tr}hello`: Print 'Hello World!' That's it

`{tr}help`: This

`{tr}id`: Returns user, message and chat ID

`{tr}insult`: Returns random insult

`{tr}ping`: Returns latency value

`{tr}speed`: Returns host bandwidth

`{tr}yta`: Download a youtube video in mp3 format

`{tr}ytv`: Download a youtube video in mp4 format
"""

@templar.on(events.NewMessage(**help))
async def send_help(event):
    await event.edit("User manual has been forwarded to 'Saved Messages'")
    await event.client.send_message('me', help_text)
