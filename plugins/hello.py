from telethon import events
from userbot import bot


@bot.on(events.NewMessage(pattern='.hello()'))
async def sendHello(event):
    await event.edit("Hello World!")
