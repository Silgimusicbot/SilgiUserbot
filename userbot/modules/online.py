import asyncio
from telethon.tl.functions.account import UpdateStatusRequest
from userbot.events import register
from userbot.cmdhelp import CmdHelp
online_muddet = None  
@register(outgoing=True, pattern="^.online$")
async def online(event):
    global online_muddet
    if online_muddet:
        await event.edit("**Zatən online rejimindəsən.**")
        return
    await event.edit("**Online rejimi aktivləşdirildi!**")
    async def online_saxla():
        while True:
            try:
                await event.client(UpdateStatusRequest(offline=False))
                await asyncio.sleep(30) 
            except Exception as e:
                print(f"Online saxlama xətası: {e}")
                break
    online_muddet = asyncio.create_task(online_saxla())
@register(outgoing=True, pattern="^.offline$")
async def offline(event):
    global online_muddet
    if online_muddet:
        online_muddet.cancel()
        online_muddet = None
        await event.client(UpdateStatusRequest(offline=True))
        await event.edit("**Artıq offline rejimindəsən.**")
    else:
        await event.edit("**Online rejimi aktiv deyildi.**")
CmdHelp("online").add_command("online", None, "Sizi daimi olaraq Telegramda online göstərər.").add_command(
    "offline", None, "Online rejimini dayandırar və sizi offline edər.").add()