# Getting the Templar in gear
# Configs of the user provided to the bot to function properly

import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
string = os.environ['STRING_SESSION']

templar = TelegramClient(StringSession(string), api_id, api_hash)
