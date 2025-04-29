
from userbot import ASYNC_POOL, SPOTIFY_DC, G_DRIVE_CLIENT_ID, lastfm, LYDIA_API_KEY, YOUTUBE_API_KEY, OPEN_WEATHER_MAP_APPID, AUTO_PP, REM_BG_API_KEY, OCR_SPACE_API_KEY, PM_AUTO_BAN, BOTLOG_CHATID, SILGI_VERSION
from userbot.events import register
from userbot import CMD_HELP, tgbot
from telethon import version
from platform import python_version
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("status")

# ████████████████████████████████ #

def durum(s):
    if s == None:
        return "⛔"
    else:
        if s == False:
            return "⛔"
        else:
            return "✅"

@register(outgoing=True, pattern="^.durum|^.status")
async def durums(event):

    await event.edit(f"""
**{LANG['OK']} ✅**

`Inline Bot:` `{durum(tgbot)}`
`Spotify:` `{durum(SPOTIFY_DC)}`
`GDrive:` `{durum(G_DRIVE_CLIENT_ID)}`
`LastFm:` `{durum(lastfm)}`
`Lydia:` `{durum(LYDIA_API_KEY)}`
`OpenWeather:` `{durum(OPEN_WEATHER_MAP_APPID)}`
`AutoPP:` `{durum(AUTO_PP)}`
`RemoveBG:` `{durum(REM_BG_API_KEY)}`
`OcrSpace:` `{durum(OCR_SPACE_API_KEY)}`
`Pm AutoBan:` `{durum(PM_AUTO_BAN)}`
`BotLog:` `{durum(BOTLOG_CHATID)}`
`Plugin:` `{LANG['PERMAMENT']}`

**Python {LANG['VERSION']}:** `{python_version()}`
**TeleThon {LANG['VERSION']}:** `{version.__version__}`
**{LANG['PLUGIN_COUNT']}:** `{len(CMD_HELP)}`
**⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ {LANG['VERSION']}:** `{SILGI_VERSION}`
    """)

CmdHelp('status').add_command(
    'status', None, (LANG['STS'])
).add()
