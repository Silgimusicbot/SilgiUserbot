from telethon import events
from userbot import bot
from userbot.modules.sql_helper import chatbot_sql as db
from userbot.events import register

@register(outgoing=True, pattern="^.chatbot (on|off)$")
async def toggle_chatbot(event):
    """ChatBot-u aktivləşdir və ya deaktivləşdir"""
    cmd = event.pattern_match.group(1).lower()
    chat_id = event.chat_id

    if cmd == "on":
        db.activate_chat(chat_id)
        await event.edit("**ChatBot bu söhbət üçün aktiv edildi.**")
    elif cmd == "off":
        db.deactivate_chat(chat_id)
        await event.edit("**ChatBot bu söhbət üçün deaktiv edildi.**")

@register(incoming=True)
async def chatbot_main(event):
    chat_id = event.chat_id
    if not db.is_chat_active(chat_id):
        return  
    message_text = event.text.strip().lower()
    if event.sender_id == (await bot.get_me()).id:
        return
    answer = db.get_answer(message_text)
    if answer:
        await event.reply(answer)
    elif event.is_reply:
        replied = await event.get_reply_message()
        if replied and replied.sender_id != (await bot.get_me()).id:
            original = replied.text.strip().lower()
            db.add_pair(original, message_text)