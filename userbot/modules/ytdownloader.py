# SilgiUserbot pluginidir kodu əkən oğurlayan deyişiklik eden bir başa peyserdir ve bu şexse ata desin t.me/SilgiTEAM
import os
import re
import asyncio
import aiohttp
import yt_dlp
from userbot.events import register as silgi
from userbot.cmdhelp import CmdHelp
from telethon.tl.types import DocumentAttributeAudio

sirniyat = "https://batbin.me/raw/buses"

def nebilim(metin):
    return re.sub(r'[\\/*?:"<>|]', "", (metin or "")).strip()
def denoyol():
    yoxlama = [
        "/root/.deno/bin/deno",
        "/app/.deno/bin/deno",
        "/usr/bin/deno",
        "/usr/local/bin/deno",
    ]
    for yol in yoxlama:
        if os.path.exists(yol):
            return yol
    return None
def hmmm(melumat):
    if not isinstance(melumat, dict):
        return "Unknown", "Mahnı"
    if melumat.get("track") and melumat.get("artist"):
        if str(melumat.get("artist")).strip() and str(melumat.get("track")).strip():
            return str(melumat.get("artist")).strip(), str(melumat.get("track")).strip()
    if melumat.get("title"):
        basliq = str(melumat.get("title")).strip()
        if " - " in basliq:
            ifa_eden, mahninin_adi = basliq.split(" - ", 1)
            return ifa_eden.strip() or "Unknown", mahninin_adi.strip() or "Mahnı"
        if " — " in basliq:
            ifa_eden, mahninin_adi = basliq.split(" — ", 1)
            return ifa_eden.strip() or "Unknown", mahninin_adi.strip() or "Mahnı"
    ifa_eden = str(melumat.get("artist") or melumat.get("uploader") or "Unknown").strip()
    mahninin_adi = str(melumat.get("track") or melumat.get("title") or "Mahnı").strip()
    return ifa_eden or "Unknown", mahninin_adi or "Mahnı"
async def sirniyat_ye():
    sirniyatresepti = "cookies.txt"
    try:
        async with aiohttp.ClientSession() as sessiya:
            async with sessiya.get(sirniyat) as cavab:
                if cavab.status != 200:
                    return None, f"❌ `cookies.txt` yüklənə bilmədi. Status: {cavab.status}"
                metin = await cavab.text()
        if "# Netscape HTTP Cookie File" not in metin:
            return None, "❌ `cookies.txt` Netscape formatında deyil."
        with open(sirniyatresepti, "w", encoding="utf-8") as fayl:
            fayl.write(metin)
        return sirniyatresepti, None
    except Exception as xeta:
        return None, f"⚠️ cookies yükləmə xətası:\n`{xeta}`"
def fayllari_temizle(*yollar):
    for yol in yollar:
        try:
            if yol and os.path.exists(yol):
                os.remove(yol)
        except Exception:
            pass
def bashi(cicibombes, sirniyatresepti):
    deno_yolu = denoyol()
    cumolar = {"deno": {}}
    if deno_yolu:
        cumolar = {"deno": {"path": deno_yolu}}
    return {
        "format": "bestaudio/best",
        "noplaylist": True,
        "cookiefile": sirniyatresepti,
        "outtmpl": cicibombes,
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {
                "key": "FFmpegThumbnailsConvertor",
                "format": "jpg",
            },
            {
                "key": "EmbedThumbnail",
            },
        ],
        "postprocessor_args": ["-id3v2_version", "3"],
        "prefer_ffmpeg": True,
        "quiet": True,
        "no_warnings": False,
        "verbose": True,
        "js_runtimes": cumolar,
        "remote_components": ["ejs:npm"],
        "extractor_args": {
            "youtube": {
                "player_client": ["tv"]
            }
        },
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        },
    }
def daqaqandes(cicibombes, sirniyatresepti):
    deno_yolu = denoyol()
    cumolar = {"deno": {}}
    if deno_yolu:
        cumolar = {"deno": {"path": deno_yolu}}
    return {
        "format": "bv*+ba/b",
        "outtmpl": cicibombes,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": False,
        "verbose": True,
        "cookiefile": sirniyatresepti,
        "merge_output_format": "mp4",
        "js_runtimes": cumolar,
        "remote_components": ["ejs:npm"],
        "extractor_args": {
            "youtube": {
                "player_client": ["tv"]
            }
        },
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        },
    }

