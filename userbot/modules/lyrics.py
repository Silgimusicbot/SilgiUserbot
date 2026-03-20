import requests
import io
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp


@silgi(outgoing=True, pattern=r"^\.lyrics (.*)")
async def lrclib_soz(event):
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("`Zəhmət olmasa bir mahnı adı qeyd edin!`")
    await event.edit(f"🔍 **'{query}'** axtarılır...")
    try:
        response = requests.get(f"https://lrclib.net/api/search?q={query}")
        data = response.json()
        if not data:
            return await event.edit("❌ **Mahnı sözləri tapılmadı.**")
        track = data[0]
        artist = track.get("artistName", "Naməlum")
        title = track.get("trackName", "Adsız")
        lyrics = track.get("plainLyrics")
        if not lyrics:
            return await event.edit(f"❌ **{artist} - {title}** üçün sözlər yoxdur.")
        son_mesaj = f"🎵 **{title}** - __{artist}__\n\n```{lyrics}```\n\n```⚝ 𝑺𝑰𝑳𝑮I 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```"
        if len(son_mesaj) > 4096:
            await event.edit("📝 **Sözlər çox uzun olduğu üçün fayl hazırlanır...**")
            file_content = f"Mahnı: {title}\nİfaçı: {artist}\n\n{lyrics}\n\n⚝ 𝑺𝑰𝑳𝑮I 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝"
            file = io.BytesIO(file_content.encode('utf-8'))
            file.name = f"{artist}_{title}_lyrics.txt"
            await event.client.send_file(
                event.chat_id,
                file,
                caption=f"🎵 **{title}** - __{artist}__\n\n`⚝ 𝑺𝑰𝑳𝑮I 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝`",
                reply_to=event.reply_to_msg_id
            )
            await event.delete()
        else:
            await event.edit(son_mesaj)
    except Exception as e:
        await event.edit(f"⚠️ **Xəta:** `{str(e)}`")

CmdHelp("lyrics").add_command(
    "lyrics", 
    "mahnı adı", 
    "Mahnı sözləri tapır."
).add_sahib(
    "[SILGI](https://t.me/silgiteam)"
).add()
