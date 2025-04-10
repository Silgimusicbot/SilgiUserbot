import requests
from deep_translator import GoogleTranslator
from telethon.tl.types import User
from userbot import CMD_HELP, LOGS
from userbot.events import register
from userbot.modules.sql_helper.chatbot_sql import ids, userbot, chatbot as deactivate_bot

LANGUAGE = "az"

url = "https://apitede.herokuapp.com/api/chatbot?message={message}"


async def words(message):
    bir_link = url.format(message=message)
    try:
        data = requests.get(bir_link)
        if data.status_code == 200:
            json_data = data.json()
            if "msg" in json_data:
                return json_data["msg"]
            else:
                LOGS.info("ERROR: 'msg' açarı tapılmadı.")
        else:
            LOGS.info(f"ERROR: API cavab statusu {data.status_code}")
    except Exception as e:
        LOGS.info(f"Chatbot API Error: {str(e)}")
    return None


async def active(event):
    status = event.pattern_match.group(1).lower()
    chat_id = event.chat_id
    if status == "on":
        if not ids(chat_id):
            userbot(chat_id)
            return await event.edit("**ChatBot Uğurla Aktiv edildi!**")
        await event.edit("ChatBot Artıq Aktivləşdirilib.")
    elif status == "off":
        if ids(chat_id):
            deactivate_bot(chat_id)
            return await event.edit("**ChatBot Uğurla Deaktiv edildi!**")
        await event.edit("ChatBot Deaktivdir.")
    else:
        await event.edit("**İşlədilişi:** `.chatbot` <on/off>")


@register(outgoing=True, pattern="^.chatbot(?: |$)(.*)")
async def on_off(event):
    await active(event)


@register(incoming=True, func=lambda e: (e.mentioned))
async def chatbot(event):
    sender = await event.get_sender()
    if not ids(event.chat_id):
        return
    if not isinstance(sender, User):
        return
    if event.text:
        rep = await words(event.message.message)
        if rep:
            try:
                translated = GoogleTranslator(source='auto', target=LANGUAGE).translate(rep)
                await event.reply(translated)
            except Exception as e:
                LOGS.info(f"Tərcümə zamanı xəta: {str(e)}")
        else:
            LOGS.info("Boş cavab alındı, tərcümə olunmadı.")