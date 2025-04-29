import asyncio
import os
import heroku3
from telethon import TelegramClient
from telethon.tl.functions.contacts import UnblockRequest
from random import randint
from userbot import BOT_TOKEN, HEROKU_APIKEY, HEROKU_APPNAME, bot
from userbot.modules.asistant import me

Silgi = os.path.join(os.getcwd(), "userbot", "SilgiUserbotlogo.jpg")

def heroku_qurulum():
    if HEROKU_APIKEY and HEROKU_APPNAME:
        heroku_conn = heroku3.from_key(HEROKU_APIKEY)
        app = heroku_conn.app(HEROKU_APPNAME)
        config = app.config()
        return app, config
    return None, None

async def get_botfather_message():
    bot_father = "@BotFather"
    for _ in range(10):
        await asyncio.sleep(1)
        messages = await bot.get_messages(bot_father, limit=2)
        for msg in messages:
            if "Use this token to access the HTTP API:" in msg.text:
                token = msg.text.split("`")[1] if "`" in msg.text else msg.text.split("\n")[2]
                return token
    return None

async def silgiassistantbot(app, config):
    bot_father = "@BotFather"
    await bot(UnblockRequest(bot_father))

    me = await bot.get_me()
    bot_name = f"{me.first_name} SilgiUserbot Assistant"
    username = f"silgiub{randint(1, 1000)}bot" if me.username else f"silgi{str(me.id)[5:]}bot"

    await bot.send_message(bot_father, "/newbot")
    await asyncio.sleep(2)
    await bot.send_message(bot_father, bot_name)
    await asyncio.sleep(2)
    await bot.send_message(bot_father, username)

    token = await get_botfather_message()

    if not token:
        await bot.send_message("me", "❌ Bot yaradılmadı. @BotFather-dən əl ilə cəhd edin.")
        return

    await bot.send_message("me", f"✅ Yeni Assistant bot yaradıldı\nİşlətmək üçün .help yazın: @{username}")

    await bot.send_message(bot_father, "/setinline")
    await asyncio.sleep(1)
    await bot.send_message(bot_father, f"@{username}")
    await asyncio.sleep(1)
    await bot.send_message(bot_father, "kömek yazın")
    await asyncio.sleep(3)

    await bot.send_message(bot_father, "/setabouttext")
    await asyncio.sleep(1)
    await bot.send_message(bot_father, f"@{username}")
    await asyncio.sleep(1)
    await bot.send_message(bot_father, f"{me.first_name} üçün [SilgiUserbot](t.me/silgiub) tərəfindən hazırlanmış assistant botuyam")
    await asyncio.sleep(3)

    await bot.send_message(bot_father, "/setdescription")
    await asyncio.sleep(1)
    await bot.send_message(bot_father, f"@{username}")
    await asyncio.sleep(1)
    await bot.send_message(bot_father, f"🖥 Sahib ~ {me.first_name} \n\n Created By ~ @SilgiUB ")
    await asyncio.sleep(2)
    await bot.send_message(bot_father, "/setuserpic")
    await asyncio.sleep(2)
    await bot.send_message(bot_father, f"@{username}")
    await asyncio.sleep(1)
    await bot.send_file(bot_father, Silgi)
    config["BOT_TOKEN"] = token
    config["BOT_USERNAME"] = username
async def main():
    app, config = heroku_qurulum()
    if not app:
        print("❌ Heroku API açarı və ya app adı tapılmadı.")
        return
    await silgiassistantbot(app, config)

if __name__ == "__main__":
    asyncio.run(main())
