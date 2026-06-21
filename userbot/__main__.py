import importlib

from telethon.errors import FloodWaitError

from plugins import All_PLUGINS
from userbot import botterfly, logger

for plugin in All_PLUGINS:
    importlib.import_module("plugins." + plugin)
    logger.info(f"Loaded plugin: {plugin}")

try:
    botterfly.start()
    logger.info("Botterfly is ready...")
    botterfly.run_until_disconnected()
except FloodWaitError as e:
    logger.error(f"Flood wait triggered, must wait {e.seconds}s before retrying")
except Exception:
    logger.exception("Botterfly crashed")
