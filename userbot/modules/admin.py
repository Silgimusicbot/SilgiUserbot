

from asyncio import sleep
from os import remove

from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest, InviteToChannelRequest)
from telethon.tl.functions.messages import (UpdatePinnedMessageRequest, AddChatUserRequest, ExportChatInviteRequest)
from telethon.tl.types import (PeerChannel, ChannelParticipantsAdmins,
                               ChatAdminRights, ChatBannedRights,
                               MessageEntityMentionName, MessageMediaPhoto,
                               ChannelParticipantsBots, User, InputPeerChat)
from telethon.events import ChatAction
from userbot import BOTLOG, BOTLOG_CHATID, BRAIN_CHECKER, CMD_HELP, bot, WARN_MODE, WARN_LIMIT, WHITELIST, SUDO_ID
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from userbot.cmdhelp import CmdHelp
import datetime

# =================== CONSTANT ===================
# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("admin")

# ████████████████████████████████ #

PP_TOO_SMOL = LANG['PP_TOO_SMOL']
PP_ERROR = LANG['PP_ERROR']
NO_ADMIN = LANG['NO_ADMIN']
NO_PERM = LANG['NO_PERM']
NO_SQL = LANG['NO_SQL']

CHAT_PP_CHANGED = LANG['CHAT_PP_CHANGED']
CHAT_PP_ERROR = LANG['CHAT_PP_ERROR']
INVALID_MEDIA = LANG['INVALID_MEDIA']

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================

@register(outgoing=True, pattern="^.elave ?(.*)")
async def elave(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit(LANG['EKLE_PRIVATE'])
    else:
        if not event.is_channel and event.is_group:
            for user_id in to_add_users.split(" "):
                await event.edit(f'`{user_id} qrupa əlavə edilir...`')
                try:
                    await event.client(AddChatUserRequest(
                        chat_id=event.chat_id,
                        user_id=user_id,
                        fwd_limit=1000000
                    ))
                except Exception as e:
                    await event.edit(f'`{user_id} qrupa əlavə edilmədi!`')
                    continue
                await event.edit(f'`{user_id} qrupa edildi!`')
        else:
            for user_id in to_add_users.split(" "):
                await event.edit(f'`{user_id} qrupa əlavə edilir...`')
                try:
                    await event.client(InviteToChannelRequest(
                        channel=event.chat_id,
                        users=[user_id]
                    ))
                except Exception as e:
                    await event.edit(f'`{user_id} qrupa əlavə edilmədi!`')
                    continue
                await event.edit(f'`{user_id} qrupa əlavə edildi!`')

@register(outgoing=True, pattern="^.gban(?: |$)(.*)")
async def gbanspider(gspdr):
    """ .gban  """
    # 
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # 
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # 
    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    # 
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await gspdr.edit(LANG['BRAIN'])
        return

    #.
    await gspdr.edit(LANG['BANNING'])
    if gban(user.id) == False:
        await gspdr.edit(
            LANG['ALREADY_GBANNED'])
    else:
        if reason:
            await gspdr.edit(f"{LANG['GBANNED_REASON']} {reason}")
        else:
            await gspdr.edit(LANG['GBANNED'])

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)")


@register(incoming=True)
async def gbanmsg(moot):
    """ """
    try:
        from userbot.modules.sql_helper.gban_sql import is_gbanned
    except:
        return

    gbanned = is_gbanned(str(moot.sender_id))
    if gbanned == str(moot.sender_id):
        try:
            chat = await moot.get_chat()
        except:
            return
            
        if (type(chat) == User):
            return 

        admin = chat.admin_rights
        creator = chat.creator

        if not admin and not creator:
            return

        try:
            await moot.client(EditBannedRequest(moot.chat_id, moot.sender_id,
                                            BANNED_RIGHTS))
            await moot.reply(LANG['GBAN_TEXT'])
        except:
            return

