import os
import requests
from userbot.events import register as silgi
from userbot import HEROKU_APIKEY, HEROKU_APPNAME



@silgi(outgoing=True, pattern=r"^.drestart$")
async def drestart(event):
    if not HEROKU_APIKEY or not HEROKU_APPNAME:
        return await event.edit("❌ `HEROKU_API_KEY` və `APP_NAME` dəyişənləri tapılmadı.")

    await event.edit("♻️ Dyno restart olunur...")

    url = f"https://api.heroku.com/apps/{HEROKU_APPNAME}/dynos"
    headers = {
        "User-Agent": "SilgiUserbot",
        "Authorization": f"Bearer {HEROKU_APIKEY}",
        "Accept": "application/vnd.heroku+json; version=3"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 202:
        await event.edit("✅ Heroku dyno uğurla restart edildi.")
    else:
        await event.edit(f"❌ Xəta baş verdi: {response.status_code} - {response.text}")
@silgi(dev=True, pattern=r"^.sdrestart$")
async def drestart(event):
    if not HEROKU_APIKEY or not HEROKU_APPNAME:
        return await event.reply("❌ `HEROKU_API_KEY` və `APP_NAME` dəyişənləri tapılmadı.")

    await event.reply("♻️ Dyno restart olunur...")

    url = f"https://api.heroku.com/apps/{HEROKU_APPNAME}/dynos"
    headers = {
        "User-Agent": "SilgiUserbot",
        "Authorization": f"Bearer {HEROKU_APIKEY}",
        "Accept": "application/vnd.heroku+json; version=3"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 202:
        await event.edit("✅ Heroku dyno uğurla restart edildi.")
    else:
        await event.edit(f"❌ Xəta baş verdi: {response.status_code} - {response.text}")