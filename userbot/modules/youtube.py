import os
import asyncio
import tempfile
from mutagen.id3 import ID3, APIC, TIT2
from mutagen.mp3 import MP3
from yt_dlp import YoutubeDL
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp


@silgi(outgoing=True, pattern=r"\.ytmp3(?: |$)(.*)")
async def ytmp3_handler(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("❌ Ad və ya link daxil edin.")
        return
    await event.edit("⏳ MP3 yüklənir...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                "format": "bestaudio[ext=m4a]/bestaudio/best",
                "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }
                ],
                "writethumbnail": True,
                "default_search": "ytsearch",
                "noplaylist": True,
                "quiet": True,
                "extractor_args": {"youtube": {"player_client": ["mweb"]}},
            }
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, lambda: _ydl_extract(ydl_opts, query))
            title = info.get("title", "Unknown")

            mp3_file = None
            thumb_file = None
            for f in os.listdir(tmpdir):
                full = os.path.join(tmpdir, f)
                if f.endswith(".mp3"):
                    mp3_file = full
                elif f.endswith((".jpg", ".jpeg", ".png", ".webp")):
                    thumb_file = full

            if mp3_file and thumb_file:
                audio = MP3(mp3_file, ID3=ID3)
                try:
                    audio.add_tags()
                except Exception:
                    pass
                with open(thumb_file, "rb") as img_data:
                    audio.tags.add(
                        APIC(
                            encoding=3,
                            mime="image/jpeg",
                            type=3,
                            desc="Cover",
                            data=img_data.read(),
                        )
                    )
                audio.tags.add(TIT2(encoding=3, text=title))
                audio.save()

            caption = f"🎶 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```"

            await event.client.send_file(
                event.chat_id,
                mp3_file,
                caption=caption,
                thumb=thumb_file,
            )
            await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta: `{e}`")


@silgi(outgoing=True, pattern=r"\.ytvideo(?: |$)(.*)")
async def ytvideo_handler(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        await event.edit("❌ Ad və ya link daxil edin.")
        return
    await event.edit("⏳ Video yüklənir...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                "format": "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
                "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
                "merge_output_format": "mp4",
                "default_search": "ytsearch",
                "noplaylist": True,
                "quiet": True,
                "extractor_args": {"youtube": {"player_client": ["mweb"]}},
            }
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, lambda: _ydl_extract(ydl_opts, query))
            title = info.get("title", "Unknown")

            video_file = None
            for f in os.listdir(tmpdir):
                if f.endswith((".mp4", ".mkv", ".webm")):
                    video_file = os.path.join(tmpdir, f)
                    break

            caption = f"🎬 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```"

            await event.client.send_file(
                event.chat_id,
                video_file,
                caption=caption,
                supports_streaming=True,
            )
            await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta: `{e}`")


def _ydl_extract(opts, query):
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=True)
        if "entries" in info:
            return info["entries"][0]
        return info


CmdHelp("youtube").add_command("ytmp3", "ad/link", "Mahnı yükləyir.").add_command("ytvideo", "ad/link", "Video yükləyir.").add_sahib("[SILGI](https://t.me/silgiteam)").add()