@register(outgoing=True, pattern="^.ungban(?: |$)(.*)")
async def ungban(un_gban):
    """ .ungban  """
    # 
    chat = await un_gban.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # 
    if not admin and not creator:
        await un_gban.edit(NO_ADMIN)
        return

    # 
    try:
        from userbot.modules.sql_helper.gban_sql import ungban
    except:
        await un_gban.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gban)
    user = user[0]
    if user:
        pass
    else:
        return

    await un_gban.edit(LANG['UNGBANNING'])

    if ungban(user.id) is False:
        await un_gban.edit(LANG['NO_BANNED'])
    else:
        # 
        await un_gban.edit(LANG['UNGBANNED'])

        if BOTLOG:
            await un_gban.client.send_message(
                BOTLOG_CHATID, "#UNGBAN\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {un_gban.chat.title}(`{un_gban.chat_id}`)")


@register(outgoing=True, pattern="^.setgpic$")
async def set_group_photo(gpic):
    """ .setgpic """
    if not gpic.is_group:
        await gpic.edit(LANG['PRIVATE'])
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await
                                 gpic.client.upload_file(photo)))
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)

@register(outgoing=True, pattern=r"^.(promote|spromote|apromote)(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern=r"^.(promote|spromote|apromote)(?: |$)(.*)")
async def promote(event):
    """ .promote | .spromote | .apromote """
    
    args = event.pattern_match.group(1)  
    input_text = event.pattern_match.group(2)  

    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await event.edit(NO_ADMIN)
        return

    try:
        result = await get_user_from_event(event)
        if result is None:
            await event.edit("❌ İstifadəçi tapılmadı və ya xəta baş verdi.")
            return

        user, user_rank = result

      
        rank_text = input_text.split(maxsplit=1)[1] if input_text and " " in input_text else None

        if args == "spromote":
            rank = "SPAM"  
        elif rank_text:  
            rank = rank_text
        else:
            rank = "Admin"


        if args == "apromote":
            new_rights = ChatAdminRights(
                add_admins=True,  
                invite_users=True,
                change_info=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                manage_call=True
            )
            role = "Tam Yetkili Admin"

        elif args == "spromote":
            new_rights = ChatAdminRights(
                invite_users=True,
                change_info=False,
                ban_users=False,
                delete_messages=False,
                pin_messages=False,
                add_admins=False,
                manage_call=False
            )
            role = "SPAM Admin"

        elif args == "promote":
            new_rights = ChatAdminRights(
                add_admins=False,  
                invite_users=True,
                change_info=False,
                ban_users=False,
                delete_messages=True,
                pin_messages=True,
                manage_call=True
            )
            role = "Admin"

        
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
        await event.edit(f"✅ **{role}** verildi: [{user.first_name}](tg://user?id={user.id})\n🎖 Rütbə: **{rank}**")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, 
                f"#ADMİNLİK\nİSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\nQRUP: {event.chat.title}(`{event.chat_id}`)\nVERİLƏN ROL: {role}\nRÜTBƏ: {rank}"
            )

    except ValueError as e:
        await event.edit(f"❌ {str(e)}")
    except Exception as e:
        await event.edit(f"❌ Xəta baş verdi: {str(e)}")  # Xəta mesajını göstər


@register(outgoing=True, pattern="^.demote(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.demote(?: |$)(.*)")
async def demote(dmod):
    """ .demote """
    # 
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # 
    await dmod.edit(LANG['UNPROMOTING'])
    rank = "admeme"  # 
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    # 
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    # 
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # 
    # 
    except:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit(LANG['UNPROMOTE'])

    # 
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#ADMİNLİKALMA\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {dmod.chat.title}(`{dmod.chat_id}`)")


