import time
from userbot.events import register
from userbot import START_TIME
from userbot import SILGI_USER
@register(outgoing=True, pattern="^.uptime$")
async def isleme_muddeti(silgi):
    indi = time.time()
    kecen_saniye = int(indi - START_TIME)
    gun = kecen_saniye // 86400
    saat = (kecen_saniye % 86400) // 3600
    deqiqe = (kecen_saniye % 3600) // 60
    saniye = kecen_saniye % 60
    vaxt = ""
    if gun > 0:
        vaxt += f"{gun} gün, "
    if saat > 0 or gun > 0:
        vaxt += f"{saat} saat, "
    if deqiqe > 0 or saat > 0 or gun > 0:
        vaxt += f"{deqiqe} dəqiqə, "
    vaxt += f"{saniye} saniyə"
    await silgi.edit(f"**Sahibim: {SILGI_USER}\nSilgiUserbot'un işləmə müddəti:**\n `{vaxt}`")