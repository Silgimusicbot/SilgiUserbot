import os
import re
import asyncio
from pytubefix import YouTube, Search
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp
from userbot import shirniyat

def zererli(ad):
    return re.sub(r'[\\/*?:"<>|]', "", ad)

def axtaris_et(query, is_audio=False):
    client_tipi = 'ANDROID_MUSIC' if is_audio else 'ANDROID'
    
    if query.startswith("http"):
        return YouTube(query, client=client_tipi, use_po_token=True)
        
    s = Search(query)
    if s.videos:
        yt = s.videos[0]
        yt.client = client_tipi
        return yt
    return None

def yukle_audio(yt):
    stream = yt.streams.get_audio_only()
    f_name = f"{zererli(yt.title)}.mp3"
    return stream.download(output_path="downloads", filename=f_name)

def yukle_video(yt):
    stream = yt.streams.get_highest_resolution()
    f_name = f"{zererli(yt.title)}.mp4"
    return stream.download(output_path="downloads", filename=f_name)

@silgi(outgoing=True, pattern=r"\.ytmp3(?: |$)(.*)")
async def ytaudio(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.edit("ℹ️ Mahnı adı və ya link daxil edin.")
    
    await event.edit("🔄 `Pytubefix: Axtarılır...`")
    os.makedirs("downloads", exist_ok=True)
    
    try:
        yt = await asyncio.to_thread(axtaris_et, query, True)
        if not yt:
            return await event.edit("❌ Nəticə tapılmadı.")
        
        title = zererli(yt.title)
        await event.edit(f"📥 `{title}` yüklənir...")
        
        file_path = await asyncio.to_thread(yukle_audio, yt)
        
        await event.edit(f"📤 `{title}` göndərilir...")
        await event.client.send_file(
            event.chat_id, 
            file_path, 
            caption=f"🎶 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```"
        )
        await event.delete()
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        await event.edit(f"❌ Xəta: `{str(e)}`")

@silgi(outgoing=True, pattern=r"\.ytvideo(?: |$)(.*)")
async def ytvideo(event):
    query = event.pattern_match.group(1).strip()
    if not query:
        return await event.edit("ℹ️ Video adı və ya link daxil edin.")
    
    await event.edit("🔄 `Pytubefix: Axtarılır...`")
    os.makedirs("downloads", exist_ok=True)
    
    try:
        yt = await asyncio.to_thread(axtaris_et, query, False)
        if not yt:
            return await event.edit("❌ Nəticə tapılmadı.")
        
        title = zererli(yt.title)
        await event.edit(f"📥 `{title}` yüklənir...")
        
        file_path = await asyncio.to_thread(yukle_video, yt)
        
        await event.edit(f"📤 `{title}` göndərilir...")
        await event.client.send_file(
            event.chat_id, 
            file_path, 
            caption=f"🎥 `{title}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```", 
            supports_streaming=True
        )
        await event.delete()
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        await event.edit(f"❌ Xəta: `{str(e)}`")

CmdHelp("youtube").add_command("ytmp3", "ad/link", "Mahnı yükləyir.").add_command("ytvideo", "ad/link", "Video yükləyir.").add_sahib("[SILGI](https://t.me/silgiteam)").add()
