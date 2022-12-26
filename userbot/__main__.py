# Recruit the Templar

import importlib

from plugins import All_PLUGINS
from userbot import templar

# Templar will complete all the objectives assigned to it
for plugin in All_PLUGINS:
    importlib.import_module("plugins." + plugin)

# Deus Vult
templar.start()
print("Templar is on duty...")

templar.run_until_disconnected()
