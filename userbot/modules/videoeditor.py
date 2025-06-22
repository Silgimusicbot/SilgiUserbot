from userbot.events import register
from userbot.cmdhelp import CmdHelp
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
import os

@register(outgoing=True, pattern=r"^.captionvideo (.+)")
async def captionvideo(event):
    reply = await event.get_reply_message()
    if not reply or not reply.media:
        return await event.edit("❌ Zəhmət olmasa, videoya cavab verərək `.captionvideo <yazı>` yazın.")

    video_path = await reply.download_media()
    if not reply.document and not reply.video:
        return await event.edit("❌ Cavab verilən fayl video olmalıdır!")

    text = event.pattern_match.group(1).strip()
    await event.edit("🎬 Video üzərinə yazı əlavə olunur...")

    try:
        videoclip = VideoFileClip(video_path)

        txt_clip = (TextClip(text, fontsize=40, color='white', font='Arial-Bold', stroke_color='black', stroke_width=2)
                    .set_position('center')
                    .set_duration(videoclip.duration))

        bg = (ColorClip(size=(videoclip.w, 80), color=(0, 0, 0))
              .set_opacity(0.15)
              .set_position('center')
              .set_duration(videoclip.duration))

        final = CompositeVideoClip([videoclip, bg, txt_clip])

        output_path = "captioned_" + os.path.basename(video_path)
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')

        await event.client.send_file(event.chat_id, output_path, reply_to=reply.id)
        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta baş verdi: {str(e)}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(output_path):
            os.remove(output_path)


@register(outgoing=True, pattern=r"^.cutvideo (\d+) (\d+)")
async def cutvideo(event):
    reply = await event.get_reply_message()
    if not reply or not reply.media:
        return await event.edit("❌ Zəhmət olmasa, videoya cavab verərək `.cutvideo <başlanğıc saniyə> <son saniyə>` yazın.\nMisal: `.cutvideo 5 15`")

    start_time = int(event.pattern_match.group(1))
    end_time = int(event.pattern_match.group(2))

    video_path = await reply.download_media()
    if not reply.document and not reply.video:
        return await event.edit("❌ Cavab verilən fayl video olmalıdır!")
    await event.edit("✂️ Video kəsilir...")

    try:
        videoclip = VideoFileClip(video_path)

        if start_time < 0 or end_time > videoclip.duration or start_time >= end_time:
            return await event.edit(f"❌ Zəhmət olmasa, düzgün zaman aralığı seçin. Video uzunluğu: {videoclip.duration:.2f} saniyə.")

        videoclip = videoclip.subclip(start_time, end_time)

        output_path = "cut_" + os.path.basename(video_path)
        videoclip.write_videofile(output_path, codec='libx264', audio_codec='aac')

        await event.client.send_file(event.chat_id, output_path, reply_to=reply.id)
        await event.delete()
    except Exception as e:
        await event.edit(f"❌ Xəta baş verdi: {str(e)}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(output_path):
            os.remove(output_path)


CmdHelp('videoedit').add_command(
    'captionvideo', '<yazı>', 'Cavab verdiyiniz videoya ortada, şəffaf fonlu yazı əlavə edir.'
).add_command(
    'cutvideo', '<başlanğıc saniyə> <son saniyə>', 'Cavab verdiyiniz videonu göstərilən aralıqda kəsir.'
).add_sahib(
    '[SILGI](t.me/silgiteam) tərəfindən hazırlanmışdır.'
).add()