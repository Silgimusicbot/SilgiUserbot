import requests
from bs4 import BeautifulSoup
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern=r"^.google(?: |$)(.*)")
async def google_axtar(event):
    axtaris = event.pattern_match.group(1).strip()
    if not axtaris:
        await event.edit("Zəhmət olmasa axtarmaq istədiyin sözü yaz.\nMisal: `.google Telegram Userbot`")
        return

    await event.edit("Google-da axtarılır...")

    try:
        link = f"https://www.google.com/search?q={axtaris.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")
        
        cavablar = []
        for result in soup.find_all('div', class_='tF2Cxc')[:5]:  
            basliq = result.find('h3')
            url = result.find('a')['href']
            if basliq and url:
                cavablar.append(f"[{basliq.text}]({url})")
        
        if cavablar:
            await event.edit("**Google Axtarış Nəticələri:**\n\n" + "\n\n".join(cavablar), link_preview=False)
        else:
            await event.edit("Heç bir nəticə tapılmadı.")
    
    except Exception as e:
        await event.edit(f"Axtarış zamanı xəta baş verdi:\n`{str(e)}`")


CmdHelp("google").add_command("google <axtarış>", None, "Google-da axtarış edib nəticələri göstərər.").add()