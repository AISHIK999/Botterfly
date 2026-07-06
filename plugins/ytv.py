from shutil import rmtree
from subprocess import PIPE, Popen
from tempfile import mkdtemp
from uuid import uuid4

from telethon import events

from plugins.commands import ytv
from plugins.utils import safe_handler
from userbot import botterfly

COMMAND_NAME = "ytv"


@botterfly.on(events.NewMessage(**ytv))
@safe_handler
async def ytv(event):
    """
    Download a youtube video in mp4 format

    USAGE:
    $ytv <youtube link>
    (or reply to a message containing the link with $ytv)
    """
    parts = event.message.message.split(maxsplit=1)
    link = parts[1] if len(parts) > 1 else None
    if not link and event.is_reply:
        replied = await event.get_reply_message()
        link = replied.message if replied else None

    if not link:
        await event.edit(
            "Please provide a link to download.\n"
            "Example: `.ytv https://www.youtube.com/watch?v=1234567890`"
        )
        return

    workdir = mkdtemp(prefix="ytv_")
    filename = f"{uuid4().hex}.mp4"
    filepath = f"{workdir}/{filename}"

    await event.edit("`Downloading...`")
    process = Popen(
        [
            "yt-dlp",
            "-f",
            "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
            "--merge-output-format",
            "mp4",
            "-o",
            filepath,
            link,
        ],
        stdout=PIPE,
        stderr=PIPE,
        cwd=workdir,
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        await event.edit(f"`Download failed:\n{stderr.decode('utf-8')[:500]}`")
        rmtree(workdir, ignore_errors=True)
        return

    await event.edit("`Sending...`")
    try:
        await event.client.send_file(event.chat_id, filepath)
    finally:
        rmtree(workdir, ignore_errors=True)

    await event.delete()
