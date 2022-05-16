# Recruit the Templar

from userbot import templar
from plugins import All_PLUGINS
from private import All_PRIVATE_PLUGINS

import importlib

# Templar will complete all the objectives assigned to it
for plugin in All_PLUGINS:
    importlib.import_module("plugins." + plugin)

# Templar will also complete all the private assignments of his Lord
'''
If you want use some private plugins/modules, just create a directory named "private"
Then copy the __init__.py file from the "plugins" directory into it
At last keep all the plugins in the "private" directory, and the job is done
'''
for private_plugin in All_PRIVATE_PLUGINS:
    importlib.import_module("private." + private_plugin)

# Deus Vult
templar.start()
print("Templar is on duty...")

templar.run_until_disconnected()
