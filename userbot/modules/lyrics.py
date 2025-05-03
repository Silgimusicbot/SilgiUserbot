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




# Genius
def scrape_lyrics(artist, title):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    search_query = f"{artist} {title}"
    search_url = "https://genius.com/search?q=" + requests.utils.quote(search_query)
    
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    first_result = soup.select_one("a[href^='/lyrics/'], a[href^='https://genius.com/']")
    if not first_result:
        return None

    song_url = first_result["href"]
    song_page = requests.get(song_url, headers=headers)
    if song_page.status_code != 200:
        return None

    soup = BeautifulSoup(song_page.text, "html.parser")
    lyrics_blocks = soup.find_all("div", attrs={"data-lyrics-container": "true"})
    lyrics = "\n".join(block.get_text(separator="\n") for block in lyrics_blocks).strip()

    return lyrics if lyrics else None

@register(outgoing=True, pattern=r"^.lyrics(?: |$)(.*)")
async def lyrics_handler(event):
    query = event.pattern_match.group(1).strip()

    if '-' not in query:
        await event.edit(LANG['WRONG_TYPE'])
        return

    artist, title = [x.strip() for x in query.split('-', 1)]
    await event.edit(LANG['SEARCHING'].format(artist, title), parse_mode='html')

    try:
        loop = asyncio.get_event_loop()
        lyrics = await loop.run_in_executor(None, scrape_lyrics, artist, title)

        if not lyrics:
            await event.reply(LANG['NOT_FOUND'].format(artist, title))
            return

        if len(lyrics) > 4096:
            await event.edit(LANG['TOO_LONG'])
            filename = "lyrics.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝\n{artist} - {title}\n\n{lyrics}")
            await event.client.send_file(event.chat_id, filename, reply_to=event.id)
            os.remove(filename)
        else:
            await event.edit(f"⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝\n**{artist} - {title}**\n\n```{lyrics}```", parse_mode="Markdown")

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