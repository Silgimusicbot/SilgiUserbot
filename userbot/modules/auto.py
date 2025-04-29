
import asyncio
import time
from telethon.tl import functions

from userbot import ASYNC_POOL
from userbot.modules.asistant import CMD_HELP
from userbot.events import register
from userbot.cmdhelp import CmdHelp



from userbot.language import get_value
LANG = get_value("auto")



@register(outgoing=True, pattern="^.auto ?(.*)")
async def auto(event):
    metod = event.pattern_match.group(1).lower()
    
    if str(metod) != "ad" and str(metod) != "bio":
        await event.edit(LANG['INVALID_TYPE'])
        return

    if metod in ASYNC_POOL:
        await event.edit(LANG['ALREADY'] % metod)
        return

    await event.edit(LANG['SETTING'] % metod)
    if metod == "ad":
        HM = time.strftime("%H:%M")

        await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            last_name=LANG['NAME'] % HM
        ))
    elif metod == "bio":
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M")

        Bio = LANG['BIO'].format(tarih=DMY, saat=HM) + LANG['NICK'] 
        await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            about=Bio
        ))


    await event.edit(LANG['SETTED'] % metod)

    ASYNC_POOL.append(metod)

    while metod in ASYNC_POOL:
        try:
            if metod == "ad":
                HM = time.strftime("%H:%M")

                await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    last_name=LANG['NAME'] % HM
                ))
            elif metod == "bio":
                DMY = time.strftime("%d.%m.%Y")
                HM = time.strftime("%H:%M")

                Bio = LANG['BIO'].format(tarih=DMY, saat=HM) + LANG['NICK'] 
                await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    about=Bio
                ))

            await asyncio.sleep(60)
        except:
            return

CmdHelp('auto').add_command(
    'auto', (LANG['AUTO1']), (LANG['AUTO2']), (LANG['AUTO3'])
).add()
