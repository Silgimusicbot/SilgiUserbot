import os, yt_dlp, re, asyncio
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp

def temiz_ad(s):
    try:
        s = s.encode('latin-1').decode('utf-8')
    except:
        pass
    return re.sub(r'[\\/*?:"<>|]', "", s).strip()

@silgi(outgoing=True, pattern=r"\.mp3(?: |$)(.*)")
async def scaudio(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.edit("ℹ️ Mahnı adı daxil edin.")
    await event.edit("🔄 `Mahnı axtarılır...`")
    out_dir = "downloads"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{out_dir}/%(title)s.%(ext)s",
        "writethumbnail": True,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata"}
        ],
        "quiet": True,
        "no_warnings": True
    }
    try:
        search = query if query.startswith("http") else f"scsearch1:{query}"
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search, download=True)
            if not info or 'entries' in info and not info['entries']:
                return await event.edit("❌ Tapılmadı.")
            data = info['entries'][0] if 'entries' in info else info
            title = temiz_ad(data.get("title", "Audio"))
            path = ydl.prepare_filename(data).rsplit(".", 1)[0]
            mp3 = f"{path}.mp3"
            thumb = None
            for ex in ['jpg', 'png', 'webp', 'jpeg']:
                if os.path.exists(f"{path}.{ex}"):
                    thumb = f"{path}.{ex}"
                    break
        await event.edit(f"📤 `{title}`...")
        await event.client.send_file(
            event.chat_id, mp3, thumb=thumb,
            caption=f"🎵 **{title}**\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```"
        )
        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta: `{str(e)}`")
    finally:
        for f in os.listdir(out_dir):
            if f.startswith(os.path.basename(path)):
                try: os.remove(os.path.join(out_dir, f))
                except: pass

CmdHelp("musicdownloader").add_command("mp3", "ad", "Mahnı yükləyir sadəcə mahnı adını yazın").add_sahib("[SILGI](https://t.me/silgiteam)").add()
