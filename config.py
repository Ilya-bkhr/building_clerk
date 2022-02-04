from emoji import emojize

#EMOJI
EMOJI = {'out': emojize(':outbox_tray:', use_aliases=True),
         'entry': emojize(':inbox_tray:', use_aliases=True),
         'builder': emojize(':man_construction_worker:', use_aliases=True),
         'report': emojize(':page_facing_up:', use_aliases=True),
         'calendar': emojize(':calendar:', use_aliases=True),
         'card': emojize(':credit_card:', use_aliases=True),
         'money': emojize(':money_bag:', use_aliases=True),
         'pencil': emojize(':pencil:', use_aliases=True),
         'receipt': emojize(':receipt:', use_aliases=True),
         'pen': emojize(':pen:', use_aliases=True),
         'abacus': emojize(':abacus:', use_aliases=True),
         'aprove': emojize(':check_mark_button:', use_aliases=True),
         'no': emojize(':cross_mark:', use_aliases=True),
         'controller': emojize(':control_knobs:', use_aliases=True),
         'micro': emojize(':microphone:', use_aliases=True)}

#TEXT
WELCOME_TEXT = [f"Привет пользователь, я <b>Билдер</b> - клерк по стройке {EMOJI['builder']}",
                "Я помогу контролировать расходы во время стройки",
                f"Нажимай /info что бы узнать про мои способности"]

INFO_TEXT = ["У меня есть несколько команд, основные из них ты можешь увидеть на клавиатуре.",
            f"Если клавиатура не высветилась, то нажми на кнопку {EMOJI['controller']}, около микрофона {EMOJI['micro']}\n",
            f"<b>Сформировать отчет</b>{EMOJI['report']} - предоставит отчет за выбраный период, по датам и всеми расходам и пополнениям",
            f"<b>Расходы</b>{EMOJI['out']} - отправит абсолютно все расходы",
            f"<b>Пополнения</b>{EMOJI['entry']} - отправит абсолютно все пополнения",
            f"<b>Баланс</b> {EMOJI['card']} - отправит актуальный баланс",
            f"<b>Пополнить</b> {EMOJI['money']} - позволяет пополнить депозит"]


#BUTTON
MAIN_KEYBOARD = {
    'MAKE_REPORT': f"Сформировать отчет{EMOJI['report']}",
    'COSTS': f"Расходы{EMOJI['out']}",
    'ENTRIES': f"Пополнения{EMOJI['entry']}",
    'BALANCE': f"Баланс {EMOJI['card']}",
    'TOP_UP': f"Пополнить{EMOJI['money']}"
}


