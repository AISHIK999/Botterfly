from speedtest import Speedtest
from telethon import events

from plugins.commands import speed
from userbot import templar


# Speedtest. Using the 'speedtest-cli' library since 'speedtest' does not work on Python 3.8 and above
@templar.on(events.NewMessage(**speed))
async def speed(event):
    await event.edit("`Wait a moment my Lord, while I run the speedtest...`")
    speed_test = Speedtest()
    download_speed = speed_test.download() / 1048576
    upload_speed = speed_test.upload() / 1048576 if "-u" in event.text else None
    speedtest_result = f"`Results:\nDownload speed: {download_speed:.2f} Mbps\n`"
    if upload_speed is not None:
        speedtest_result += f"`Upload speed: {upload_speed:.2f} Mbps`"
    await event.edit(speedtest_result)
