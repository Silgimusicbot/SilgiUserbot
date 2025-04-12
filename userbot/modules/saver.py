# ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ Əkmə OĞLUMMM
from userbot.events import register
from userbot.cmdhelp import CmdHelp
import asyncio
import random
mesaj = "Video yükləndi.\n⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝"
YUKLEYICI_BOT = "HK_tiktok_bot"
async def gosterici(event, uzunluq=5):
    mesaj = await event.edit("Yükləmə başlayır...")
    addimlar = 10
    for i in range(1, addimlar + 1):
        faiz = i * 10
        bar = "▓" * i + "░" * (addimlar - i)
        suret = round(random.uniform(0.8, 4.5), 2)
        metn = f"[{bar}] {faiz}% - {suret} MB/s"
        await mesaj.edit(f"Yüklənir...\n{metn}")
        await asyncio.sleep(uzunluq / addimlar)
    await mesaj.edit("Yükləmə tamamlandı. Video hazırlanır...")
async def gonder(event, link):
    try:
        bot = await event.client.get_entity(YUKLEYICI_BOT)
        await gosterici(event, uzunluq=6)
        await event.edit("Linki yükləyici bota göndərirəm...")
        await event.client.send_message(bot, link)
        cavab = await event.client.wait_for_event(
            lambda e: (
                e.chat_id == bot.id and e.sender_id == bot.id and
                (e.video or e.document or e.photo)
            ),
            timeout=30
        )
        await event.client.send_file(
            event.chat_id,
            cavab.media,
            caption=mesaj,
            reply_to=event.reply_to_msg_id
        )
        await event.delete()

    except asyncio.TimeoutError:
        await event.edit("Bot cavab vermədi. Zəhmət olmasa linki yoxla.")
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