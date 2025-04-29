


if not BOT_TOKEN == None:
    tgbot = TelegramClient(
        "TG_BOT_TOKEN",
        api_id=API_KEY,
        api_hash=API_HASH
    ).start(bot_token=BOT_TOKEN)
else:
    tgbot = None
heroku_conn = heroku3.from_key(HEROKU_APIKEY)
app = heroku_conn.apps()[HEROKU_APPNAME]
def butonlastir(sayfa, moduller):
    Satir = 5
    Kolon = 3
    
    moduller = sorted([modul for modul in moduller if not modul.startswith("_")])
    pairs = list(map(list, zip(moduller[::2], moduller[1::2])))
    if len(moduller) % 2 == 1:
        pairs.append([moduller[-1]])
    max_pages = ceil(len(pairs) / Satir)
    pairs = [pairs[i:i + Satir] for i in range(0, len(pairs), Satir)]
    butonlar = []
    for pairs in pairs[sayfa]:
        butonlar.append([
            custom.Button.inline("🔸 " + pair, data=f"bilgi[{sayfa}]({pair})") for pair in pairs
        ])

    butonlar.append([custom.Button.inline("◀️ Geri", data=f"sayfa({(max_pages - 1) if sayfa == 0 else (sayfa - 1)})"), custom.Button.inline("İrəli ▶️", data=f"sayfa({0 if sayfa == (max_pages - 1) else sayfa + 1})")])
    butonlar.append([custom.Button.inline("📂Menyu", data="evvel")])
    return [max_pages, butonlar]


