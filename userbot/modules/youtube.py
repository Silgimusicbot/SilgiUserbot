import os
import yt_dlp
import aiohttp
import re
import asyncio
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp
from userbot import shirniyat

COOKIES_URL = "https://batbin.me/raw/unwheel"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

def zererli(ad: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", ad or "")

async def get_cookies_file():
    cookies_path = "cookies.txt"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COOKIES_URL) as resp:
                if resp.status != 200:
                    return None
                text = await resp.text()
                if not text or len(text.strip()) < 10:
                    return None
                with open(cookies_path, "w", encoding="utf-8") as f:
                    f.write(text)
        return cookies_path
    except Exception:
        return None

def build_common_ydl_opts(output_dir: str, cookies_path: str | None):
    opts = {
        "noplaylist": True,
        "outtmpl": os.path.join(output_dir, "%(title).50s.%(ext)s"),
        "restrictfilenames": True,
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,

        # Stabillik
        "socket_timeout": 30,
        "retries": 5,
        "fragment_retries": 5,

        # EJS / node runtime
        "js_runtimes": {"node": {}},
        "remote_components": "ejs:github",

        # Header-lar
        "http_headers": {
            "User-Agent": UA,
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.youtube.com/",
        },

        # YouTube extractor parametrləri
        "extractor_args": {
            "youtube": {
                "player_client": ["web", "tv"],
                "player_skip": ["configs", "webpage"],
            }
        },
    }

    # Cookies yalnız real fayl varsa əlavə edirik
    if cookies_path and os.path.exists(cookies_path):
        opts["cookiefile"] = cookies_path

    return opts

@silgi(outgoing=True, pattern=r"\\.ytmp3(?: |$)(.*)")
async def ytaudio(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.edit("ℹ️ Mahnı adı daxil edin.")

    await event.edit("🔄 `Audio hazırlanır...`")
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    cookies = await get_cookies_file()
    ydl_opts = build_common_ydl_opts(output_dir, cookies)

    # Daha sağlam format fallback
    ydl_opts.update({
        "format": "ba/bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {"key": "FFmpegMetadata"},
        ],
    })

    file_path = None
    try:
        search = query if query.startswith("http") else f"ytsearch1:{query}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search, download=True)
            if not info:
                return await event.edit("❌ YouTube-dan cavab alınmadı.")
            data = info["entries"][0] if "entries" in info else info

            # mp3 çıxışı
            file_path = ydl.prepare_filename(data).rsplit(".", 1)[0] + ".mp3"
            title = zererli(data.get("title", "Audio"))

        await event.edit(f"📤 `{title}` göndərilir...")
        await event.client.send_file(
            event.chat_id,
            file_path,
            caption=f"🎶 `{title}`\\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```",
        )
        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta: `{str(e)}`")
    finally:
        if cookies and os.path.exists(cookies):
            os.remove(cookies)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

@silgi(outgoing=True, pattern=r"\\.ytvideo(?: |$)(.*)")
async def ytvideo(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.edit("ℹ️ Video adı daxil edin.")

    await event.edit("🔄 `Video hazırlanır...`")
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    cookies = await get_cookies_file()
    ydl_opts = build_common_ydl_opts(output_dir, cookies)

    # Video üçün universal format (ext məhdudiyyəti yoxdur)
    ydl_opts.update({
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
    })

    file_path = None
    try:
        search = query if query.startswith("http") else f"ytsearch1:{query}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search, download=True)
            if not info:
                return await event.edit("❌ YouTube-dan cavab alınmadı.")
            data = info["entries"][0] if "entries" in info else info
            file_path = ydl.prepare_filename(data)
            title = zererli(data.get("title", "Video"))

        await event.edit(f"📤 `{title}` göndərilir...")
        await event.client.send_file(
            event.chat_id,
            file_path,
            caption=f"🎥 `{title}`\\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```",
            supports_streaming=True,
        )
        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta: `{str(e)}`")
    finally:
        if cookies and os.path.exists(cookies):
            os.remove(cookies)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

CmdHelp("youtube")\
    .add_command("ytmp3", "ad/link", "Mahnı yükləyir.")\
    .add_command("ytvideo", "ad/link", "Video yükləyir.")\
    .add_sahib("[SILGI](https://t.me/silgiteam)")\
    .add()
