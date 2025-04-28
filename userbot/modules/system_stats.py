from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import uname
from shutil import which
from os import remove
from userbot import CMD_HELP, SILGI_VERSION, SILGI_USER
from telethon.tl.patched import Message
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from telethon import version
from platform import python_version
from userbot.cmdhelp import CmdHelp


# ================= CONSTANT =================
DEFAULTUSER = uname().node
# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("system_stats")

# ████████████████████████████████ #
# ============================================

@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
    """ .sysd """
    try:
        neo = "neofetch --stdout"
        fetch = await asyncrunapp(
            neo,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await fetch.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await sysd.edit("" + result + "")
    except FileNotFoundError:
        await sysd.edit(LANG['NO_NEOFETCH'])


@register(outgoing=True, pattern="^.botver$")
async def bot_ver(event):
    """ .botver"""
    if which("git") is not None:
        invokever = "git describe --all --long"
        ver = await asyncrunapp(
            invokever,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        invokerev = "git rev-list --all --count"
        rev = await asyncrunapp(
            invokerev,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await event.edit(f"{LANG['VERSION']}: "
                         f"{verout}"
                         " \n"
                         f"{LANG['REVOUT']}: "
                         f"{revout}"
                         "")
    else:
        await event.edit(
            "Allah Azərbaycanlıları qorusun 🇦🇿"
        )


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
async def pipcheck(pip):
    """ .pip"""
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit(f"{LANG['SEARCHING']} . . .")
        invokepip = f"pip3 search {pipmodule}"
        pipc = await asyncrunapp(
            invokepip,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit(LANG['BIG'])
                file = open("output.txt", "w+")
                file.write(pipout)
                file.close()
                await pip.client.send_file(
                    pip.chat_id,
                    "output.txt",
                    reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit(f"**{LANG['QUERY']}: **\n"
                           f"{invokepip}"
                           f"\n**{LANG['RESULT']}: **\n"
                           f"{pipout}"
                           "")
        else:
            await pip.edit(f"**{LANG['QUERY']}: **\n"
                           f"{invokepip}"
                           f"\n**{LANG['RESULT']}: **\n{LANG['NOT_FOUND']}.")
    else:
        await pip.edit(LANG['EXAMPLE'])
@register(outgoing=True, pattern="^.malive$")
async def malive(event):
    img = "https://files.catbox.moe/eiqmdh.gif"  
    caption = (
        "**╭━━━➤ 『 BOT STATUS 』\n"
        f"┣• {LANG['ALIVE1']}\n"
        f"┣• {LANG['OK']}\n"
        "╰━━━━━━━━━━━━━━━━━━━\n\n"
        f"╭━━━➤ 『 {LANG['INFO']} 』\n"
        f"┣• 👤 {LANG['NAME']}: {SILGI_USER}\n"
        f"┣• ⚙️ {LANG['PYTHON']}: `{python_version()}`\n"
        f"┣• 🛠️ {LANG['VERSION']}: `{SILGI_VERSION}`\n"
        f"┣• 📚 {LANG['PLUGIN_COUNT']}: `{len(CMD_HELP)}`\n"
        "╰━━━━━━━━━━━━━━━━━━━\n\n"
        "#SilgiUserbot"
    )
    await event.client.send_file(event.chat_id, img, caption=caption)
    await event.delete()
@register(outgoing=True, pattern="^.alive$")
async def amialive(e):
    me = await e.client.get_me()
    if type(PLUGIN_MESAJLAR['alive']) == str:
        await e.edit(PLUGIN_MESAJLAR['alive'].format(
            telethon=version.__version__,
            python=python_version(),
            silgi=SILGI_VERSION,
            plugin=len(CMD_HELP),
            id=me.id,
            username='@' + me.username if me.username else f'[{me.first_name}](tg://user?id={me.id})',
            first_name=me.first_name,
            last_name=me.last_name if me.last_name else '',
            mention=f'[{me.first_name}](tg://user?id={me.id})'
        ))
    else:
        await e.delete()
        if not PLUGIN_MESAJLAR['alive'].text == '':
            PLUGIN_MESAJLAR['alive'].text = PLUGIN_MESAJLAR['alive'].text.format(
                telethon=version.__version__,
                python=python_version(),
                silgi=SILGI_VERSION,
                plugin=len(CMD_HELP),
                id=me.id,
                username='@' + me.username if me.username else f'[{me.first_name}](tg://user?id={me.id})',
                first_name=me.first_name,
                last_name=me.last_name if me.last_name else '',
                mention=f'[{me.first_name}](tg://user?id={me.id})'
            )
        if e.is_reply:
            await e.respond(PLUGIN_MESAJLAR['alive'], reply_to=e.message.reply_to_msg_id)
        else:
            await e.respond(PLUGIN_MESAJLAR['alive'])


CmdHelp('system_stats').add_command(
    'sysd', None, (LANG['SS1'])
).add_command(
    'botver', None, (LANG['SS2'])
).add_command(
    'pip', (LANG['SS3']), (LANG['SS4'])
).add_command(
    'alive', None, (LANG['SS5'])
).add()