with bot:
    if AVTO_Q:
        try:
            bot(JoinChannelRequest("@silgiub"))
            bot(JoinChannelRequest("@silgiuserbots"))
            bot(JoinChannelRequest("@silgiuserbotchat"))
            bot(JoinChannelRequest("@silgiubplugin"))
            
            
        except:
            pass

    moduller = CMD_HELP
    me = bot.get_me()
    uid = me.id
    SILGI_USER = f"[{me.first_name}](tg://user?id={me.id})"

    try:
        @tgbot.on(NewMessage(pattern='/start'))
        async def start_bot_handler(event):
            if not event.message.from_id == uid:
                await event.reply(f'`Salam mən `⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ `! Mən sahibimə (`@{me.username}`) kömək olmaq üçün varam, yəni sənə köməkçi ola bilmərəm :/ Ama sən da bir ⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ quraşdıra bilərsən; Qrupa bax` @silgiub')
            else:
                await event.reply(f'`⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝`')

        @tgbot.on(InlineQuery)  
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query == "kömek":
                rev_text = query[::-1]
                veriler = (butonlastir(0, sorted(CMD_HELP)))
                result = await builder.article(
                    f"Xaiş sadəcə .kömek əmri ilə işladin",
                    text=f"**⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝** [SilgiUb](https://t.me/silgiub) __💻__\n\n**Yüklənən Modul Sayı:** `{len(CMD_HELP)}`\n**Səhifə:** 1/{veriler[0]}",
                    buttons=veriler[1],
                    link_preview=False
                )
            elif event.query.user_id == uid and query == "@SilgiUB":
                text = "**⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝** [SilgiUb](https://t.me/silgiub) __işləyir__\n\n"
                text += f"👤 **Sahibim** {SILGI_USER}\n __Qulluğunda hazıram__"
                result = builder.document(
                     file=botgif,
                     title="⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝",
                     text=text,
                     buttons=[
                         [custom.Button.inline("📲Plugin Listi", data="komek")],
                         [custom.Button.inline("🛠️Bot Configləri", data="config")]
                     ],
                     link_preview=False
                 )
            elif query.startswith("http"):
                parca = query.split(" ")
                result = builder.article(
                    "Fayl Yükləndi",
                    text=f"**Fayl uğurlu bir şəkildə {parca[2]} saytına yükləndi!**\n\nYükləmə zamanı: {parca[1][:3]} saniyə\n[‏‏‎ ‎]({parca[0]})",
                    buttons=[
                        [custom.Button.url('URL', parca[0])]
                    ],
                    link_preview=True
                )
            else:
                result = builder.article(
                    "⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝",
                    text="""[⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝](https://t.me/silgiub)'u işlətməyi yoxlayın!
Hesabınızı bot'a çevirə bilərsiz və bunları işlədə bilərsiz. Unutmayın, siz başqasının botunu idarə edə bilmərsiz! Altdakı GitHub adresindən bütün qurulum haqda məlumat var.""",
                    buttons=[
                        [custom.Button.url("Dəstək qrupuna Qatıl", "https://t.me/silgiub"), custom.Button.url(
                            "Sahibim", "https://t.me/hvseyn")],
                        [custom.Button.url(
                            "GitHub", "https://github.com/Silgimusicbot/SilgiUserbot")],
                        [custom.Button.url(
                            "Qurulum botu", "https://t.me/silgiqur_bot")]
                    ],
                    link_preview=False
                )
            await event.answer([result] if result else None)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"sayfa\((.+?)\)")))
        async def sayfa(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Məni əlləmə! Özünə bir @silgiub qur.", cache_time=0, alert=True)
            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            veriler = butonlastir(sayfa, CMD_HELP)
            await event.edit(
                f"**⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝** [SilgiUb](https://t.me/silgiub) __işləyir__\n\n**Yüklənən Modul Sayı:** `{len(CMD_HELP)}`\n**Səhifə:** {sayfa + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False
            )
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"komek")))
        async def inline_handler(event):
            if not event.query.user_id == uid:
                return await event.answer("❌ Hey! Məni əlləmə! Özünə bir @silgiub qur.", cache_time=0, alert=True)   
            query = event.data.decode("UTF-8")
            veriler = butonlastir(0, sorted(CMD_HELP))
            buttons = veriler[1]  
            await event.answer("📱Plugin listi açıldı", cache_time=1)
            await event.edit(
                text=f"**⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝** [SilgiUb](https://t.me/silgiub) __💻__\n\n**Yüklənən Modul Sayı:** `{len(CMD_HELP)}`\n**Səhifə:** 1/{veriler[0]}",
                buttons=buttons,  
                link_preview=False
            )
        @tgbot.on(events.CallbackQuery(data=re.compile(b"evvel")))
        async def main_menu(event):
            if not event.query.user_id == uid:
                return await event.answer("❌ Hey! Məni əlləmə! Özünə bir @silgiub qur.", cache_time=0, alert=True)
            text="**⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝** [SilgiUb](https://t.me/silgiub) __işləyir__"
            text += f"👤 **Sahibim** {SILGI_USER}\n __Qulluğunda hazıram__"
            buttons = [
                [Button.inline("📲Plugin Listi", data="komek")],
                [Button.inline("🛠️Bot Configləri", data="config")]
            ]

            await event.answer("📌 Əsas menyuya qayıdıldı", cache_time=0)
            await event.edit(text, buttons=buttons, link_preview=False)
        @tgbot.on(events.CallbackQuery(data=re.compile(b"config")))
        async def config_handler(event):
            if event.query.user_id != uid:
                return await event.answer("❌ Hey! Məni əlləmə! Özünə bir @silgiub qur.", cache_time=0, alert=True) 
    
            needed_keys = ["BOT_USERNAME", "BOT_TOKEN", "BOTLOG_CHATID", "API_HASH", "PM_AUTO_BAN", "TZ", "LANGUAGE", "COUNTRY", "PM_AUTO_BAN_LIMIT", "START_TIME", "WARN_LIMIT", "WARN_MODE"]  
            config_vars = app.config().to_dict()
            config_keys = [key for key in needed_keys if key in config_vars and config_vars[key]]  

            if not config_keys:
                return await event.answer("❌ Heç bir uyğun config tapılmadı!", cache_time=0, alert=True)
            text = "**🔧 Heroku Config Vars**\n\n"
            buttons = []
            for index, key in enumerate(config_keys, start=1):
                text += f"**{index}.** `{key}`\n"
                buttons.append(Button.inline(f"🔢 {index}", data=f"config_edit:{key}"))
            buttons.append(Button.inline("📂Menyu", data="evvel"))
            if buttons:
                buttons = list(itertools.zip_longest(*[iter(buttons)] * 3))
                buttons = [list(filter(None, row)) for row in buttons]
            await event.answer("Config listi açıldı🛠️", cache_time=1)
            await event.edit(text, buttons=buttons, link_preview=False)

        @tgbot.on(events.CallbackQuery(data=re.compile(b"config_edit:(.+)")))
        async def config_edit(event):
            if not event.query.user_id == uid: 
                        return await event.answer("❌ Hey! Məni əlləmə! Özünə bir @silgiub qur.", cache_time=0, alert=True)
            key = event.data_match.group(1).decode("UTF-8")
            user_id = event.query.user_id
            config_vars = app.config().to_dict()
            current_value = config_vars.get(key)
            text = f"🔧 **{key}** dəyişdirilməsi\n\n"
            text += f"🔹 Mövcud dəyər: `{current_value}`\n\n"
            text += f"✏️ Dəyəri dəyişmək üçün:\n`.set var {key} yeni_dəyər`"
            await event.answer(f"Config {key} açıldı", cache_time=1)
            await event.edit(text, buttons=[[Button.inline("🔙 Geri", data="config_back")]])
        @tgbot.on(events.CallbackQuery(data=re.compile(b"config_back")))
        async def config_back(event):
            await event.answer("🔙 Geri qayıdıldı", cache_time=1)
            await config_handler(event)
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"bilgi\[(\d*)\]\((.*)\)")))
        async def bilgi(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌  Hey! Məni əlləmə! Özünə bir @silgiub qur.", cache_time=0, alert=True)

            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            komut = event.data_match.group(2).decode("UTF-8")
            try:
                butonlar = [custom.Button.inline("🔹 " + cmd[0], data=f"komut[{komut}[{sayfa}]]({cmd[0]})") for cmd in CMD_HELP_BOT[komut]['commands'].items()]
            except KeyError:
                return await event.answer("❌ Bu modula açıqlama yazılmayıb.", cache_time=0, alert=True)

            butonlar = [butonlar[i:i + 2] for i in range(0, len(butonlar), 2)]
            butonlar.append([custom.Button.inline("◀️ Geri", data=f"sayfa({sayfa})")])
            await event.edit(
                f"**📗 Fayl:** `{komut}`\n**🔢 Əmr sayı:** `{len(CMD_HELP_BOT[komut]['commands'])}`",
                buttons=butonlar,
                link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"komut\[(.*)\[(\d*)\]\]\((.*)\)")))
        async def komut(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Məni əlləmə! Özünə bir @silgiub qur.", cache_time=0, alert=True)

            cmd = event.data_match.group(1).decode("UTF-8")
            sayfa = int(event.data_match.group(2).decode("UTF-8"))
            komut = event.data_match.group(3).decode("UTF-8")

            result = f"**📗 Fayl:** `{cmd}`\n"
            if 'sahib' in CMD_HELP_BOT[cmd]['info'] and CMD_HELP_BOT[cmd]['info']['sahib']:
                result += f"**👤 Sahib:** {CMD_HELP_BOT[cmd]['info']['sahib']}\n"
            if CMD_HELP_BOT[cmd]['info']['info'] == '':
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                    result += f"**⚠️ Xəbərdarlıq:** {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
                else:
                    result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n\n"
            else:
                result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⚠️ Xəbərdarlıq:** {CMD_HELP_BOT[cmd]['info']['warning']}\n"
                result += f"**ℹ️ Info:** {CMD_HELP_BOT[cmd]['info']['info']}\n\n"

            command = CMD_HELP_BOT[cmd]['commands'][komut]
            if command['params'] is None:
                result += f"**🛠 Əmr:** `{PATTERNS[:1]}{command['command']}`\n"
            else:
                result += f"**🛠 Əmr:** `{PATTERNS[:1]}{command['command']} {command['params']}`\n"
                
            if command['example'] is None:
                result += f"**💬 Açıqlama:** `{command['usage']}`\n\n"
            else:
                result += f"**💬 Açıqlama:** `{command['usage']}`\n"
                result += f"**⌨️ Məsələn:** `{PATTERNS[:1]}{command['example']}`\n\n"

            await event.edit(
                result,
                buttons=[custom.Button.inline("◀️ Geri", data=f"bilgi[{sayfa}]({cmd})")],
                link_preview=False
            )
    except Exception as e:
        print(e)
        LOGS.info(
            "Botunuzda inline dəstəyi deaktiv edildi. "
            "Aktivləşdirmək üçün bir bot token tanımlayın və botunuzda inline modunu aktivləşdirin. "
            "Əgər bunun xaricində bir problem olduğunu düşünürsüzsə bizlə əlaqə saxlayın."
        )

