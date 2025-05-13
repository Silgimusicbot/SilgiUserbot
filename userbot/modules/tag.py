import time
import requests
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from asyncio import sleep
from userbot import CMD_HELP, bot, WHITELIST
from userbot.events import register
from userbot.cmdhelp import CmdHelp

ADMINS = [7589331363, 7287936548, 6436992668]

tag_active = {}
@register(outgoing=True, pattern="^.5tag(?: |$)(.*)")
async def tag_five(event):
    
    if event.fwd_from:
        return
    
    message = event.pattern_match.group(1) or ""  
    chat = await event.get_input_chat()
    
    mentions = []
    async for user in bot.iter_participants(chat):
        mentions.append(f"[{user.first_name}](tg://user?id={user.id})")

        if len(mentions) == 5: 
            await event.client.send_message(event.chat_id, " ".join(mentions) + f" {message}")
            mentions = []  
            await sleep(2)  


    if mentions:
        await event.client.send_message(event.chat_id, " ".join(mentions) + f" {message}")

    await event.delete()
@register(outgoing=True, pattern="^.tagall$")
async def tag_all(event):
    chat_id = event.chat_id
    tag_active[chat_id] = True
    mentions = "@tag"
    chat = await event.get_input_chat()

    try:
        async for x in event.client.iter_participants(chat):
            if not tag_active.get(chat_id, False):
                await event.respond("Tagging dayandırıldı.")
                return
            if x.id in ADMINS:
                continue  
            mentions += f"[\u2063](tg://user?id={x.id})"
            if len(mentions) > 4000: 
                await event.respond(mentions)
                mentions = "@tag"
                await sleep(1)
        if mentions.strip() != "@tag":
            await event.respond(mentions)
    except Exception as e:
        await event.respond(f"Xəta baş verdi: {str(e)}")
    finally:
        await event.delete()

@register(outgoing=True, pattern="^.tagadmin(?: |$)(.*)")
async def tag_admins(event):
    chat_id = event.chat_id
    tag_active[chat_id] = True
    text = event.pattern_match.group(1)
    chat = await event.get_input_chat()

    try:
        async for admin in event.client.iter_participants(chat, filter=ChannelParticipantsAdmins):
            if not tag_active.get(chat_id, False):
                await event.respond("Tagging dayandırıldı.")
                return
            if admin.id in ADMINS:
                continue  
            mention = f"[{admin.first_name}](tg://user?id={admin.id}) {text}"
            await event.respond(mention)
            await sleep(1)
    except Exception as e:
        await event.respond(f"Xəta baş verdi: {str(e)}")
    finally:
        await event.delete()

@register(outgoing=True, pattern="^.tag(?: |$)(.*)")
async def tag_one_by_one(event):
    chat_id = event.chat_id
    tag_active[chat_id] = True
    seasons = event.pattern_match.group(1) if event.pattern_match.group(1) else ""

    chat = await event.get_input_chat()
    await event.delete()
    try:
        async for i in event.client.iter_participants(chat):
            if not tag_active.get(chat_id, False):
                await event.respond("Tagging dayandırıldı.")
                return
            if i.id in ADMINS:
                continue  
            await event.client.send_message(chat_id, f"[{i.first_name}](tg://user?id={i.id}) {seasons}")
            await sleep(1.9)
    except Exception as e:
        await event.respond(f"Xəta baş verdi: {str(e)}")

@register(outgoing=True, pattern="^.stoptag$")
async def stop_tag(event):
    chat_id = event.chat_id
    tag_active[chat_id] = False
    await event.respond("Tagging dayandırıldı.")
    await event.delete()
                                  
CmdHelp('tag').add_command(
    'tagall', None, 'Hərkəsi bir mesajda tağ edər.'
).add_command(
    'tag', None, 'Hərkəsi bir-bir tağ edər.'
).add_command(
    'tagadmin', None, 'Bu əmri hər hansısa sohbətdə işlədəndə adminləri tağ edər.'
).add_command(
    'stoptag', None, 'Tag əməliyyatını dayandırır.'
).add_info(
    'Etiketləmə plugini'
).add_sahib(
    '[SİLGİ](t.me/hvseyn) tərəfindən hazırlanmışdır.'
).add()
    
