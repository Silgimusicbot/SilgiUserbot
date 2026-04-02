# SilgiUserbot a aiddir. Bunu əkən sənin lişni varını yoxunu 7 cəddini sikim
from telethon import events
from telethon.tl.types import DocumentAttributeFilename
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
        return await event.client.send_message(
            uid,
            "Media olan mesaja reply verin zəhmət olmasa.",
            reply_to=event.reply_to_msg_id if event.reply_to_msg_id else None
        )

    reply_msg = await event.get_reply_message()
    if not reply_msg or not reply_msg.media:
        await msg.edit("Reply etdiyiniz mesajda media yoxdur.")
        return

    folder = "downloads"
    if not os.path.isdir(folder):
        os.makedirs(folder)

    start_time = datetime.now()

    try:
        if hasattr(reply_msg.media, "document") and reply_msg.media.document:
            doc = reply_msg.media.document
            filename = "unknown_file"

            for attr in doc.attributes:
                if isinstance(attr, DocumentAttributeFilename):
                    filename = attr.file_name
                    break

            filepath = await event.client.download_media(reply_msg, file=os.path.join(folder, filename))
        else:
            filepath = await event.client.download_media(reply_msg, file=folder)
    except Exception as e:
        await msg.edit(f"Yükləmək alınmadı: {e}")
        return

    end_time = datetime.now()
    delta = (end_time - start_time).seconds * 1000

    if filepath and os.path.isfile(filepath):
        caption = (
            f"{reply_msg.sender_id} tərəfindən yadda saxlandı.\n"
            f"```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```"
        )
        await event.client.send_file("me", filepath, caption=caption)
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
    "[SILGI](t.me/SilgiTEAM) tərəfindən hazırlanmışdır. Kodu oğurlamaq istəyən faylı oxusun😉"
).add()