@register(outgoing=True, pattern="^.ban(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.ban(?: |$)(.*)")
async def ban(bon):
    """ .ban"""
    # 
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    # 
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await bon.edit(
            LANG['BRAIN']
        )
        return

    # 
    await bon.edit(LANG['BANNING'])

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except:
        await bon.edit(NO_PERM)
        return
    # 
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except:
        await bon.edit(
            LANG['NO_PERM_BUT_BANNED'])
        return
    # 
    # 
    SONMESAJ = PLUGIN_MESAJLAR['ban'].format(
        id = user.id,
        username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
        first_name = user.first_name,
        last_name = '' if not user.last_name else user.last_name,
        mention = f"[{user.first_name}](tg://user?id={user.id})",
        date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
        count = (chat.participants_count - 1) if chat.participants_count else 'Bilinmiyor'
    )
    
    if reason:
        await bon.edit(f"{SONMESAJ}\n{LANG['REASON']}: {reason}")
    else:
        await bon.edit(SONMESAJ)
    # 
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID, "#BAN\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {bon.chat.title}(`{bon.chat_id}`)")


@register(outgoing=True, pattern="^.unban(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.unban(?: |$)(.*)")
async def nothanos(unbon):
    """ .unban """
    # 
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    # 
    await unbon.edit(LANG['UNBANNING'])

    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit(LANG['UNBANNED'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmiyor'
        ))

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID, "#UNBAN\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {unbon.chat.title}(`{unbon.chat_id}`)")
    except:
        await unbon.edit(LANG['EXCUSE_ME_WTF'])


@register(outgoing=True, pattern="^.mute(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.mute(?: |$)(.*)")
async def spider(spdr):
    """

    """
    # 
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except:
        await spdr.edit(NO_SQL)
        return

    # 
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # 
    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    # 
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await spdr.edit(
            LANG['BRAIN']
        )
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        await spdr.edit(
            LANG['NO_MUTE_ME'])
        return

    # 
    await spdr.edit(LANG['MUTING'])
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit(LANG['ALREADY_MUTED'])
    else:
        try:
            await spdr.client(
                EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            await mutmsg(spdr, user, reason, chat)
        except UserAdminInvalidError:
            await mutmsg(spdr, user, reason, chat)
        except:
            return await spdr.edit(LANG['WTF_MUTE'])


async def mutmsg(spdr, user, reason, chat):
    # 
    SONMESAJ = PLUGIN_MESAJLAR['mute'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmiyor'
        )

    if reason:
        await spdr.edit(f"{SONMESAJ}\n{LANG['REASON']}: {reason}")
    else:
        await spdr.edit(f"{SONMESAJ}")

    # 
    if BOTLOG:
        await spdr.client.send_message(
            BOTLOG_CHATID, "#MUTE\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {spdr.chat.title}(`{spdr.chat_id}`)")


@register(outgoing=True, pattern="^.unmute(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.unmute(?: |$)(.*)")
async def unmoot(unmot):
    """ .unmute """
    # 
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator


    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    # 
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except:
        await unmot.edit(NO_SQL)
        return

    await unmot.edit(LANG['UNMUTING'])
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit(LANG['ALREADY_UNMUTED'])
    else:

        try:
            await unmot.client(
                EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit(LANG['UNMUTED'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmiyor'
        ))
        except UserAdminInvalidError:
            await unmot.edit(LANG['UNMUTED'].format(
            id = user.id,
            username = '@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name = user.first_name,
            last_name = '' if not user.last_name else user.last_name,
            mention = f"[{user.first_name}](tg://user?id={user.id})",
            date = datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count = (chat.participants_count) if chat.participants_count else 'Bilinmiyor'
        ))
        except:
            await unmot.edit(LANG['WTF_MUTE'])
            return

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID, "#UNMUTE\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {unmot.chat.title}(`{unmot.chat_id}`)")


@register(incoming=True)
async def muter(moot):
    """ """
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                try:
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id, rights))
                except:
                    pass
    if gmuted:
        for i in gmuted:
            if i.sender == str(moot.sender_id):
                await moot.delete()

