import importlib

from plugins import All_PLUGINS
from userbot import botterfly


for plugin in All_PLUGINS:
    importlib.import_module("plugins." + plugin)

# Fly high...
botterfly.start()
print("Botterfly is ready...")

botterfly.run_until_disconnected()
