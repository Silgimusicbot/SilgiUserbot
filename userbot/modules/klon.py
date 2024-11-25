import os
from telethon.tl.functions.photos import GetUserPhotosRequest, UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.types import InputPhoto
from telethon.errors.rpcerrorlist import PhotoCropSizeSmallError
from userbot.events import register
from userbot import BRAIN_CHECKER, WHITELIST
from userbot.language import get_value
LANG = get_value("userbot")
original_profile = {
    "first_name": None,
    "last_name": None,
    "about": None,
    "photo": None
}

@register(pattern="^\.klon(?: |$)(.*)", outgoing=True)
async def klon(event):
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        replied_user = await event.client.get_entity(reply_message.sender_id)
    else:
        args = event.pattern_match.group(1)
        if args.isdigit():
            replied_user = await event.client.get_entity(int(args))
        elif args:
            replied_user = await event.client.get_entity(args)
        else:
            await event.edit("🔴 İstifadəçi seçilmədi.")
            return

    if replied_user.id in BRAIN_CHECKER or replied_user.id in WHITELIST:
        await event.edit(LANG['SILGI'])
        return

    global original_profile

    if original_profile["first_name"] is None:
        me = await event.client.get_me()
        original_profile["first_name"] = me.first_name
        original_profile["last_name"] = me.last_name
        original_profile["about"] = (await event.client(functions.account.GetPrivacySettingsRequest())).bio

        photos = await event.client(GetUserPhotosRequest(user_id='me', offset=0, max_id=0, limit=1))
        if photos.photos:
            original_profile["photo"] = photos.photos[0]

    # Kullanıcının profil bilgilerini al ve uygula
    await event.edit("🔄 Klonlama prosesi başladı...")
    try:
        await event.client(UpdateProfileRequest(
            first_name=replied_user.first_name,
            last_name=replied_user.last_name,
            about=(await event.client(functions.account.GetPrivacySettingsRequest(replied_user))).bio
        ))

        photos = await event.client(GetUserPhotosRequest(user_id=replied_user.id, offset=0, max_id=0, limit=1))
        if photos.photos:
            photo = photos.photos[0]
            await event.client(UploadProfilePhotoRequest(photo=InputPhoto(
                id=photo.id,
                access_hash=photo.access_hash,
                file_reference=photo.file_reference
            )))
    except PhotoCropSizeSmallError:
        await event.edit("🔴 Foto çox kiçik olduğu üçün klonlana bilmədi.")

    await event.edit("✅ Axalay maxalay puf! Profil klonlandı.")

@register(pattern="^\.revert$", outgoing=True)
async def revert(event):
    global original_profile

    if not original_profile["first_name"]:
        await event.edit("🔴 Orijinal profil məlumatı tapılmadı.")
        return

    await event.edit("🔄 Orijinal profil geri yüklənir...")
    await event.client(UpdateProfileRequest(
        first_name=original_profile["first_name"],
        last_name=original_profile["last_name"],
        about=original_profile["about"]
    ))

    if original_profile["photo"]:
        await event.client(UploadProfilePhotoRequest(
            photo=InputPhoto(
                id=original_profile["photo"].id,
                access_hash=original_profile["photo"].access_hash,
                file_reference=original_profile["photo"].file_reference
            )
        ))
    else:
        await event.client(DeletePhotosRequest(await event.client.get_profile_photos('me')))

    
    original_profile = {
        "first_name": None,
        "last_name": None,
        "about": None,
        "photo": None
    }

    await event.edit("✅ Axalay maxalay puf! Profil geri qayıtdı.")
