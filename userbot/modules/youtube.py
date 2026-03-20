import os, yt_dlp, re, asyncio
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp
from telethon.tl.types import DocumentAttributeAudio

def ad_normal(s):
    if not s: return "Audio"
    return re.sub(r'[\\/*?:"<>|]', "", s).strip()

@silgi(outgoing=True, pattern=r"\.mp3(?: |$)(.*)")
async def scaudio(event):
    query = event.pattern_match.group(1).strip()
    if not query: return await event.edit("ℹ️ Mahnı adı daxil edin.")
    await event.edit("```🔍 Mahnı axtarılır...```")
    out_dir = "downloads"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{out_dir}/%(id)s.%(ext)s",
        "writethumbnail": True,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
            {"key": "FFmpegThumbnailsConvertor", "format": "jpg"},
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata"}
        ],
        "quiet": True,
        "no_warnings": True
    }
    try:
        search = query if query.startswith("http") else f"scsearch1:{query}"
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search, download=False)
            if not info or 'entries' in info and not info['entries']:
                return await event.edit("❌ Tapılmadı.")
            data = info['entries'][0] if 'entries' in info else info
            title = ad_normal(data.get("title"))
            bot_brand = "⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝"
            await event.edit(f"```🔍 Mahnı axtarılır...\n📥 {title} yüklənir...```")
            await asyncio.to_thread(ydl.process_info, data)
            fid = data.get("id")
            mp3, thumb = f"{out_dir}/{fid}.mp3", f"{out_dir}/{fid}.jpg"
            if not os.path.exists(thumb): thumb = None
        await event.edit(f"```🔍 Mahnı axtarılır...\n📥 {title} yüklənir...\n📤 Göndərilir...```")
        await event.client.send_file(
            event.chat_id, mp3, thumb=thumb,
            caption=f"🎵 **{title}**\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```",
            attributes=[DocumentAttributeAudio(
                duration=int(data.get("duration", 0)),
                title=title,
                performer=bot_brand
            )]
        )
        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta: `{str(e)}`")
    finally:
        if 'fid' in locals():
            for f in os.listdir(out_dir):
                if f.startswith(fid):
                    try: os.remove(os.path.join(out_dir, f))
                    except: pass

CmdHelp("musicdownloader").add_command("mp3", "ad", "Mahnı yükləyir sadəcə mahnı adını yazın").add_sahib("[SILGI](https://t.me/silgiteam)").add()
