# SilgiUserbot məhsuludur əkmə peysərin balası
from telethon import events
from userbot import bot
import g4f
import random
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern=r"^\.gpt (.+)")
async def gpt_plugin(event):
    mesaj = event.pattern_match.group(1)
    await event.edit("⏳ Cavab axtarılır...")

    try:
        cavab = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            provider=g4f.Provider.Bing,
            messages=[{"role": "user", "content": mesaj}],
        )
        await event.edit(f"**GPT Cavabı:**\n{cavab}")
    except Exception as e:
        await event.edit(f"Xəta baş verdi:\n`{str(e)}`")