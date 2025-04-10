import requests
from googletrans import Translator
from telethon.tl.types import User
from userbot import CMD_HELP, LOGS
from userbot.events import register
from userbot.modules.sql_helper.chatbot_sql import ids, userbot, chatbot

translator = Translator()
LANGUAGE = "az"

url = "https://apitede.herokuapp.com/api/chatbot?message={message}"


async def words(message):
    bir_link = url.format(message=message)
    try:
        data = requests.get(bir_link)
        if data.status_code == 200:
            return (data.json())["msg"]
        LOGS.info("ERROR: Chatbot API işləmir, @SilgiUB-a məlumat verin.")
    except Exception as e:
        LOGS.info(str(e))


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
            chatbot(chat_id)
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
    if not ids (event.chat_id):
        return
    if not isinstance(sender, User):
        return
    if event.text:
        rep = await words(event.message.message)
        tr = translator.translate(rep, LANGUAGE)
        if tr:
            await event.reply(tr.text)