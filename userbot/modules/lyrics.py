import os
import lyricsgenius
import asyncio
import requests
from bs4 import BeautifulSoup
from userbot.events import register
from userbot import CMD_HELP, GENIUS
from userbot.cmdhelp import CmdHelp
import aiohttp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("lyrics")

# ████████████████████████████████ #


LANG = get_value("lyrics")

# Genius
GENIUS_API_TOKEN = "MzGtNRFOK_6rGyuBzhn5aN5hed_LlI6I9ykQbdQZeB8NLqepONtr-4HcBzj9P5V9"

genius = lyricsgenius.Genius(GENIUS_API_TOKEN, timeout=10)

@register(outgoing=True, pattern=r"^.lyrics(?: |$)(.*)")
async def lyrics_handler(event):
    query = event.pattern_match.group(1)

    if '-' not in query:
        await event.edit(LANG['WRONG_TYPE'])
        return

    artist, title = [x.strip() for x in query.split('-', 1)]
    await event.edit(LANG['SEARCHING'].format(artist, title), parse_mode='html')

    try:
        song = genius.search_song(title, artist)

        if not song or not song.lyrics:
            await event.reply(LANG['NOT_FOUND'].format(artist, title))
            return

        lyrics = song.lyrics
        for marker in [
            "You might also like",
            "Embed",
            "ContributorsTranslations",
            "Read more on Genius",
            "More on Genius",
        ]:
            if marker in lyrics:
                lyrics = lyrics.split(marker)[0].strip()

        if len(lyrics) > 4096:
            await event.edit(LANG['TOO_LONG'])
            with open("lyrics.txt", "w", encoding="utf-8") as f:
                f.write(f"⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝\n{artist} - {title}\n\n{lyrics}")
            await event.client.send_file(
                event.chat_id,
                "lyrics.txt",
                reply_to=event.id,
            )
            os.remove("lyrics.txt")
        else:
            basliq = f"⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝\n**{artist} - {title}**\n\n"
            mahni = f"```{lyrics}```"
            await event.edit(basliq + mahni, parse_mode="Markdown")

    except Exception as e:
        await event.reply(f"Xəta baş verdi:\n<code>{str(e)}</code>", parse_mode="html")
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