import logging
import locale


from telegram.ext import (Updater, MessageHandler, Filters,
                          CommandHandler, ConversationHandler,
                          CallbackQueryHandler)


import settings
from config import MAIN_KEYBOARD
from handlers import (copy_past, add_costs, welcome, deposit,
                      add_deposit, get_balance, total_cost_per_category,
                      total_deposit_transaction, make_report, get_report,
                      exception, get_info)


logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    locale.setlocale(category=locale.LC_ALL, locale='ru_RU.utf-8')
    my_bot = Updater(settings.API_KEY, use_context=True)
    dp = my_bot.dispatcher
    deposit_money = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(MAIN_KEYBOARD['TOP_UP']), deposit),
                      MessageHandler(Filters.regex(MAIN_KEYBOARD['MAKE_REPORT']), make_report)],
        states={'sum': [MessageHandler(Filters.text, add_deposit)],
                'report': [CallbackQueryHandler(get_report, pattern='^(7|30|60)$'),
                           MessageHandler(Filters.regex(MAIN_KEYBOARD['MAKE_REPORT']), make_report),
                           MessageHandler(Filters.text, exception)]},
        fallbacks=[]
    )
    dp.add_handler(deposit_money)
    dp.add_handler(CommandHandler('start', welcome))
    dp.add_handler(CommandHandler('add', add_costs))
    dp.add_handler(CommandHandler('info', get_info))
    dp.add_handler(MessageHandler(Filters.regex(MAIN_KEYBOARD['COSTS']), total_cost_per_category))
    dp.add_handler(MessageHandler(Filters.regex(MAIN_KEYBOARD['ENTRIES']), total_deposit_transaction))
    dp.add_handler(MessageHandler(Filters.regex(MAIN_KEYBOARD['BALANCE']), get_balance))
    dp.add_handler(MessageHandler(Filters.text, copy_past))
    logging.info('Bot have started')
    my_bot.start_polling()
    my_bot.idle()


if __name__ == '__main__':
    main()
