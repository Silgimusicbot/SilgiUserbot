import requests
from userbot.events import register
from userbot.cmdhelp import CmdHelp
SERPER_API_KEY = "bb3ddc47d064d10495d0a158f3748c68c8ffef69"

@register(outgoing=True, pattern=r"^.google(?: |$)(.*)")
async def google_serper(event):
    axtarish = event.pattern_match.group(1).strip()
    if not axtarish:
        await event.edit("Zəhmət olmasa axtarmaq istədiyin sözü yaz.\nMisal: `.google Telegram userbot`")
        return

    await event.edit("Axtarış edilir...")

    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "q": axtarish
        }
        cavab = requests.post(url, headers=headers, json=data).json()

        nəticələr = cavab.get("organic", [])
        if not nəticələr:
            await event.edit("Heç bir nəticə tapılmadı.")
            return

        mesaj = "**Google Axtarış Nəticələri:**\n\n"
        for nəticə in nəticələr[:5]:
            başlıq = nəticə.get("title")
            link = nəticə.get("link")
            mesaj += f"[{başlıq}]({link})\n\n"

        await event.edit(mesaj, link_preview=False)

    except Exception as e:
        await event.edit(f"Xəta baş verdi:\n`{str(e)}`")
CmdHelp("google").add_command("google <söz>", None, "Google-da axtarış edər və nəticələri göstərər.").add()