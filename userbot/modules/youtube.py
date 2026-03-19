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
    cookies_path = "cookies.txt"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COOKIES_URL) as resp:
                if resp.status != 200: return None
                text = await resp.text()
                with open(cookies_path, "w", encoding="utf-8") as f:
                    f.write(text)
        return cookies_path
    except:
        return None

@silgi(outgoing=True, pattern=r"\.ytmp3(?: |$)(.*)")
async def ytaudio(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("ℹ️ Mahnı adı və ya link yazın.")
        return

    await event.edit("🔄 `Mahnı axtarılır...`")
    cookies = await get_cookies_file()
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "cookiefile": cookies,
        "outtmpl": os.path.join(output_dir, "%(title).50s.%(ext)s"),
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "extractor_args": {
            "youtube": {
                "player_client": ["web", "mweb", "web_creator"],
                "player_skip": ["configs", "webpage"]
            }
        },
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }, {"key": "FFmpegMetadata"}],
        "quiet": True,
        "nocheckcertificate": True,
        "ignoreerrors": True
    }

    try:
        search = query if query.startswith("http") else f"ytsearch1:{query}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search, download=True)
            if info is None:
                await event.edit("❌ Video tapılmadı və ya YouTube blokladı.")
                return
            if "entries" in info: info = info["entries"][0]
            
            title = zererli(info.get("title", "Audio"))
            file_path = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"

        await event.edit(f"📤 `{title}` göndərilir...")
        await event.client.send_file(event.chat_id, file_path, caption=f"🎶 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```")
        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta: `{str(e)}`")
    finally:
        if cookies and os.path.exists(cookies): os.remove(cookies)
        if 'file_path' in locals() and os.path.exists(file_path): os.remove(file_path)

@silgi(outgoing=True, pattern=r"\.ytvideo(?: |$)(.*)")
async def ytvideo(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("ℹ️ Video adı və ya link yazın.")
        return

    await event.edit("🔄 `Video hazırlanır...`")
    cookies = await get_cookies_file()
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "noplaylist": True,
        "cookiefile": cookies,
        "outtmpl": os.path.join(output_dir, "%(title).50s.%(ext)s"),
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "extractor_args": {
            "youtube": {
                "player_client": ["web", "mweb", "web_creator"],
                "player_skip": ["configs", "webpage"]
            }
        },
        "merge_output_format": "mp4",
        "quiet": True,
        "nocheckcertificate": True,
        "ignoreerrors": True
    }

    try:
        search = query if query.startswith("http") else f"ytsearch1:{query}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search, download=True)
            if info is None:
                await event.edit("❌ Video tapılmadı və ya YouTube blokladı.")
                return
            if "entries" in info: info = info["entries"][0]
            
            title = zererli(info.get("title", "Video"))
            file_path = ydl.prepare_filename(info)

        await event.edit(f"📤 `{title}` göndərilir...")
        await event.client.send_file(event.chat_id, file_path, caption=f"🎥 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```", supports_streaming=True)
        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta: `{str(e)}`")
    finally:
        if cookies and os.path.exists(cookies): os.remove(cookies)
        if 'file_path' in locals() and os.path.exists(file_path): os.remove(file_path)

CmdHelp("youtube").add_command("ytmp3", "ad/link", "Mahnı yükləyir.").add_command("ytvideo", "ad/link", "Video yükləyir.").add_sahib("[SILGI](https://t.me/silgiteam)").add()
