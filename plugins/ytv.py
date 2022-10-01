from os import remove
from subprocess import PIPE, Popen

from telethon import events
from telethon.tl.types import DocumentAttributeVideo

from plugins.commands import ytv
from userbot import templar


@templar.on(events.NewMessage(**ytv))
async def ytv(event):
    try:
        link = event.message.message.split(" ")[1] if event.message.message.split(" ")[1] else event.reply_to_message.message
    except IndexError:
        await event.edit("Please provide a link to download.\nExample: `.ytv https://www.youtube.com/watch?v=1234567890`")
        return

    doc = True if "-d" in event.message.message.split(" ") else False

    await event.edit("`Downloading...`")
    process = Popen(["yt-dlp", "-o", f"{link}.mp4", link], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    await event.edit("`Sending...`")
    if doc:
        await event.client.send_file(event.chat_id, f"{link}.mp4", force_document=True)
    else:
        await event.client.send_file(event.chat_id, f"{link}.mp4", attributes=[DocumentAttributeVideo(duration=0, w=0, h=0)])

    await event.edit("`Removing...`")
    remove(f"{link}.mp4")
    await event.delete()

    if stderr:
        await event.client.send_message(event.chat_id, f"Error: {stderr.decode('utf-8')}")
