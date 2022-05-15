from userbot import bot
from plugins import All_PLUGINS

import importlib

for plugin in All_PLUGINS:
    importlib.import_module("plugins." + plugin)

bot.start()

bot.run_until_disconnected()
