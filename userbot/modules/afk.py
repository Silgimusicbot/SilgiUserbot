from random import randint
from asyncio import sleep
from telethon.tl.types import Message
from telethon.tl.types import Channel
from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN, SON_GORULME)
from userbot import CMD_HELP, SILGI_USER
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from time import time
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("afk")

# ████████████████████████████████ #

def time_formatter(seconds, short=True):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + (LANG['DAY'] if not short else "g, ")) if days else "") + \
        ((str(hours) + (LANG['HOURS'] if not short else "s, ")) if hours else "") + \
        ((str(minutes) + (LANG['MIN'] if not short else "d, ")) if minutes else "") + \
        ((str(seconds) + (LANG['SEC'] if not short else "s, ")) if seconds else "")
    return tmp[:-2] + LANG['BEFORE']


seen_users = set()

@register(incoming=True, disable_errors=True, disable_edited=True)
async def mention_afk(mention):
    """ ."""
    global COUNT_MSG
    global USERS
    global ISAFK
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            from_user = await mention.get_sender()
            if from_user.username:
                username = '@' + from_user.username
            else:
                username = f'[{from_user.first_name} {from_user.last_name}](tg://user?id={from_user.id})'
            
            mention_format = f'[{from_user.first_name}](tg://user?id={from_user.id})'
            first_name = from_user.first_name

            if from_user.last_name:
                last_name = from_user.last_name
            else:
                last_name = ''

            last_seen_seconds = round(time() - SON_GORULME)
            last_seen = time_formatter(last_seen_seconds)
            last_seen_long = time_formatter(last_seen_seconds, False)

            if mention.sender_id not in USERS:
                if AFKREASON:
                    if type(PLUGIN_MESAJLAR['afk']) is str:
                        await mention.reply(PLUGIN_MESAJLAR['afk'].format(
                        username=username,
                        mention=mention_format,
                        first_name=first_name,
                        last_name=last_name,
                        last_seen_seconds=last_seen_seconds,
                        last_seen=last_seen,
                        last_seen_long=last_seen_long
                    ) \
                            + f"\n{LANG['REASON']}: `{AFKREASON}`\n")
                    else:
                        msj = await mention.reply(PLUGIN_MESAJLAR['afk'])
                        await msj.reply(f"{LANG['REASON']}: `{AFKREASON}`")
                else:
                    if not isinstance(PLUGIN_MESAJLAR['afk'], str):
                        PLUGIN_MESAJLAR['afk'].text = PLUGIN_MESAJLAR['afk'].text.format(
                            username=username,
                            mention=mention_format,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long
                        )
                        await mention.reply(PLUGIN_MESAJLAR['afk'])
                    else:
                        await mention.reply(PLUGIN_MESAJLAR['afk'].format(
                            username=username,
                            mention=mention_format,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long
                        ))
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        if PLUGIN_MESAJLAR['afk'] is str:
                            await mention.reply(PLUGIN_MESAJLAR['afk'].format(
                            username=username,
                            mention=mention_format,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long
                            ) \
                                + f"\n{LANG['REASON']}: `{AFKREASON}`")
                        else:
                            msj = await mention.reply(PLUGIN_MESAJLAR['afk'])
                            await msj.reply(f"{LANG['REASON']}: `{AFKREASON}`")
                    else:
                        if not isinstance(PLUGIN_MESAJLAR['afk'], str):
                            PLUGIN_MESAJLAR['afk'].text = PLUGIN_MESAJLAR['afk'].text.format(
                                username=username,
                                mention=mention_format,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long
                            )
                            await mention.reply(PLUGIN_MESAJLAR['afk'])
                        else:
                            await mention.reply(PLUGIN_MESAJLAR['afk'].format(
                                username=username,
                                mention=mention_format,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long
                            ))

                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ . """
    global ISAFK
    global USERS
    global COUNT_MSG
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        
        from_user = await sender.get_sender()
        if from_user.username:
            username = '@' + from_user.username
        else:
            username = f'[{from_user.first_name} {from_user.last_name}](tg://user?id={from_user.id})'
        
        mention = f'[{from_user.first_name}](tg://user?id={from_user.id})'
        first_name = from_user.first_name

        if from_user.last_name:
            last_name = from_user.last_name
        else:
            last_name = ''

        last_seen_seconds = round(time() - SON_GORULME)
        last_seen = time_formatter(last_seen_seconds)
        last_seen_long = time_formatter(last_seen_seconds, False)

        if apprv and ISAFK:
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(LANG['AFK'].format(
                        username=username,
                        mention=mention,
                        first_name=first_name,
                        last_name=last_name,
                        last_seen_seconds=last_seen_seconds,
                        last_seen=last_seen,
                        last_seen_long=last_seen_long
                    ) \
                    + f"\n{LANG['REASON']}: `{AFKREASON}`")
                else:
                    if not isinstance(PLUGIN_MESAJLAR['afk'], str):
                        PLUGIN_MESAJLAR['afk'].text = PLUGIN_MESAJLAR['afk'].text.format(
                            username=username,
                            mention=mention,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long
                        )
                        await sender.reply(PLUGIN_MESAJLAR['afk'])
                    else:
                        await sender.reply(PLUGIN_MESAJLAR['afk'].format(
                            username=username,
                            mention=mention,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long
                        ))

                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        if type(PLUGIN_MESAJLAR['afk']) is str:
                            await sender.reply(PLUGIN_MESAJLAR['afk'].format(
                                username=username,
                                mention=mention,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long
                            ) \
                            + f"\n{LANG['REASON']}: `{AFKREASON}`")
                        else:
                            msj = await sender.reply(PLUGIN_MESAJLAR['afk'])
                            await msj.reply(f"{LANG['REASON']}: `{AFKREASON}`")
                    else:
                        if not isinstance(PLUGIN_MESAJLAR['afk'], str):
                            PLUGIN_MESAJLAR['afk'].text = PLUGIN_MESAJLAR['afk'].text.format(
                                username=username,
                                mention=mention,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long
                            )
                            await sender.reply(PLUGIN_MESAJLAR['afk'])
                        else:
                            await sender.reply(PLUGIN_MESAJLAR['afk'].format(
                                username=username,
                                mention=mention,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long
                            ))

                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1

@register(outgoing=True, pattern=".afk")
async def go_afk(afk):
    """ . """
    global ISAFK
    global AFKREASON
    global SON_GORULME
    global COUNT_MSG
    if afk.text[0:4] == ".afk":
        reason = afk.text[5:]
        if reason:
            AFKREASON = reason
        else:
            AFKREASON = None
        ISAFK = True
        SON_GORULME = time()
        await afk.reply(LANG['IM_AFK'].format(
            reason=AFKREASON
        ))
        raise StopPropagation

@register(outgoing=True, pattern=".noafk")
async def go_afk_off(afk):
    """ . """
    global ISAFK
    global AFKREASON
    if ISAFK:
        ISAFK = False
        AFKREASON = None
        await afk.reply(LANG['IM_NOT_AFK'])
        raise StopPropagation


  

CmdHelp('afk').add_command('afk', (LANG['AFK1']), (LANG['AFK2'])).add_command('noafk',None, 'Afk modundan çıxarır').add()