@register(outgoing=True, pattern="^.ungmute(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.ungmute(?: |$)(.*)")
async def ungmoot(un_gmute):
    """ .ungmute  """
    # 
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # 
    if not admin and not creator:
        await un_gmute.edit(NO_ADMIN)
        return

    # 
    try:
        from userbot.modules.sql_helper.gmute_sql import ungmute
    except:
        await un_gmute.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if user:
        pass
    else:
        return

    await un_gmute.edit(LANG['GUNMUTING'])

    if ungmute(user.id) is False:
        await un_gmute.edit(LANG['NO_GMUTE'])
    else:
        # 
        await un_gmute.edit(LANG['UNMUTED'])

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID, "#UNGMUTE\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {un_gmute.chat.title}(`{un_gmute.chat_id}`)")


@register(outgoing=True, pattern="^.gmute(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.gmute(?: |$)(.*)")
async def gspider(gspdr):
    """ .gmute """
    # 
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # 
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # 
    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    # 
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await gspdr.edit(LANG['BRAIN'])
        return

    # 
    await gspdr.edit(LANG['GMUTING'])
    if gmute(user.id) == False:
        await gspdr.edit(
            LANG['ALREADY_GMUTED'])
    else:
        if reason:
            await gspdr.edit(f"{LANG['GMUTED']} {LANG['REASON']}: {reason}")
        else:
            await gspdr.edit(LANG['GMUTED'])

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)")


@register(outgoing=True, pattern="^.zombies(?: |$)(.*)", groups_only=False)
async def rm_deletedacc(show):
    """ .zombies """

    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = LANG['NO_ZOMBIE']

    if con != "clean":
        await show.edit(LANG['ZOMBIE'])
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = LANG['ZOMBIES'].format(del_u)
        await show.edit(del_status)
        return

    #
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await show.edit(LANG['NO_ADMIN'])
        return

    await show.edit(LANG['CLEANING'])
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            except:
                await show.edit(LANG['NO_BAN_YT'])
                return
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"**{del_u}** {LANG['DELETED']}"

    if del_a > 0:
        del_status = f"**{del_u}** {LANG['DELETED']} \
        \n**{del_a}** dənə silinmiş olan admin hesabları çıxarılmadı"

    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID, "#TEMIZLIK\n"
            f"**{del_u}** tane silinmiş hesap çıkartıldı !!\
            \nQRUP: {show.chat.title}(`{show.chat_id}`)")


@register(outgoing=True, pattern="^.admins$")
async def get_admin(show):
    """ .admins  """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b>{title} {LANG["ADMINS"]}:</b> \n'
    try:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsAdmins):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nDeleted Account <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@register(outgoing=True, pattern="^.pin(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.pin(?: |$)(.*)")
async def pin(msg):
    """ .pin  """
    # 
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # 
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit(LANG['NEED_MSG'])
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except:
        await msg.edit(NO_PERM)
        return

    await msg.edit(LANG['PINNED'])

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}")


@register(outgoing=True, pattern="^.kick(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.kick(?: |$)(.*)")
async def kick(usr):
    """ .kick """
    # 
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # 
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit(LANG['NOT_FOUND'])
        return

    # 
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await usr.edit(
            LANG['BRAIN']
        )
        return

    await usr.edit(LANG['KICKING'])

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `{LANG['KICKED']}`\n{LANG['REASON']}: {reason}"
        )
    else:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `{LANG['KICKED']}`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#KICK\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {usr.chat.title}(`{usr.chat_id}`)\n")


