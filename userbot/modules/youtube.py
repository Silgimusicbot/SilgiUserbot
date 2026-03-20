import os
import yt_dlp
import re
import asyncio
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp

def zererli(ad):
    return re.sub(r'[\\/*?:"<>|]', "", ad)

@silgi(outgoing=True, pattern=r"\.mp3(?: |$)(.*)")
async def scaudio(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.edit("ℹ️ Mahnı adı və ya link daxil edin.")

    await event.edit("🔄 `Mahnı axtarılır...`")
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    
    # Thumbnail yükləmək və MP3-ə yerləşdirmək üçün parametrlər
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title).50s.%(ext)s"),
        "writethumbnail": True, # Üz qabığını ayrıca fayl kimi yükləyir
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {"key": "EmbedThumbnail"}, # Şəkli MP3 faylının içinə yapışdırır
            {"key": "FFmpegMetadata"}
        ],
        "quiet": True,
        "no_warnings": True
    }

    try:
        search = query if query.startswith("http") else f"scsearch1:{query}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, search, download=True)
            
            if not info or (isinstance(info, dict) and "entries" in info and not info["entries"]):
                return await event.edit("❌ SoundCloud-da mahnı tapılmadı.")
            
            data = info["entries"][0] if "entries" in info else info
            title = zererli(data.get("title", "Audio"))
            
            # Faylın adını və yolunu tapırıq
            base_filepath = ydl.prepare_filename(data).rsplit(".", 1)[0]
            file_path = base_filepath + ".mp3"
            
            # Yüklənmiş şəkli (thumbnail) tapırıq (.jpg, .png və ya .webp ola bilər)
            thumb_path = None
            for ext in ['jpg', 'png', 'webp', 'jpeg']:
                if os.path.exists(f"{base_filepath}.{ext}"):
                    thumb_path = f"{base_filepath}.{ext}"
                    break

        await event.edit(f"📥 `{title}` göndərilir...")
        
        # Telegrama həm mahnını, həm də şəkli (thumb) göndəririk
        await event.client.send_file(
            event.chat_id, 
            file_path, 
            thumb=thumb_path, # Şəkil parametri buradadır
            caption=f"🎶 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```"
        )
        await event.delete()
        
    except Exception as e:
        await event.edit(f"❌ Xəta: `{str(e)}`")
    finally:
        # Həm MP3, həm də şəkil faylını serverdən silib təmizləyirik
        if 'file_path' in locals() and os.path.exists(file_path): 
            os.remove(file_path)
        if 'thumb_path' in locals() and thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)

CmdHelp("musicdownloader").add_command("mp3", "ad", "Mahnı yükləyir sadəcə mahnı adını yazın").add_sahib("[SILGI](https://t.me/silgiteam)").add()
