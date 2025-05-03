import os
import lyricsgenius
import asyncio
import time
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
    # Genius'taki arama URL'si
    search_query = f"{artist} {title}"
    search_url = f"https://genius.com/search?q={search_query}"
    time.sleep(10)
    # Sayfa yüklenmesini beklemek için 2 saniye bekliyoruz
    response = requests.get(search_url)
    if response.status_code != 200:
        return None

    # BeautifulSoup ile HTML parsing
    soup = BeautifulSoup(response.text, "html.parser")

    # İlk şarkıyı bulmak için sonuçları alıyoruz
    first_result = soup.select_one("a[href^='/lyrics/']")
    if not first_result:
        return None

    # Şarkının tam URL'sini alıyoruz
    song_url = "https://genius.com" + first_result["href"]

    # Şarkı sayfasını çekiyoruz
    song_page = requests.get(song_url)
    if song_page.status_code != 200:
        return None

    # Şarkı sayfasından sözleri almak
    soup = BeautifulSoup(song_page.text, "html.parser")
    lyrics_blocks = soup.find_all("div", class_="lyrics")
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
            await event.edit(LANG['NOT_FOUND'].format(artist, title))
            return

        header = f"⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝\n**{artist} - {title}**\n\n"

        if len(lyrics) > 4096:
            await event.edit(LANG['TOO_LONG'])
            filename = "lyrics.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"{header}{lyrics}")
            await event.client.send_file(event.chat_id, filename, reply_to=event.id)
            os.remove(filename)
        else:
            await event.edit(header + f"```{lyrics}```", parse_mode="Markdown")

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