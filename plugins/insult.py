import random
from telethon import events

from plugins.commands import insult
from userbot import templar


# Spits random insults. Insults are stored in 'resources,insults'
# You can add your own insults by adding them to the list
# I am in no way responsible if you do something stupid by using this in a heated argument
@templar.on(events.NewMessage(**insult))
async def insult(event):
    lines = open("./resources/insult").read().splitlines()
    chosen_insult = random.choice(lines)
    await event.edit(chosen_insult)
