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

GENIUS_TOKEN = "BURAYA_SƏNİN_TOKEN"
genius = lyricsgenius.Genius(GENIUS_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])

@register(outgoing=True, pattern=r"^.genius(?: |$)(.*)")
async def genius_lyrics(event):
    query = event.pattern_match.group(1)

    if '-' not in query:
        await event.reply(LANG['WRONG_TYPE'])
        return

    artist, title = [x.strip() for x in query.split('-', 1)]
    await event.reply(LANG['SEARCHING'].format(artist, title))

    try:
        song = genius.search_song(title, artist)
    except Exception:
        await event.reply(f"Xəta:\n{str(e)}")
        return

    if not song or not song.lyrics:
        await event.reply(LANG['NOT_FOUND'].format(artist, title))
        return

    lyrics = song.lyrics

    if len(lyrics) > 4096:
        await event.respond(LANG['TOO_LONG'])
        with open("lyrics.txt", "w", encoding="utf-8") as f:
            f.write(f"⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝\n{artist} - {title}\n\n{lyrics}")
        await event.client.send_file(
            event.chat_id,
            "lyrics.txt",
            reply_to=event.id,
        )
        os.remove("lyrics.txt")
    else:
        header = f"⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝\n{artist} - {title}\n\n"
        formatted_lyrics = "<code>" + lyrics + "</code>"
        await event.respond(header + formatted_lyrics, parse_mode='html')
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
).add_sahib(
    "[SILGI](t.me/silgiteam) tərəfindən hazırlanmışdır"
).add()