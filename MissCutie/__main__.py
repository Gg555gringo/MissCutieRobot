import time, re, psutil
from platform import python_version

from sys import argv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import escape_markdown, mention_html
from MissCutie.Handlers.validation import is_user_admin

from telegram.error import (
    BadRequest,
    Unauthorized,
)

from MissCutie import (
    OWNER_ID,
    OWNER_USERNAME,
    dispatcher, 
    StartTime,
    LOGGER,
    SUPPORT_CHAT,
    WEBHOOK,
    CERT_PATH,
    PORT,
    URL,
    TOKEN,
    PHOTO,
    telethn,
    updater)

from MissCutie.Plugins import ALL_MODULES
from MissCutie.__help__ import (
get_help, 
help_button, 
get_settings, 
settings_button, 
migrate_chats, 
send_help, 
send_admin_help,
send_user_help,
user_help_button,
send_settings,
admin_help_button,
tools_help_button,
send_tools_help,
HELP_STRINGS,
IMPORTED,
IMPORTED,
HELPABLE,
ADMIN,
USER,
TOOLS )


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f"{time_list.pop()}, "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """ Hello *{}*, My name is *{}*! 
A telegram group management bot. I'm here to help you to manage your groups.
I have lots of handy features such as:
‣ Warning system
‣ Artificial intelligence
‣ Flood control system
‣ Note keeping system
‣ Filters keeping system
‣ Approvals and much more.

So what are you waiting for?
*Add me in your groups and give me full rights to make me function well.*
"""




def start(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    first_name = update.effective_user.first_name
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="help_back")]]
                    ),
                )
                send_admin_help(
                    update.effective_chat.id,
                    ADMIN[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="admin_back")]]
                    ),
                )
                send_user_help(
                    update.effective_chat.id,
                    USER[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="user_back")]]
                    ),
                )
                send_tools_help(
                    update.effective_chat.id,
                    USER[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="⬅️ BACK", callback_data="tools_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match[1])

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match[1], update.effective_user.id, False)
                else:
                    send_settings(match[1], update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
                        update.effective_message.reply_text(
                            PM_START_TEXT.format(
                                    escape_markdown(first_name), escape_markdown(context.bot.first_name)),
                            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="➕️ Add me to your chat ➕️", url=f"https://t.me/{context.bot.username}?startgroup=true"),
                ],
                [
                    InlineKeyboardButton(text="Admin", callback_data="admin_back"),
                    InlineKeyboardButton(
                        text="Users", callback_data="user_back"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Tools", callback_data="tools_back"),
                    InlineKeyboardButton(
                        text="Bot Info", callback_data="MissCutie_"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Helps & Commands❔", callback_data="help_back"),
                ],
            ]),
                            parse_mode=ParseMode.MARKDOWN,
                            timeout=60,
                        )
    else:
        text = (
            f"Hello {mention_html(user.id, user.first_name)}, I'm {bot.first_name}\n\n"
            f"┏━━━━━━━━━━━━━━\n"
            f"┣[• Owner : @{OWNER_USERNAME}  \n"
            f"┣[• Uptime : {uptime} \n"
            f"┣[• Core : {psutil.cpu_percent()}%\n"
            f"┣[• Python   : Ver {python_version()} \n"
            f"┗━━━━━━━━━━━━━━")


        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="SUPPORT", 
                    url=f"https://t.me/{SUPPORT_CHAT}"),
                InlineKeyboardButton(
                    text="🍷DEVELOPER", 
                    url=f"https://t.me/gringomdz")

            ],

            ])
        message.reply_photo(
                    PHOTO,
                    caption=(text),
                    reply_markup=keyboard,
                    parse_mode=ParseMode.HTML,

                )

                



def misscutie_about_callback(update: Update, context: CallbackContext):
    first_name = update.effective_user.first_name
    query = update.callback_query
    if query.data == "misscutie_":
        query.message.edit_text(
            text="""Hello *{}*, I'm *{}*.Um poderoso bot de gerenciamento de grupos de telegramas criado para ajudá-lo a gerenciar grupos facilmente. 
            \n ‣ Posso Restringir Usuários. 
            \n ‣ Posso cumprimentar os usuários com uma mensagem de boas-vindas personalizável e até definir regras de grupo 
            \n ‣ Eu tenho um sistema anti-flood avançado que ajudará você a proteger o grupo do Spammmer .
            \n ‣ Posso avisar os usuários até atingirem o máximo de alertas, com cada ação predefinida, como banir, silenciar e chutar, etc. 
            \n ‣ Eu tenho um sistema de anotações, listas negras e até respostas predeterminadas para determinadas palavras-chave. 
            \n ‣ Eu verifico as permissões de administrador antes de executar qualquer comando e mais coisas. 
            \n ‣ Eu tenho um sistema de chatbot artificial avançado, então posso falar com usuários como humanos.
            \n\n*Se você tiver alguma dúvida, pode entrar no bate-papo de suporte. Minha equipe de desenvolvedores responderá. Confira o link abaixo*""".format(
                        escape_markdown(first_name), escape_markdown(context.bot.first_name)),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                   [
                     InlineKeyboardButton(text="Suporte", url="t.me/gringomdz"),
                     InlineKeyboardButton(text="Novidades", url="t.me/mdzup"),
                   ],
                   [
                    InlineKeyboardButton(text="Voltar", callback_data="misscutie_back")
                   ]
                ]
            ),
        )
    elif query.data == "misscutie_back":
        query.message.edit_text(
                PM_START_TEXT.format(
                        escape_markdown(first_name), escape_markdown(context.bot.first_name)),
                reply_markup=InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="➕️ Adicione-me ao seu chat  ➕️", url=f"https://t.me/{context.bot.username}?startgroup=true"),
    ],
    [
        InlineKeyboardButton(text="Admin", callback_data="admin_back"),
        InlineKeyboardButton(
            text="Users", callback_data="user_back"
        ),
    ],
    [
        InlineKeyboardButton(text="Tools", callback_data="tools_back"),
        InlineKeyboardButton(
            text="Bot Info", callback_data="misscutie_"
        ),
    ],
    [
        InlineKeyboardButton(text="Help & Commands❔", callback_data="help_back"),
    ],
]),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            stringz = "Meu caro proprietário, estou trabalhando novamente. Obrigado por me fazer viver."
            dispatcher.bot.sendMessage(f"@{OWNER_ID}", stringz)
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler("start", start, pass_args=True, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*", run_async=True)
    admin_help_callback_handler = CallbackQueryHandler(admin_help_button, pattern=r"admin_.*", run_async=True)
    user_help_callback_handler = CallbackQueryHandler(user_help_button, pattern=r"user_.*", run_async=True)
    tools_help_callback_handler = CallbackQueryHandler(tools_help_button, pattern=r"tools_.*", run_async=True)

    about_callback_handler = CallbackQueryHandler(misscutie_about_callback, pattern=r"misscutie_", run_async=True)

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_", run_async=True)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats, run_async=True)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(admin_help_callback_handler)
    dispatcher.add_handler(user_help_callback_handler)
    dispatcher.add_handler(tools_help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(allowed_updates=Update.ALL_TYPES, timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) in {1, 3, 4}:
        telethn.run_until_disconnected()

    else:
        telethn.disconnect()
    updater.idle()



if __name__ == "__main__":
    LOGGER.info(f"Successfully loaded modules: {str(ALL_MODULES)}")
    telethn.start(bot_token=TOKEN)
    main()
