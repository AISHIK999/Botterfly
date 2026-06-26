# Botterfly is getting ready

import logging
import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

_handlers = [logging.StreamHandler()]
_log_file = os.environ.get("LOG_FILE", "")
if _log_file:
    _handlers.append(logging.FileHandler(_log_file, encoding="utf-8"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=os.environ.get("LOG_LEVEL", "INFO"),
    handlers=_handlers,
)
# Telethon's own logger is noisy at INFO, quiet it down
logging.getLogger("telethon").setLevel(logging.WARNING)

logger = logging.getLogger("botterfly")

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
string = os.environ["STRING_SESSION"]

botterfly = TelegramClient(StringSession(string), api_id, api_hash)