@register(outgoing=True, pattern="^.users ?(.*)")
async def get_users(show):
    """ .users """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '{} QruPunda tapılam istifadəçilər: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nSilinən hesab `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nSilinən hesab `{user.id}`"
    except Exception as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Lənət olsun, bu böyük bir qrupdur. İstifadəçi listini fayl olaraq göndərirəm.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption='{} qrupundakı istifadəçilər'.format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """  """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`İstifadəçi adı, ID'sini vəya mesajını yönləndirin!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except Exception as err:
        await event.edit(str(err))
        return None

    return user_obj

@register(outgoing=True, pattern="^.unwarn ?(.*)")
async def unwarn(event):
    """ .unwarn """
    # 
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # 
    if not admin and not creator:
        await event.edit(NO_ADMIN)
        return

    # 
    try:
        import userbot.modules.sql_helper.warn_sql as warn
    except:
        await event.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    # 
    await event.edit(LANG['UNWARNING'])
    silme = warn.sil_warn(user.id)
    if silme == False:
        await event.edit(LANG['UNWARNED'])
        return

    warnsayi = warn.getir_warn(user.id)
    
    await event.edit(f"[{user.first_name}](tg://user?id={user.id})`, {LANG['UNWARN']} {warnsayi}/{WARN_LIMIT}`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#WARN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")

@register(outgoing=True, pattern="^.warn ?(.*)")
async def warn(event):
    """ .warn """
    # 
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # 
    if not admin and not creator:
        await event.edit(NO_ADMIN)
        return

    # 
    try:
        import userbot.modules.sql_helper.warn_sql as warn
    except:
        await event.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    # 
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await event.edit(LANG['BRAIN'])
        return

    # 
    await event.edit(LANG['WARNING'])
    warn.ekle_warn(user.id)
    warnsayi = warn.getir_warn(user.id)
    if warnsayi >= WARN_LIMIT:
        if WARN_MODE == "gban":
            await Warn_Gban(event, warn, user)
        else:
            await Warn_Gmute(event, warn, user)
        return
    await event.edit(f"[{user.first_name}](tg://user?id={user.id})`, {warnsayi}/{WARN_LIMIT} {LANG['WARN']}`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#WARN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")

async def Warn_Gmute(event, warn, user, reason = None):
    await event.delete()
    yeni = await event.reply(f"`Səni yetəri qədər xəbərdar etdim` [{user.first_name}](tg://user?id={user.id})`, qlobal olaraq susduruldun!`")

    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except:
        await yeni.edit(NO_SQL)
        return
        
    yeni2 = await yeni.reply("`Susdurulur...`")
        
    if gmute(user.id) == False:
        await yeni2.edit(
            '`Xəta! İstifadəçi onsuz qlobal olaraq susdurulub.`')
    else:
        if reason != None:
            await yeni2.edit(f"`İstifadəçi qlobal olaraq susduruldu!`Səbəbi: {reason}")
        else:
            await yeni2.edit("`İstifadəçi qlobal olaraq susduruldu!`")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)")
    warn.toplu_sil_warn(user.id)

async def Warn_Gban(event, warn, user, reason = None):
    await event.delete()
    yeni = await event.reply(f"`Səni yetəri qədər xəbərdar etdim` [{user.first_name}](tg://user?id={user.id})`, qlobal olaraq banlandın!`")

    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except:
        await yeni.edit(NO_SQL)
        return
        
    yeni2 = await yeni.reply("`Banlanır...`")
        
    if gban(user.id) == False:
        await yeni2.edit(
            '`Xəta! İstifadəçi onsuz qlobal olaraq banlanıb.`')
    else:
        if reason != None:
            await yeni2.edit(f"`İstifadəçi qlobal olaraq banlandı!`Səbəbi: {reason}")
        else:
            await yeni2.edit("`İstifadəçi qlobal olaraq banlandı!`")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#GBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)")
    warn.toplu_sil_warn(user.id)

@register(outgoing=True, pattern="^.usersdel ?(.*)")
async def get_usersdel(show):
    """ .usersdel  """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '{} qrupunda tapılman silinməyən hesablar: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
         #       else:
    #                mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
         #       else:
      #              mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Lənət olsun, bu böyük qrupdur. Silinməyən istifadəçilər listini fayl olaraq göndərirəm.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "deleteduserslist.txt",
            caption='{} qrupuna aid olan silinmiş hesablar:'.format(title),
            reply_to=show.id,
        )
        remove("deleteduserslist.txt")


async def get_userdel_from_event(event):
    """ . """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Silinməyən istifadəçinin istifadəçi adını, ID'sini vəya mesajını yönləndirin`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_userdel_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except Exception as err:
        await event.edit(str(err))
        return None

    return user_obj


