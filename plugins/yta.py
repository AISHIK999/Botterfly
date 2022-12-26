from os import remove
from subprocess import PIPE, Popen

from telethon import events
from telethon.tl.types import DocumentAttributeAudio

from plugins.commands import yta
from userbot import templar


# Download audio from YouTube
@templar.on(events.NewMessage(**yta))
async def yta(event):
    try:
        link = event.message.message.split(" ")[1] if event.message.message.split(" ")[
            1] else event.reply_to_message.message
    except IndexError:
        await event.edit(
            "Please provide a link to download.\nExample: `.yta https://www.youtube.com/watch?v=1234567890`")
        return

    await event.edit("`Downloading...`")
    process = Popen(["yt-dlp", "-o", f"{link}.mp3", link], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    await event.edit("`Sending...`")
    await event.client.send_file(event.chat_id, f"{link}.mp3",
                                 attributes=[DocumentAttributeAudio(duration=0, title="", performer="")])

    await event.edit("`Removing...`")
    remove(f"{link}.mp3")
    await event.delete()

    if stderr:
        await event.client.send_message(event.chat_id, f"Error: {stderr.decode('utf-8')}")
