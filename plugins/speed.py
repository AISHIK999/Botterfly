import asyncio

from speedtest import Speedtest
from telethon import events

from plugins.commands import speed as speed_pattern
from plugins.utils import safe_handler
from userbot import botterfly

COMMAND_NAME = "speed"


def _run_speedtest(want_upload):
    speed_test = Speedtest()
    download_speed = speed_test.download() / 1048576
    upload_speed = speed_test.upload() / 1048576 if want_upload else None
    return download_speed, upload_speed


# Using the 'speedtest-cli' library since 'speedtest' does not work on Python 3.8 and above
@botterfly.on(events.NewMessage(**speed_pattern))
@safe_handler
async def speed(event):
    """
    Returns host bandwidth

    USAGE:
    $speed (add -u to also test upload)
    """
    await event.edit("`Wait a moment my Lord, while I run the speedtest...`")
    want_upload = "-u" in event.text
    download_speed, upload_speed = await asyncio.to_thread(_run_speedtest, want_upload)
    speedtest_result = f"`Results:\nDownload speed: {download_speed:.2f} Mbps\n`"
    if upload_speed is not None:
        speedtest_result += f"`Upload speed: {upload_speed:.2f} Mbps`"
    await event.edit(speedtest_result)