@register(outgoing=True, pattern="^.bots$", groups_only=True)
async def get_bots(show):
    """ .bots  """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b> {title} qrupunda tapılan botlar:</b>\n'
    try:
       # if isinstance(message.to_id, PeerChat):
        #    await show.edit("`Sadəcə super qrupların botlara sahib ola biləcəyini eşitdim.`")
        #   return
       # else:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsBots):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nSilinmiş bot <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await show.edit(
            "Lənət olsun, burda çox bot var. Botların listini fayl olaraq göndərirəm.")
        file = open("botlist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "botlist.txt",
            caption='{} qrubunda tapılam botlar:'.format(title),
            reply_to=show.id,
        )
        remove("botlist.txt")

@register(outgoing=True, pattern="^.getlink", groups_only=True)
async def _(event):
    await event.edit("Hazırlanır...")
    try:
        e = await event.client(
        ExportChatInviteRequest(event.chat_id),
        )
    except ChatAdminRequiredError:
        return await event.edit(NO_ADMIN)
        sleep(7)
        await event.delete()
    await event.edit(f"Link: {e.link}")

@register(outgoing=True, pattern="^.recent ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    say = event.pattern_match.group(1)
    c = await event.get_chat()
    qrup = c.title
    if c.admin_rights or c.creator:
        a = await bot.get_admin_log(event.chat_id, limit=5, edit=False, delete=True)
        deleted_msg = f"{qrup} qrupunda silinmiş son 5 mesaj:**"
        for i in a:
            deleted_msg += "\n-> __{}__".format(i.old.message)
        await event.edit(deleted_msg)
    else:
        await event.edit("`Bunun üçün admin olmalısan`")
        await asyncio.sleep(5)
        await event.delete()


CmdHelp('admin').add_command(
        'promote', (LANG['PROMOTE1']), (LANG['PROMOTE2'])
    ).add_command(
        'demote', (LANG['DEMOTE1']), (LANG['DEMOTE2'])
    ).add_command(
        'ban', (LANG['BAN1']), (LANG['BAN2'])
    ).add_command(
        'unban', (LANG['UNBAN1']), (LANG['UNBAN2'])
    ).add_command(
        'mute', (LANG['MUTE1']), (LANG['MUTE2'])
    ).add_command(
        'unmute', (LANG['UNMUTE1']), (LANG['UNMUTE2'])
    ).add_command(
        'kick', (LANG['KICK1']), (LANG['KICK2'])
    ).add_command(
        'gmute', (LANG['GMUTE1']), (LANG['GMUTE2'])
    ).add_command(
        'ungmute', (LANG['UNGMUTE1']), (LANG['UNGMUTE2'])
    ).add_command(
        'zombies', None, (LANG['ZOMBI1'])
    ).add_command(
        'admins', None, (LANG['ADMINS1'])
    ).add_command(
        'bots', None, (LANG['BOTS1'])
    ).add_command(
        'users', None, (LANG['USERS1'])
    ).add_command(
        'usersdel', None, (LANG['USERDEL1'])
    ).add_command(
        'warn', (LANG['WARN1']), (LANG['WARN2'])
    ).add_command(
        'unwarn', (LANG['UNWARN1']), (LANG['UNWARN2'])
    ).add_command(
        'add', (LANG['ELAVE1']), (LANG['ELAVE2'])
    ).add_command(
        'gban', (LANG['GBAN1']), (LANG['GBAN2'])
    ).add_command(
        'ungban', (LANG['UNGBAN1']), (LANG['UNGBAN2'])
    ).add_command(
        'pin', (LANG['PIN1']), (LANG['PIN2'])
    ).add_command(
        'setgpic', (LANG['QS1']), (LANG['QS2'])
    ).add_command(
        'getlink', None, 'Qrup linkini verər'
    ).add_command(
        'recent', None, 'Qrupda silinmiş son 5 mesajı göstərər'
    ).add()