@silgi(outgoing=True, pattern=r"\.ytmp3(?: |$)(.*)")
async def mahnini_yukle(hadise):
    sorgu = hadise.pattern_match.group(1).strip()
    if not sorgu:
        await hadise.edit(
            "ℹ️ Zəhmət olmasa link və ya mahnı adı yaz:\n"
            "`.ytmp3 Mahnı adı` və ya `.ytmp3 https://youtu.be/...`"
        )
        return
    await hadise.edit("```🔍 Mahnı axtarılır...```")
    sirniyatresepti, xeta = await sirniyat_ye()
    if xeta:
        await hadise.edit(xeta)
        return
    axtaris = sorgu if sorgu.startswith("http") else f"ytsearch1:{sorgu}"
    xaladelnik = "downloads"
    os.makedirs(xaladelnik, exist_ok=True)
    mp3_yolu = None
    sekil_yolu = None
    try:
        secenekler = bashi(
            os.path.join(xaladelnik, "%(title).80s.%(ext)s"),
            sirniyatresepti
        )
        with yt_dlp.YoutubeDL(secenekler) as yukleyici:
            melumat = await asyncio.to_thread(yukleyici.extract_info, axtaris, True)
            if "entries" in melumat:
                melumat = melumat["entries"][0]
            ifa_eden, mahninin_adi = hmmm(melumat)
            tam_basliq = nebilim(f"{ifa_eden} - {mahninin_adi}")
            await hadise.edit(f"```🔍 Mahnı axtarılır...\n📥 {tam_basliq} yüklənir...```")
            hazir_fayl = yukleyici.prepare_filename(melumat)
            esas_yol = os.path.splitext(hazir_fayl)[0]
            mp3_yolu = esas_yol + ".mp3"
            sekiller = [
                esas_yol + ".jpg",
                esas_yol + ".jpeg",
                esas_yol + ".png",
                esas_yol + ".webp",
            ]
            for sekil in sekiller:
                if os.path.exists(sekil):
                    sekil_yolu = sekil
                    break
            if not os.path.exists(mp3_yolu):
                await hadise.edit("❌ `MP3 faylı tapılmadı.`")
                return
        await hadise.edit(f"```🔍 Mahnı axtarılır...\n📥 {tam_basliq} yüklənir...\n📤 Göndərilir...```")
        await hadise.client.send_file(
            hadise.chat_id,
            mp3_yolu,
            thumb=sekil_yolu if sekil_yolu and os.path.exists(sekil_yolu) else None,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(melumat.get("duration") or 0),
                    voice=False,
                    title=mahninin_adi,
                    performer=ifa_eden
                )
            ],
            caption=f"🎶 `{ifa_eden} - {mahninin_adi}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```",
            supports_streaming=True,
            force_document=False,
            link_preview=False
        )
        await hadise.delete()
    except Exception as xeta:
        await hadise.edit(f"❌ Yükləmə xətası:\n`{xeta}`")
    finally:
        fayllari_temizle(sirniyatresepti, mp3_yolu, sekil_yolu)

@silgi(outgoing=True, pattern=r"\.ytvideo(?: |$)(.*)")
async def videonu_yukle(hadise):
    sorgu = hadise.pattern_match.group(1).strip()
    if not sorgu:
        await hadise.edit(
            "ℹ️ Zəhmət olmasa link və ya video adı yaz:\n"
            "`.ytvideo Video adı` və ya `.ytvideo https://youtu.be/...`"
        )
        return
    await hadise.edit("```🎬 Video axtarılır...```")
    sirniyatresepti, xeta = await sirniyat_ye()
    if xeta:
        await hadise.edit(xeta)
        return
    axtaris = sorgu if sorgu.startswith("http") else f"ytsearch1:{sorgu}"
    xaladelnik = "downloads"
    os.makedirs(xaladelnik, exist_ok=True)
    video_yolu = None
    try:
        secenekler = daqaqandes(
            os.path.join(xaladelnik, "%(title).80s.%(ext)s"),
            sirniyatresepti
        )
        with yt_dlp.YoutubeDL(secenekler) as yukleyici:
            melumat = await asyncio.to_thread(yukleyici.extract_info, axtaris, True)
            if "entries" in melumat:
                melumat = melumat["entries"][0]
            xam_basliq = melumat.get("title", "Video")
            video_adi = nebilim(xam_basliq)
            await hadise.edit(f"```🎬 Video axtarılır...\n📥 {video_adi} yüklənir...```")
            video_yolu = yukleyici.prepare_filename(melumat)
            if not os.path.exists(video_yolu):
                esas_yol = os.path.splitext(video_yolu)[0]
                for sonluq in ("mp4", "mkv", "webm"):
                    ehtiyat_yol = f"{esas_yol}.{sonluq}"
                    if os.path.exists(ehtiyat_yol):
                        video_yolu = ehtiyat_yol
                        break
        if not video_yolu or not os.path.exists(video_yolu):
            await hadise.edit("❌ `Video faylı tapılmadı.`")
            return
        await hadise.edit(f"```🎬 Video axtarılır...\n📥 {video_adi} yüklənir...\n📤 Göndərilir...```")
        await hadise.client.send_file(
            hadise.chat_id,
            video_yolu,
            caption=f"🎥 `{video_adi}`\n```⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝```",
            supports_streaming=True,
            link_preview=False
        )
        await hadise.delete()
    except Exception as xeta:
        await hadise.edit(f"❌ Yükləmə xətası:\n`{xeta}`")
    finally:
        fayllari_temizle(sirniyatresepti, video_yolu)
CmdHelp("youtube").add_command(
    "ytmp3", "mahnı adı vəya link", "Youtube-dən mahnı yükləyir."
).add_command(
    "ytvideo", "video adı vəya link", "Youtube-dən video yükləyir."
).add_sahib(
    "[SILGI](https://t.me/silgiteam)"
).add()
