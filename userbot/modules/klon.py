import os
import tempfile
from telethon.tl import functions
from telethon.tl.functions.photos import GetUserPhotosRequest, DeletePhotosRequest
from userbot.events import register
from userbot import BRAIN_CHECKER, WHITELIST
from userbot.language import get_value

LANG = get_value("userbot")

old_first_name = None
old_last_name = None
old_profile_photo = None
old_bio = None
old_had_photo = False
async def get_user(event):
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        if reply_message and reply_message.sender_id:
            try:
                return await event.client.get_entity(reply_message.sender_id)
            except Exception:
                return None
        return None
    user = event.pattern_match.group(1)
    if user:
        user = user.strip()
        if not user:
            return None
        try:
            if user.isnumeric():
                return await event.client.get_entity(int(user))
            return await event.client.get_entity(user)
        except Exception:
            return None
    return None
async def get_bio(client, user_id):
    try:
        full = await client(functions.users.GetFullUserRequest(user_id))
        return getattr(full.full_user, "about", "") or ""
    except Exception:
        return ""
async def delete_all_my_photos(client):
    try:
        photos = await client(GetUserPhotosRequest(
            user_id="me",
            offset=0,
            max_id=0,
            limit=100
        ))
        if photos and getattr(photos, "photos", None):
            await client(DeletePhotosRequest(id=photos.photos))
    except Exception:
        pass
@register(outgoing=True, pattern=r"^.klon(?: |$)(.*)")
async def clone(event):
    global old_first_name, old_last_name, old_profile_photo, old_bio, old_had_photo
    if event.fwd_from:
        return
    replied_user = await get_user(event)
    if replied_user is None:
        await event.edit("❗ User tapılmadı. Reply et və ya username/id yaz.")
        return
    if replied_user.id in BRAIN_CHECKER or replied_user.id in WHITELIST:
        await event.edit(LANG["SILGI"])
        return
    me = await event.client.get_me()
    old_first_name = me.first_name or ""
    old_last_name = me.last_name or ""
    old_bio = await get_bio(event.client, me.id)
    old_profile_photo = None
    old_had_photo = False
    try:
        temp_dir = tempfile.gettempdir()
        my_old_photo_path = os.path.join(temp_dir, f"silgi_old_me_{me.id}.jpg")
        if os.path.exists(my_old_photo_path):
            os.remove(my_old_photo_path)
        downloaded = await event.client.download_profile_photo(me, file=my_old_photo_path)
        if downloaded and os.path.exists(downloaded):
            old_profile_photo = downloaded
            old_had_photo = True
    except Exception:
        old_profile_photo = None
        old_had_photo = False
    target_first_name = replied_user.first_name or ""
    target_last_name = replied_user.last_name or ""
    target_bio = await get_bio(event.client, replied_user.id)
    await event.client(functions.account.UpdateProfileRequest(
        first_name=target_first_name,
        last_name=target_last_name,
        about=target_bio
    ))
    try:
        temp_dir = tempfile.gettempdir()
        target_photo_path = os.path.join(temp_dir, f"silgi_clone_{replied_user.id}.jpg")
        if os.path.exists(target_photo_path):
            os.remove(target_photo_path)
        downloaded_target = await event.client.download_profile_photo(
            replied_user,
            file=target_photo_path
        )
        if downloaded_target and os.path.exists(downloaded_target):
            await delete_all_my_photos(event.client)
            uploaded = await event.client.upload_file(downloaded_target)
            await event.client(functions.photos.UploadProfilePhotoRequest(file=uploaded))
            try:
                os.remove(downloaded_target)
            except Exception:
                pass
            await event.edit("✅ Axalay maxalay puf! Profil klonlandı.")
            return
    except Exception:
        pass
    await delete_all_my_photos(event.client)
    await event.edit("⚠️ Profil şəkli tapılmadı. Sadəcə ad, soyad və bio klonlandı.")
@register(outgoing=True, pattern=r"^.revert$")
async def revert(event):
    global old_first_name, old_last_name, old_profile_photo, old_bio, old_had_photo
    if event.fwd_from:
        return
    if (
        old_first_name is None and
        old_last_name is None and
        old_profile_photo is None and
        old_bio is None
    ):
        await event.edit("❗ Köhnə profil məlumatları tapılmadı.")
        return
    await event.client(functions.account.UpdateProfileRequest(
        first_name=old_first_name or "",
        last_name=old_last_name or "",
        about=old_bio or ""
    ))
    await delete_all_my_photos(event.client)
    if old_had_photo and old_profile_photo and os.path.exists(old_profile_photo):
        try:
            uploaded = await event.client.upload_file(old_profile_photo)
            await event.client(functions.photos.UploadProfilePhotoRequest(file=uploaded))
        except Exception:
            pass
    await event.edit("✅ Axalay maxalay puf! Profil geri qayıtdı.")
    if old_profile_photo and os.path.exists(old_profile_photo):
        try:
            os.remove(old_profile_photo)
        except Exception:
            pass
    old_first_name = None
    old_last_name = None
    old_profile_photo = None
    old_bio = None
    old_had_photo = False
