# SilgiUserbot a aiddir. Bunu əkən sənin lişni varını yoxunu 7 cəddini sikim
from telethon import events
from userbot.events import register
from userbot.cmdhelp import CmdHelp
import os
from datetime import datetime

uid = None

@register(outgoing=True, pattern=r"^\.vw$")
async def save_media(event):
    global uid

    if not uid:
        me = await event.client.get_me()
        uid = me.id

    if event.sender_id != uid:
        return

    await event.delete()
    msg = await event.client.send_message(uid, "Yüklənir...")

    if not event.reply_to_msg_id:
        await msg.delete()
        return await event.reply("Media olan mesaja reply verin zəhmət olmasa.", ttl=7)

    reply_msg = await event.get_reply_message()
    if not reply_msg or not reply_msg.media:
        await msg.edit("Reply etdiyiniz mesajda media yoxdur.")
        return

    folder = "downloads"
    if not os.path.isdir(folder):
        os.makedirs(folder)

    start_time = datetime.now()

    filename = None
    if hasattr(reply_msg.media, "document"):
        doc = reply_msg.media.document
        filename = doc.file_name or "unknown_file"
        try:
            filename = await event.client.download_media(reply_msg, file=f"{folder}/{filename}")
        except Exception as e:
            await msg.edit(f"Yükləmək alınmadı: {e}")
            return
    else:
        filename = await event.client.download_media(reply_msg, folder)

    end_time = datetime.now()
    delta = (end_time - start_time).seconds * 1000

    if filename and os.path.isfile(filename):
        await event.client.send_file("me", filename, caption=f"{reply_msg.sender_id} tərəfindən yadda saxlandı.")
    else:
        await event.client.send_message(uid, "Fayl tapılmadı yüklənəndən sonra.")

    await msg.delete()


CmdHelp("viewonce").add_command(
    "vw", None, "Reply etdiyiniz media faylını yadda saxlayır."
).add_info(
    "Bu plugin reply etdiyiniz media faylı sizin Saved Messages çatınıza yükləyir."
).add_warning(
    "Yalnız sizin mesajlarınız üçün işləyir və reply ilə istifadə edilməlidir."
).add_sahib(
    "[SILGI](t.me/SilgiTEAM) tərəfindən hazırlanmışdır. Kodu oğurıamaq istəyən faylı oxusun😉"
).add()