import os
import lyricsgenius
import asyncio

from userbot.events import register
from userbot import CMD_HELP, GENIUS
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("lyrics")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.lyrics(?: |$)(.*)")
async def lyrics(lyric):
    if r"-" in lyric.text:
        pass
    else:
        await lyric.edit(LANG['WRONG_TYPE'])
        return

    if GENIUS:
        await lyric.edit("heroku'daki, genius var'nı silin.")
        return
    else:
        genius = lyricsgenius.Genius("7JWO79mydLFN2DatQv94mIyulpYH_1Mnw4jZ7e8OViyJpmUs75gEpRwVCZ30EsEA")
        try:
            args = lyric.text.split('.lyrics')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except:
            await lyric.edit(LANG['GIVE_INFO'])
            return

    if len(args) < 1:
        await lyric.edit(LANG['GIVE_INFO'])
        return

    await lyric.edit(LANG['SEARCHING'].format(artist, song))

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lyric.edit(LANG['NOT_FOUND'].format(artist, song))
        return
    if len(songs.lyrics) > 4096:
        await lyric.edit(LANG['TOO_LONG'])
        with open("lyrics.txt", "w+") as f:
            f.write(f"{LANG['LYRICS']} \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
        )
        os.remove("lyrics.txt")
    else:
        await lyric.edit(f"{LANG['LYRICS']} \n`{artist} - {song}`\n\n```{songs.lyrics}```")
    return

@register(outgoing=True, pattern="^.singer(?: |$)(.*)")
async def singer(lyric):
    if r"-" in lyric.text:
        pass
    else:
        await lyric.edit(LANG['WRONG_TYPE'])
        return

    if GENIUS is None:
        await lyric.edit(
            LANG['GENIUS_NOT_FOUND'])
        return
    else:
        genius = lyricsgenius.Genius("FdiG8NMlpEVOW3fJnaJqW7Vom-8p9lUauP_jNuA5PLbX3L-kDznZlIghV2Opiooz")
        try:
            args = lyric.text.split('.singer')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except:
            await lyric.edit(LANG['GIVE_INFO'])
            return

    if len(args) < 1:
        await lyric.edit(LANG['GIVE_INFO'])
        return

    await lyric.edit(LANG['SEARCHING'].format(artist, song))

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lyric.edit(LANG['NOT_FOUND'].format(artist, song))
        return
    await lyric.edit(LANG['SINGER_LYRICS'].format(artist, song))
    await asyncio.sleep(1)

    split = songs.lyrics.splitlines()
    i = 0
    while i < len(split):
        try:
            if split[i] != None:
                await lyric.edit(split[i])
                await asyncio.sleep(2)
            i += 1
        except:
            i += 1
    await lyric.edit(LANG['SINGER_ENDED'])

    return

            
CmdHelp('lyrics').add_command(
    'lyrics', (LANG['LY1']), (LANG['LY2']), (LANG['LY3'])
).add_command(
    'singer', (LANG['SG1']), (LANG['SG2']), (LANG['SG3'])
).add()