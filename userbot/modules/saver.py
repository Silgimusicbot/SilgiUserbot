# ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ Əkmə OĞLUMMM
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from telethon import events
import asyncio
import random

mesaj = "Video yükləndi.\n⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝"
YUKLEYICI_BOT = "HK_tiktok_bot"

async def gosterici(event, uzunluq=6):
    mesaj_obj = await event.edit("Yükləmə başlayır...")
    addimlar = 10
    for i in range(1, addimlar + 1):
        faiz = i * 10
        bar = "▓" * i + "░" * (addimlar - i)
        suret = round(random.uniform(0.8, 4.5), 2)
        metn = f"[{bar}] {faiz}% - {suret} MB/s"
        await mesaj_obj.edit(f"Yüklənir...\n{metn}")
        await asyncio.sleep(uzunluq / addimlar)
    await mesaj_obj.edit("Yükləmə tamamlandı. Video hazırlanır...")

async def gonder(event, link):
    try:
        bot = await event.client.get_entity(YUKLEYICI_BOT)
        cavab = None

        @event.client.on(events.NewMessage(from_users=bot.id))
        async def cavabi_al(mesaj):
            nonlocal cavab
            if mesaj.media:
                cavab = mesaj

        await event.edit("Yükləyici bota /start göndərilir...")
        await event.client.send_message(bot, "/start")
        await asyncio.sleep(1)
        await event.edit("Link bota göndərilir...")
        await event.client.send_message(bot, link)
        await gosterici(event, uzunluq=6)

        for _ in range(20):
            if cavab:
                break
            await asyncio.sleep(1)

        if cavab:
            await event.client.send_file(
                event.chat_id,
                cavab.media,
                caption=mesaj,
                reply_to=event.reply_to_msg_id
            )
            await event.delete()
        else:
            await event.edit("Botdan cavab gəlmədi. Linki və botun aktivliyini yoxla.")
    except Exception as e:
        await event.edit(f"Xəta baş verdi: `{str(e)}`")

@register(outgoing=True, pattern=r"^.vtt(?: |$)(.*)")
async def tiktok(event):
    link = event.pattern_match.group(1)
    if not link:
        await event.edit("Zəhmət olmasa TikTok linkini yazın: `.vtt <link>`")
        return
    await gonder(event, link)

@register(outgoing=True, pattern=r"^.vig(?: |$)(.*)")
async def instagram(event):
    link = event.pattern_match.group(1)
    if not link:
        await event.edit("Zəhmət olmasa Instagram linkini yazın: `.vig <link>`")
        return
    await gonder(event, link)

CmdHelp("videosaver").add_command(
    "vtt", "<link>", "TikTok videosunu yükləyir."
).add_command(
    "vig", "<link>", "Instagram videosunu yükləyir."
).add()