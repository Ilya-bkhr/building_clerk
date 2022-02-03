import datetime


from telegram.ext import ConversationHandler
from telegram import ParseMode


from db import (update_add_transaction, get_total_costs,
                get_total_deposit, get_price_per_category)
from keyboards import  main_keyboard, period_keyboard
from config import EMOJI, WELCOME_TEXT
from utilities import (format_text_costs, prepare_deposit, format_num,
                       period_of_report, display_data, create_begin_of_day,
                       check_comment)


def copy_past(update, context):
    text = update.message.text
    update.message.reply_text(text)


def welcome(update, context):
    update.message.reply_text(
        text = '\n'.join(WELCOME_TEXT),
        reply_markup=main_keyboard(),
        parse_mode=ParseMode.HTML
    )


def add_costs(update, context):
    text = update.message.text
    items = text.lower().split()
    sum = items[2]
    category = items[1]
    begin_of_day = create_begin_of_day()
    total_sum = get_price_per_category(items[1]) + sum
    comment = check_comment(items, category, begin_of_day, sum)
    text = [
            f"Запись добавленна: <u>{begin_of_day.strftime('%d %b')}</u> {EMOJI['pen']}",
            f"Категория: <b>{items[1]}</b>",
            f"Сумма: <b>{format_num(sum)}</b>",
            f"Коментарий: <b>{comment}</b>\n",
            f"Всего расходов по категории: <b>{format_num(total_sum)} руб.</b>{EMOJI['abacus']}"
        ]
    update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.HTML
    )


def deposit(update, context):
    update.message.reply_text(f"Введите сумму пополнения {EMOJI['pen']}")
    return 'sum'


def check_users_sum(update, context):
    try:
        sum = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            text=f"Нужно ввести число, без пробелов\nВведите сумму повторно...{EMOJI['pencil']}"
            )
        deposit(update, context)
    return sum


def add_deposit(update, context):
    sum = check_users_sum(update, context)
    update_add_transaction(update, sum, datetime.datetime.now())
    balance = get_total_deposit(1)
    text = [
        f"<b>Баланс пополнен на сумму:</b> {format_num(sum)} {EMOJI['receipt']}",
        f"<b>Баланс на сегодня:</b> {format_num(balance)} {EMOJI['money']}"
        ]
    update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


def get_balance(update, context):
    deposit = get_total_deposit(1)
    cost = get_total_costs(total=True)
    balance = deposit - cost
    date = datetime.datetime.now()
    text = [
        f"<b>Всего пополнений:</b> {format_num(deposit)} {EMOJI['entry']}",
        f"<b>Всего расходов:</b> {format_num(cost)} {EMOJI['out']}\n",
        f"Баланс на <b>{date.strftime('%d %b')}</b>: {format_num(balance)} {EMOJI['abacus']}"
        ]
    update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.HTML
    )


def total_cost_per_category(update, context):
    total_cost = get_total_costs(total=True)
    cost_per_category = get_total_costs(total=False)
    key_value = cost_per_category.items()
    text = format_text_costs(total_cost, key_value)
    update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML
        )


def total_deposit_transaction(update, context):
    text = prepare_deposit()
    update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML)


def make_report(update, context):
    update.message.reply_text(
        f"Выберете период{EMOJI['calendar']}",
        reply_markup=period_keyboard()
    )
    return 'report'


def get_report(update, context):
    query = update.callback_query
    query.answer()
    data_for_report = period_of_report(query.data)
    text = display_data(data_for_report)
    query.message.edit_text(
        text=text,
        parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def exception(update, context):
    update.message.reply_text(
        f"Для продолжения необходимо завершить формирование отчета{EMOJI['report']}")  
    return 'report'
