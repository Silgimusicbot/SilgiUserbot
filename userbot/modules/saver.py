# ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ Əkmə OĞLUMMM
import re
import requests
from userbot.events import register
from userbot.cmdhelp import CmdHelp
def snaptik_yukle(link):
    url = "https://snaptik.io/abc2"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    data = {"url": link}
    cavab = requests.post(url, data=data, headers=headers)
    video_linkləri = re.findall(r'https://[^"]+\.mp4', cavab.text)
    return video_linkləri
def indown_yukle(link):
    try:
        url = "https://indown.io/download/"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "url": link
        }
        cavab = requests.post(url, headers=headers, data=data, timeout=10)
        video_linkləri = re.findall(r'https:\/\/[^"]+\.mp4', cavab.text)
        return video_linkləri
    except:
        return []

@register(outgoing=True, pattern=r"^.vtt(?: |$)(.*)")
async def snaptik_komut(event):
    link = event.pattern_match.group(1).strip()
    if not link:
        await event.edit("Zəhmət olmasa TikTok linkini daxil edin.\nMisal: `.vtt https://www.tiktok.com/...`")
        return

    await event.edit("SnapTik ilə video yüklənir...")

    try:
        video_linkləri = snaptik_yukle(link)
        if not video_linkləri:
            await event.edit("Video tapılmadı və ya link səhvdir.")
            return

        for video_url in video_linkləri:
            video_bytes = requests.get(video_url).content
            await event.client.send_file(event.chat_id, video_bytes, caption="TikTok videosu (SnapTik)")
        await event.delete()

    except Exception as e:
        await event.edit(f"Xəta baş verdi:\n`{str(e)}`")

@register(outgoing=True, pattern=r"^.mig(?: |$)(.*)")
async def instagram_indown_komut(event):
    link = event.pattern_match.group(1).strip()
    if not link:
        await event.edit("Instagram post linkini daxil edin.\nMisal: `.mig https://www.instagram.com/p/...`")
        return

    await event.edit("Instagram postu yüklənir...")

    media_linkləri = indown_yukle(link)
    if not media_linkləri:
        await event.edit("Mediya tapılmadı və ya link səhvdir.")
        return

    try:
        for media in media_linkləri:
            fayl = requests.get(media).content
            await event.client.send_file(event.chat_id, file=fayl, force_document=False, file_name="instagram.mp4")
        await event.delete()
    except Exception as e:
        await event.edit(f"Mediya göndərilə bilmədi:\n`{str(e)}`")
@register(outgoing=True, pattern=r"^.vig(?: |$)(.*)")
async def instagram_reels_komut(event):
    link = event.pattern_match.group(1).strip()
    if not link:
        await event.edit("Instagram Reels linkini daxil edin.\nMisal: `.vig https://www.instagram.com/reel/...`")
        return

    await event.edit("Reels videosu yüklənir...")

    media_linkləri = indown_yukle(link)
    if not media_linkləri:
        await event.edit("Video tapılmadı və ya link səhvdir.")
        return

    try:
        for media in media_linkləri:
            fayl = requests.get(media).content
            await event.client.send_file(event.chat_id, file=fayl, force_document=False, file_name="reel.mp4")
        await event.delete()
    except Exception as e:
        await event.edit(f"Videonu göndərmək alınmadı:\n`{str(e)}`")
CmdHelp("media").add_command("vtt <link>", None, "TikTok videosunu su nişanı olmadan yükləyər.").add_command(
    "mig <link>", None, "Instagram postundakı şəkil və videonu yükləyər.").add_command("vig <link>", None, "Instagram Reels videosunu yükləyər və göndərər.").add_info("⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ Məhsuludur").add()