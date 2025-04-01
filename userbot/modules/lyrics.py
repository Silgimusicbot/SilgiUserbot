import os
import lyricsgenius

from userbot.events import register
from userbot import CMD_HELP, GENIUS
from userbot.cmdhelp import CmdHelp
from userbot.language import get_value

LANG = get_value("lyrics")
GENIUS_API_KEY = "7JWO79mydLFN2DatQv94mIyulpYH_1Mnw4jZ7e8OViyJpmUs75gEpRwVCZ30EsEA"


genius = lyricsgenius.Genius(GENIUS_API_KEY)

@register(outgoing=True, pattern=r"^\.lyrics (.+)")
async def lyrics(event):
    song_name = event.pattern_match.group(1)
    await event.edit("🔍 Mahnı axtarılır...")

    try:
        song = genius.search_song(song_name)
        if song:
            lyrics_text = f"🎵 **{song.title}** - {song.artist}\n\n{song.lyrics}"
            
            
            if len(lyrics_text) > 4000:
                file_path = f"{song.title}.txt"
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(lyrics_text)
                
                await event.edit("📄 Mahnı sözləri çox uzundur, fayl kimi göndərilir...")
                await event.client.send_file(event.chat_id, file_path, caption=f"📄 **{song.title} - {song.artist}** mahnısının sözləri:")
                os.remove(file_path)  
            else:
                await event.edit(lyrics_text)
        else:
            await event.edit("🚫 Mahnı tapılmadı!")
    except Exception as e:
        await event.edit(f"❌ Xəta baş verdi:\n`{str(e)}`")
@register(outgoing=True, pattern="^.genius(?: |$)(.*)")
async def lyrics(event):
    args = event.pattern_match.group(1)
    if not args or "-" not in args:
        await event.edit(LANG['WRONG_TYPE'])
        return

    if not GENIUS:
        genius = lyricsgenius.Genius("FdiG8NMlpEVOW3fJnaJqW7Vom-8p9lUauP_jNuA5PLbX3L-kDznZlIghV2Opiooz")
    else:
        genius = lyricsgenius.Genius(GENIUS)

    genius.verbose = True  

    try:
        artist, song = [x.strip() for x in args.split('-', 1)]
    except ValueError:
        await event.edit(LANG['GIVE_INFO'])
        return

    await event.edit(LANG['SEARCHING'].format(artist, song))

    try:
        song_data = genius.search_song(song, artist)
        
        
        if not song_data:
            song_data = genius.search_song(song)

    except Exception as e:
        await event.edit(f"⚠️ Xəta baş verdi: `{str(e)}`")
        return

    if not song_data or not hasattr(song_data, 'lyrics'):
        await event.edit(LANG['NOT_FOUND'].format(artist, song))
        return

    lyrics_text = song_data.lyrics
    if len(lyrics_text) > 4096:
        with open("lyrics.txt", "w") as file:
            file.write(f"{LANG['LYRICS']} \n{artist} - {song}\n\n{lyrics_text}")
        await event.client.send_file(event.chat_id, "lyrics.txt", reply_to=event.id)
        os.remove("lyrics.txt")
    else:
        await event.edit(f"[⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝](@silgiub)\n"
                         f"{LANG['LYRICS']} \n`{artist} - {song}`\n\n```{lyrics_text}```")

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
        genius = lyricsgenius.Genius(GENIUS)
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
