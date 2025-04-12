import re
import requests
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# TikTok 
def tiktok_yukle(link):
    api = "https://tikwm.com/api/"
    parametrlər = {"url": link}
    cavab = requests.get(api, params=parametrlər).json()
    if cavab.get("data"):
        return cavab["data"]["play"], cavab["data"]["title"]
    else:
        return None, None

@register(outgoing=True, pattern=r"^.vtt(?: |$)(.*)")
async def tiktok_komut(event):
    link = event.pattern_match.group(1).strip()
    if not link:
        await event.edit("Zəhmət olmasa TikTok linkini daxil edin.\nMisal: `.tt https://www.tiktok.com/...`")
        return

    await event.edit("TikTok videosu yüklənir...")

    video_linki, basliq = tiktok_yukle(link)
    if not video_linki:
        await event.edit("Videonu yükləmək mümkün olmadı. Linki düzgün daxil etdiyinizə əmin olun.")
        return

    try:
        video = requests.get(video_linki).content
        await event.client.send_file(event.chat_id, video, caption=basliq or "TikTok videosu")
        await event.delete()
    except Exception as e:
        await event.edit(f"Videonu göndərmək mümkün olmadı:\n`{str(e)}`")


# Instagram 
def instagram_yukle(link):
    api = "https://igram.io/i/"
    basliq = {
        "User-Agent": "Mozilla/5.0"
    }
    cavab = requests.post(api, data={"url": link}, headers=basliq)
    media_linkləri = re.findall(r'https://[^"]+\.mp4|https://[^"]+\.jpg', cavab.text)
    return media_linkləri

@register(outgoing=True, pattern=r"^.mig(?: |$)(.*)")
async def instagram_komut(event):
    link = event.pattern_match.group(1).strip()
    if not link:
        await event.edit("Zəhmət olmasa Instagram post linkini daxil edin.\nMisal: `.ig https://www.instagram.com/p/...`")
        return

    await event.edit("Instagram mediası yüklənir...")

    media_linkləri = instagram_yukle(link)
    if not media_linkləri:
        await event.edit("Mediya tapılmadı və ya link düzgün deyil.")
        return

    try:
        for media in media_linkləri:
            fayl = requests.get(media).content
            await event.client.send_file(event.chat_id, fayl)
        await event.delete()
    except Exception as e:
        await event.edit(f"Mediya göndərilə bilmədi:\n`{str(e)}`")
def reel_yukle(link):
    api = "https://igram.io/i/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    cavab = requests.post(api, data={"url": link}, headers=headers)
    reels = re.findall(r'https://[^"]+\.mp4', cavab.text)
    return reels

@register(outgoing=True, pattern=r"^.vig(?: |$)(.*)")
async def reel_komutu(event):
    link = event.pattern_match.group(1).strip()
    if not link:
        await event.edit("Zəhmət olmasa Instagram Reels linkini daxil edin.\nMisal: `.reel https://www.instagram.com/reel/...`")
        return

    await event.edit("Reels videosu yüklənir...")

    video_linkləri = reel_yukle(link)
    if not video_linkləri:
        await event.edit("Reels videosu tapılmadı və ya link düzgün deyil.")
        return

    try:
        for video in video_linkləri:
            fayl = requests.get(video).content
            await event.client.send_file(event.chat_id, fayl)
        await event.delete()
    except Exception as e:
        await event.edit(f"Videonu göndərmək mümkün olmadı:\n`{str(e)}`")
CmdHelp("media").add_command("vtt <link>", None, "TikTok videosunu su nişanı olmadan yükləyər.").add_command(
    "mig <link>", None, "Instagram postundakı şəkil və videonu yükləyər.").add_command("reel <link>", None, "Instagram Reels videosunu yükləyər və göndərər.").add()