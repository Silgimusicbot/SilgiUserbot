import os
import requests
from userbot.events import register as silgi

HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
APP_NAME = os.environ.get("APP_NAME")

@silgi(outgoing=True, pattern=r"^.drestart$")
async def drestart(event):
    if not HEROKU_API_KEY or not APP_NAME:
        return await event.edit("❌ `HEROKU_API_KEY` və `APP_NAME` dəyişənləri tapılmadı.")

    await event.edit("♻️ Dyno restart olunur...")

    url = f"https://api.heroku.com/apps/{APP_NAME}/dynos"
    headers = {
        "User-Agent": "SilgiUserbot",
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 202:
        await event.edit("✅ Heroku dyno uğurla restart edildi.")
    else:
        await event.edit(f"❌ Xəta baş verdi: {response.status_code} - {response.text}")