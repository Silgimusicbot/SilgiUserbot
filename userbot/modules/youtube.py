# SilgiUserbot məhsuludur əkən vəya başqa şey edən bir başa peysərdir.
import os
import yt_dlp
import aiohttp
import re
import asyncio
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp
from userbot import shirniyat 

COOKIES_URL = shirniyat

def zererli(ad):
    return re.sub(r'[\\/*?:"<>|]', "", ad)

async def get_cookies_file():
    if not COOKIES_URL:
        return None, None
    cookies_path = "cookies.txt"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COOKIES_URL) as resp:
                if resp.status != 200:
                    return None, f"❌ `cookies.txt` yüklənə bilmədi. Status: {resp.status}"
                text = await resp.text()
                with open(cookies_path, "w", encoding="utf-8") as f:
                    f.write(text)
        return cookies_path, None
    except Exception as e:
        return None, f"⚠️ cookies yükləmə xətası:\n`{e}`"

# -------------------- .ytmp3 --------------------
@silgi(outgoing=True, pattern=r"\.ytmp3(?: |$)(.*)")
async def ytaudio(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit(
            "ℹ️ Zəhmət olmasa link və ya mahnı adı yaz:\n`.ytmp3 Mahnı adı` və ya `.ytmp3 https://youtu.be/...`"
        )
        return

    await event.edit("🔄 `Gözləyin, yükləmə hazırlanır...`")
    cookies_path, error = await get_cookies_file()
    if error:
        await event.edit(error)
        return

    search_term = query if query.startswith("http") else f"ytsearch1:{query}"
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "cookiefile": cookies_path if cookies_path else None,
        "outtmpl": os.path.join(output_dir, "%(title).50s.%(ext)s"),
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "nocheckcertificate": True,
        "ignoreerrors": True,
    }

    mp3_path = None
    try:
        await event.edit("🎧 `Mahnı axtarılır...`")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search_term, download=True)
            if "entries" in info:
                info = info["entries"][0]

            raw_title = info.get("title", "Mahnı")
            title = zererli(raw_title)

            # Find downloaded mp3 file
            for file in os.listdir(output_dir):
                if file.endswith(".mp3"):
                    mp3_path = os.path.join(output_dir, file)
                    break

            if not mp3_path or not os.path.exists(mp3_path):
                await event.edit("❌ `MP3 faylı tapılmadı.`")
                return

        await event.edit(f"🎵 `{title}` adlı mahnı göndərilir...")
        await event.client.send_file(
            event.chat_id,
            mp3_path,
            caption=f"🎶 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```",
            link_preview=False
        )
        await event.delete()

    except Exception as e:
        await event.edit(f"❌ Yükləmə xətası:\n`{str(e)}`")

    finally:
        if cookies_path and os.path.exists(cookies_path):
            os.remove(cookies_path)
        if mp3_path and os.path.exists(mp3_path):
            os.remove(mp3_path)

# -------------------- .ytvideo --------------------
@silgi(outgoing=True, pattern=r"\.ytvideo(?: |$)(.*)")
async def ytvideo(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit(
            "ℹ️ Zəhmət olmasa link və ya video adı yaz:\n`.ytvideo Video adı` və ya `.ytvideo https://youtu.be/...`"
        )
        return

    await event.edit("🔄 `Gözləyin, yükləmə hazırlanır...`")
    cookies_path, error = await get_cookies_file()
    if error:
        await event.edit(error)
        return

    search_term = query if query.startswith("http") else f"ytsearch1:{query}"
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, "%(title)s.%(ext)s"),
        'noplaylist': True,
        'quiet': True,
        'cookiefile': cookies_path if cookies_path else None,
        'merge_output_format': 'mp4',
        'nocheckcertificate': True,
        'ignoreerrors': True,
    }

    file_path = None
    try:
        await event.edit("🎬 `Video yüklənir...`")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search_term, download=True)
            if 'entries' in info:
                info = info['entries'][0]

            raw_title = info.get("title", "Video")
            title = zererli(raw_title)
            file_path = ydl.prepare_filename(info)

            if not os.path.exists(file_path):
                # fallback: pick any mp4 in folder
                for file in os.listdir(output_dir):
                    if file.endswith(".mp4"):
                        file_path = os.path.join(output_dir, file)
                        break

            if not file_path or not os.path.exists(file_path):
                await event.edit("❌ `Video faylı tapılmadı.`")
                return

        await event.edit(f"📼 `{title}` adlı video göndərilir...")
        await event.client.send_file(
            event.chat_id,
            file_path,
            caption=f"🎥 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```",
            supports_streaming=True,
            link_preview=False
        )
        await event.delete()

    except Exception as e:
        await event.edit(f"❌ Yükləmə xətası:\n`{str(e)}`")

    finally:
        if cookies_path and os.path.exists(cookies_path):
            os.remove(cookies_path)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

# -------------------- CmdHelp --------------------
CmdHelp("youtube").add_command(
    "ytmp3", "mahnı adı vəya link", "Youtube dən mahnı yükləyir."
).add_command(
    "ytvideo", "video adı vəya link", "Youtube dən video yükləyir."
).add_sahib(
    "[SILGI](https://t.me/silgiteam)"
).add()
