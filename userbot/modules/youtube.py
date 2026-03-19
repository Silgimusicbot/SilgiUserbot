# SilgiUserbot məhsuludur əkən vəya başqa şey edən bir başa peysərdir.
import os
import yt_dlp
import aiohttp
import re
import asyncio
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp
from userbot import şirniyat

COOKIES_URL = şirniyat

def zererli(ad):
    return re.sub(r'[\\/*?:"<>|]', "", ad)

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

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "cookiefile": cookies_path,
        "outtmpl": os.path.join(output_dir, "%(title).50s.%(ext)s"),
        "writethumbnail": True,    
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},  
        ],
        "postprocessor_args": ["-id3v2_version", "3"],
        "quiet": True,
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

            downloaded_path = ydl.prepare_filename(info)
            mp3_path = os.path.splitext(downloaded_path)[0] + ".mp3"

            if not os.path.exists(mp3_path):
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
        if os.path.exists(cookies_path):
            os.remove(cookies_path)
        if mp3_path and os.path.exists(mp3_path):
            os.remove(mp3_path)



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

    ydl_opts = {
        'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': outtmpl,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': cookies_path,
        'merge_output_format': 'mp4',
    }

    try:
        await event.edit("🎬 `Video yüklənir...`")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=True)
            if 'entries' in info:
                info = info['entries'][0]
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
