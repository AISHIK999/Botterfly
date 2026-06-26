from os import remove
from subprocess import PIPE, Popen
from uuid import uuid4

from telethon import events
from telethon.tl.types import DocumentAttributeAudio

from plugins.commands import yta
from plugins.utils import safe_handler
from userbot import botterfly

COMMAND_NAME = "yta"


@botterfly.on(events.NewMessage(**yta))
@safe_handler
async def yta(event):
    """
    Download a youtube video in mp3 format

    USAGE:
    $yta <youtube link>
    (or reply to a message containing the link with $yta)
    """
    parts = event.message.message.split(maxsplit=1)
    link = parts[1] if len(parts) > 1 else None
    if not link and event.is_reply:
        replied = await event.get_reply_message()
        link = replied.message if replied else None

    if not link:
        await event.edit(
            "Please provide a link to download.\n"
            "Example: `.yta https://www.youtube.com/watch?v=1234567890`"
        )
        return

    filename = f"{uuid4().hex}.mp3"

    await event.edit("`Downloading...`")
    process = Popen(
        ["yt-dlp", "-x", "--audio-format", "mp3", "-o", filename, link],
        stdout=PIPE,
        stderr=PIPE,
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        await event.edit(f"`Download failed:\n{stderr.decode('utf-8')[:500]}`")
        return

    await event.edit("`Sending...`")
    await event.client.send_file(
        event.chat_id,
        filename,
        attributes=[DocumentAttributeAudio(duration=0, title="", performer="")],
    )

    remove(filename)
    await event.delete()
