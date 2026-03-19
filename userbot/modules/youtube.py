# SilgiUserbot məhsuludur əkən vəya başqa şey edən bir başa peysərdir.
import os
import yt_dlp
import aiohttp
import re
import asyncio
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp
from userbot import shirniyat  # dəyişmədik

COOKIES_URL = shirniyat

def zererli(ad):
    return re.sub(r'[\\/*?:"<>|]', "", ad)

# ---------------- COOKIES ----------------
async def get_cookies_file():
    if not COOKIES_URL:
        return None, None
    cookies_path = "cookies.txt"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COOKIES_URL) as resp:
                if resp.status != 200:
                    return None, f"❌ cookies yüklənmədi: {resp.status}"
                text = await resp.text()
                with open(cookies_path, "w", encoding="utf-8") as f:
                    f.write(text)
        return cookies_path, None
    except Exception as e:
        return None, f"⚠️ cookies xətası:\n{e}"

# ---------------- YTMP3 ----------------
@silgi(outgoing=True, pattern=r"\.ytmp3(?: |$)(.*)")
async def ytaudio(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("ℹ️ `.ytmp3 mahnı adı və ya link`")
        return

    await event.edit("🔄 Hazırlanır...")

    cookies_path, error = await get_cookies_file()
    if error:
        await event.edit(error)
        return

    search_term = query if query.startswith("http") else f"ytsearch5:{query}"
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "cookiefile": cookies_path if cookies_path else None,
        "outtmpl": os.path.join(output_dir, "%(title).50s.%(ext)s"),
        "quiet": True,
        "ignoreerrors": True,
        "nocheckcertificate": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    mp3_path = None

    try:
        await event.edit("🎧 Axtarılır...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search_term, download=True)

            if not info:
                await event.edit("❌ Nəticə tapılmadı.")
                return

            if "entries" in info:
                info = info["entries"][0] if info["entries"] else None

            if not info:
                await event.edit("❌ Mahnı tapılmadı.")
                return

            title = zererli(info.get("title", "Mahnı"))

            # mp3 tap
            for f in os.listdir(output_dir):
                if f.endswith(".mp3"):
                    mp3_path = os.path.join(output_dir, f)
                    break

            if not mp3_path:
                await event.edit("❌ MP3 tapılmadı.")
                return

        await event.edit(f"🎵 `{title}` göndərilir...")
        await event.client.send_file(
            event.chat_id,
            mp3_path,
            caption=f"🎶 `{title}`\n```⚝ SILGI USERBOT ⚝```",
            link_preview=False
        )
        await event.delete()

    except Exception as e:
        await event.edit(f"❌ Xəta:\n`{e}`")

    finally:
        if cookies_path and os.path.exists(cookies_path):
            os.remove(cookies_path)
        if mp3_path and os.path.exists(mp3_path):
            os.remove(mp3_path)

# ---------------- YTVIDEO ----------------
@silgi(outgoing=True, pattern=r"\.ytvideo(?: |$)(.*)")
async def ytvideo(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("ℹ️ `.ytvideo video adı və ya link`")
        return

    await event.edit("🔄 Hazırlanır...")

    cookies_path, error = await get_cookies_file()
    if error:
        await event.edit(error)
        return

    search_term = query if query.startswith("http") else f"ytsearch5:{query}"
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "cookiefile": cookies_path if cookies_path else None,
        "merge_output_format": "mp4",
        "ignoreerrors": True,
        "nocheckcertificate": True,
    }

    file_path = None

    try:
        await event.edit("🎬 Yüklənir...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search_term, download=True)

            if not info:
                await event.edit("❌ Video tapılmadı.")
                return

            if "entries" in info:
                info = info["entries"][0] if info["entries"] else None

            if not info:
                await event.edit("❌ Video tapılmadı.")
                return

            title = zererli(info.get("title", "Video"))

            file_path = ydl.prepare_filename(info)

            if not os.path.exists(file_path):
                # fallback
                for f in os.listdir(output_dir):
                    if f.endswith(".mp4"):
                        file_path = os.path.join(output_dir, f)
                        break

            if not file_path:
                await event.edit("❌ Video faylı tapılmadı.")
                return

        await event.edit(f"📼 `{title}` göndərilir...")
        await event.client.send_file(
            event.chat_id,
            file_path,
            caption=f"🎥 `{title}`\n```⚝ SILGI USERBOT ⚝```",
            supports_streaming=True,
            link_preview=False
        )
        await event.delete()

    except Exception as e:
        await event.edit(f"❌ Xəta:\n`{e}`")

    finally:
        if cookies_path and os.path.exists(cookies_path):
            os.remove(cookies_path)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

# ---------------- HELP ----------------
CmdHelp("youtube").add_command(
    "ytmp3", "mahnı adı vəya link", "Youtube dən mahnı yükləyir."
).add_command(
    "ytvideo", "video adı vəya link", "Youtube dən video yükləyir."
).add_sahib(
    "[SILGI](https://t.me/silgiteam)"
).add()
