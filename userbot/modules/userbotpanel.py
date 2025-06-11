from userbot import bot, HEROKU_APIKEY, HEROKU_APPNAME, SILGI_USER
from userbot.events import register
from userbot.cmdhelp import CmdHelp

PANEL_LINK = f"https://silgiuserbot.netlify.app/?APIKEY={HEROKU_APIKEY}&APPNAME={HEROKU_APPNAME}"

@register(outgoing=True, pattern=r"^\.panel$")
async def send_panel_to_saved(event):
    await event.edit(f"Sahibim: {SILGI_USER}\n📥 SilgiUserbot İdarəetmə Panel linki 'Saved Messages/Kayıtlı Mesajlar' bölməsinə göndərildi.")
    await bot.send_message("me", f"⚙️ Panel linki:\n[Bura bas]({PANEL_LINK})")

CmdHelp("panel").add_command(
    ".panel",
    None,
    "SilgiUserbot'un İdarəetmə Panel linkini göndərir"
).add()