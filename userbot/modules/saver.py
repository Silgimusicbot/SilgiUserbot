# ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ Əkmə OĞLUMMM
from userbot.events import register
from userbot.cmdhelp import CmdHelp
import requests
import re
import os
import asyncio

# Fayl yüklənərkən progress göstərmək üçün funksiyamız
async def progress_bar(current, total, event, start, type="Yüklənir"):
    now = time.time()
    diff = now - start

    if diff % 2 == 0 or current == total:
        percent = int(current * 100 / total)
        bar = "█" * (percent // 10) + "░" * (10 - (percent // 10))
        status = f"{type}: [{bar}] {percent}%"
        try:
            await event.edit(status)
        except:
            pass

@register(outgoing=True, pattern=r"^.tiktok(?: |$)(.*)")
async def tiktok_download(event):
    import time
    url = event.pattern_match.group(1)
    if not url:
        await event.edit("Zəhmət olmasa TikTok linkini daxil et: `.tiktok <link>`")
        return

    msg = await event.edit("Videonu yükləyirəm...")
    try:
        headers = {"user-agent": "Mozilla/5.0"}
        session = requests.Session()

        r1 = session.get("https://ssstik.io/en", headers=headers)
        token = re.search(r'id="token" value="(.*?)"', r1.text).group(1)

        response = session.post("https://ssstik.io/abc", data={
            "id": url,
            "locale": "en",
            "tt": token
        }, headers=headers)

        video_url = re.search(r'href="(https:\/\/[^"]+)"', response.text)
        if not video_url:
            await msg.edit("Videonu yükləmək alınmadı.")
            return

        video_link = video_url.group(1)

        file_name = "tiktok.mp4"
        video_data = session.get(video_link, stream=True)

        total_length = int(video_data.headers.get('content-length', 0))
        downloaded = 0
        start_time = time.time()

        with open(file_name, "wb") as f:
            for chunk in video_data.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    await progress_bar(downloaded, total_length, msg, start_time)

        await msg.edit("Telegram-a göndərilir...")
        await event.client.send_file(
            event.chat_id,
            file_name,
            caption="Budur TikTok videosu!",
            progress_callback=lambda d, t: asyncio.ensure_future(
                progress_bar(d, t, msg, start_time, type="Göndərilir")
            )
        )
        await msg.delete()
        os.remove(file_name)

    except Exception as e:
        await msg.edit(f"Xəta baş verdi: `{str(e)}`")

CmdHelp("tiktok").add_command(
    "tiktok", "<link>", "TikTok videosunu watermark olmadan yükləyir və çatda paylaşır. Yükləmə zamanı progress bar göstərilir."
).add()