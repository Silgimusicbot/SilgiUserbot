# SilgiUserbot məhsuludur əkən vəya başqa şey edən bir başa peysərdir.
import os
import yt_dlp
import aiohttp
import re
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp

COOKIES_URL = "https://batbin.me/raw/layers"

def zererli(ad):
    return re.sub(r'[\\/*!?:"<>|]', "", ad)

async def get_cookies_file():
    cookies_path = "cookies.txt"
    async with aiohttp.ClientSession() as session:
        async with session.get(COOKIES_URL) as resp:
            if resp.status != 200:
                return None, f"❌ `cookies.txt` yüklənə bilmədi. Status: {resp.status}"
            text = await resp.text()
            with open(cookies_path, "w", encoding="utf-8") as f:
                f.write(text)
    return cookies_path, None

@silgi(outgoing=True, pattern=r"\.ytmp3(?: |$)(.*)")
async def ytaudio(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("ℹ️ Zəhmət olmasa link və ya mahnı adı yaz:\n`.ytmp3 Mahnı adı` və ya `.ytmp3 https://youtu.be/...`")
        return

    await event.edit("🔄 `Gözləyin, yükləmə hazırlanır...`")

    cookies_path, error = await get_cookies_file()
    if error:
        await event.edit(error)
        return

    search_term = query if query.startswith("http") else f"ytsearch1:{query}"
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': outtmpl,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': cookies_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        await event.edit("🎧 `Mahnı axtarılır...`")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            raw_title = info.get("title", "Mahnı")
            title = zererli(raw_title)
            file_path = os.path.join(output_dir, f"{title}.mp3")

        await event.edit(f"🎵 `{title}` adlı mahnı yüklənir")
        await event.client.send_file(
            event.chat_id,
            file_path,
            caption=f"🎶 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```",
            link_preview=False
        )
        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Yükləmə xətası:\n`{str(e)}`")
    finally:
        if os.path.exists(cookies_path):
            os.remove(cookies_path)
        if os.path.exists(file_path):
            os.remove(file_path)

@silgi(outgoing=True, pattern=r"\.ytvideo(?: |$)(.*)")
async def ytvideo(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("ℹ️ Zəhmət olmasa link və ya video adı yaz:\n`.ytvideo Video adı` və ya `.ytvideo https://youtu.be/...`")
        return

    await event.edit("🔄 `Gözləyin, yükləmə hazırlanır...`")

    cookies_path = "cookies.txt"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COOKIES_URL) as resp:
                if resp.status != 200:
                    await event.edit("❌ `cookies.txt` yüklənə bilmədi.")
                    return
                text = await resp.text()
                with open(cookies_path, "w", encoding="utf-8") as f:
                    f.write(text)
    except Exception as e:
        await event.edit(f"⚠️ cookies yükləmə xətası:\n`{e}`")
        return

    search_term = query if query.startswith("http") else f"ytsearch1:{query}"
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

    try:
        await event.edit("🎬 `Video axtarılır...`")

        ydl_opts_info = {
            'quiet': True,
            'cookiefile': cookies_path,
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(search_term, download=False)
            if 'entries' in info:
                info = info['entries'][0]

            formats = info.get('formats', [])
            progressive = None
            for f in formats:
                if f.get("vcodec", "none") != "none" and f.get("acodec", "none") != "none" and f["ext"] == "mp4":
                    progressive = f["format_id"]
                    break

            if not progressive:
                await event.edit("❌ `MP4 format tapılmadı.`")
                return

        ydl_opts = {
            'format': progressive,
            'outtmpl': outtmpl,
            'noplaylist': True,
            'quiet': True,
            'cookiefile': cookies_path,
        }

   
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=True)
            raw_title = info.get("title", "Video")
            title = zererli(raw_title)
            ext = info.get("ext", "mp4")
            file_path = os.path.join(output_dir, f"{title}.{ext}")

        await event.edit(f"📼 `{title}` adlı video yüklənir...")
        await event.client.send_file(
            event.chat_id,
            file_path,
            caption=f"🎥 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```",
            supports_streaming=True,
            link_preview=False
        )
        await event.delete()
        os.remove(file_path)
        os.remove(cookies_path)

    except Exception as e:
        await event.edit(f"❌ Yükləmə xətası:\n`{str(e)}`")
CmdHelp("youtube").add_command(
    "ytmp3", "mahnı adı vəya link", "Youtube dən mahnı yükləyir."
).add_command(
    "ytvideo", "video adı vəya link", "Youtube dən video yükləyir."
).add_sahib(
    "[SILGI](https://t.me/silgiteam)"
).add()