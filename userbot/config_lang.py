import os
from logging import getLogger
from telethon import TelegramClient
from telethon.sessions import StringSession

# LOGS
LOGS = getLogger(__name__)

# LANGUAGE
LANGUAGE = os.environ.get("LANGUAGE", None)

if LANGUAGE:
    LANGUAGE = LANGUAGE.upper()
else:
    LANGUAGE = "DEFAULT"

if LANGUAGE not in ["EN", "TR", "AZ", "UZ", "DEFAULT"]:
    LOGS.info("[Dil]: Bilinməyən bir dil seçdiniz. Buna görə DEFAULT işlədilir.")
    LANGUAGE = "DEFAULT"

# TELEGRAM BOT
API_KEY = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", None)
STRING_SESSION = os.environ.get("STRING_SESSION", None)

if STRING_SESSION:
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    bot = TelegramClient("userbot", API_KEY, API_HASH)

# PLUGIN CHANNEL
PLUGINID = os.environ.get("PLUGIN_CHANNEL_ID", None)

if not PLUGINID:
    PLUGIN_CHANNEL_ID = "me"
else:
    PLUGIN_CHANNEL_ID = int(PLUGINID)
