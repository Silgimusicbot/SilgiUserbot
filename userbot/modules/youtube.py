# SilgiUserbot məhsuludur əkən vəya başqa şey edən bir başa peysərdir.
import os
import yt_dlp
import aiohttp

from userbot.events import register
from useebot.cmdhelp import CmdHelp

COOKIES_URL = "https://batbin.me/raw/layers"

@register(outgoing=True, pattern=r"\.ytmp3(?: |$)(.*)")
async def ytaudio(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("ℹ️ Zəhmət olmasa link və ya mahnı adı yaz:\n`.ytmp3 Mahnı adı` və ya `.ytmp3 https://youtu.be/...`")
        return

    await event.edit("🔄 Gözləyin, yükləmə hazırlanır...")

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
        'format': 'bestaudio/best',
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
        await event.edit("🎧 Mahnı endirilir...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            title = info.get("title", "Mahnı")
            file_path = os.path.join(output_dir, f"{title}.mp3")

        await event.edit("📤 Göndərilir...")
        await event.client.send_file(
            event.chat_id,
            file_path,
            caption=f"🎶 `{title}`",
            link_preview=False
        )
        await event.delete()

        os.remove(file_path)
        os.remove(cookies_path)

    except Exception as e:
        await event.edit(f"❌ Yükləmə xətası:\n`{str(e)}`")


@register(outgoing=True, pattern=r"\.ytvideo(?: |$)(.*)")
async def ytvideo(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("ℹ️ Zəhmət olmasa link və ya video adı yaz:\n`.ytvideo Video adı` və ya `.ytvideo https://youtu.be/...`")
        return

    await event.edit("🔄 Gözləyin, yükləmə hazırlanır...")

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
        'format': 'best',
        'outtmpl': outtmpl,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': cookies_path,
    }

    try:
        await event.edit("🎬 Video endirilir...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            title = info.get("title", "Video")
            ext = info.get("ext", "mp4")
            file_path = os.path.join(output_dir, f"{title}.{ext}")

        await event.edit("📤 Göndərilir...")
        await event.client.send_file(
            event.chat_id,
            file_path,
            caption=f"🎥 `{title}`",
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