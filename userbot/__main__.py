# Recruit the Templar

from userbot import templar
from plugins import All_PLUGINS

import importlib

# Templar will complete all the objectives assigned to it
for plugin in All_PLUGINS:
    importlib.import_module("plugins." + plugin)

# Deus Vult
templar.start()
print("Templar is on duty...")

templar.run_until_disconnected()
