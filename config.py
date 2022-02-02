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
         'no': emojize(':cross_mark:', use_aliases=True)}

#TEXT
WELCOME_TEXT = [f"Привет пользователь, я Билдер - клерк по стройке {EMOJI['builder']}",
                "Я помогу контролировать расходы во время стройки",
                f"Нажимай /info что бы узнать про мои способности"]



#BUTTONS
MAIN_KEYBOARD = {
    'MAKE_REPORT': f"Сформировать отчет{EMOJI['report']}",
    'COSTS': f"Расходы{EMOJI['out']}",
    'ENTRIES': f"Пополнения{EMOJI['entry']}",
    'BALANCE': f"Баланс {EMOJI['card']}",
    'TOP_UP': f"Пополнить{EMOJI['money']}"
}


