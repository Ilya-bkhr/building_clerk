import datetime as dt


from humanize import intcomma


from db import db
from config import EMOJI


def format_text_costs(total_cost, key_value):
    '''Подготовка списка всех расходов и и обзей суммы (в текстовом виде)'''
    count = 1
    end_text = f"<b>Расходы по категориям:</b> {EMOJI['out']}\n\n"
    for i in key_value:
        format_category_name = i[0].replace("_", " ").capitalize()
        text = f'{count}. {format_category_name} - {format_num(i[1])}\n'
        end_text += text
        count += 1
    total_result = f"\n<b>Всего потраченно:</b> {format_num(total_cost)}  {EMOJI['abacus']}"
    total_text = end_text + total_result
    return total_text


def prepare_deposit_list(deposit_data):
    '''Подготовка списка в текстовом виде всех пополнений и общей суммы пополнений'''
    counter = 1
    total_deposit = 0
    text = f"<b>Пополнения по датам:</b> {EMOJI['entry']}\n\n"
    for i in deposit_data:
        date = i['date']
        amount = i['amount']
        text += f"{counter}. {date.strftime('%d %b')} - {format_num(amount)}\n"
        total_deposit += amount
        counter += 1
    return {'deposit_list': text, 'total_deposit': total_deposit}


def prepare_deposit():
    '''Результирующая подготовка текста для вывода всех пополнений'''
    data = list(db.deposit.find({}, {'transaction_info': 1, '_id': 0}))
    deposit_data = data[0]['transaction_info']
    deposit_info = prepare_deposit_list(deposit_data)
    total_text = f"\n<b>Всего пополнений на сумму:</b> {format_num(deposit_info['total_deposit'])}  {EMOJI['abacus']}"
    result_text = deposit_info['deposit_list'] + total_text
    return result_text


def format_num(number):
    '''Форматирует все числа выводимые в сообщениях в читабельном виде'''
    triada = intcomma(number)
    result = triada.replace(',', ' ')
    final_result = f'<i>{result}₽</i>'
    return final_result


def create_begin_of_day():
    '''Создает объект DATETIME с первой секундной дня'''
    today_date = dt.date.today()
    today_time = dt.time(0, 0)
    begin_of_day = dt.datetime.combine(today_date, today_time)
    return begin_of_day


def day_broads(date):
    """Принимает объект datetime возвращаяет начальную конечную секунду дня"""
    start_time = dt.time(0, 0)
    end_time = dt.time(23, 59)
    day_begin = dt.datetime.combine(date, start_time)
    day_end = dt.datetime.combine(date, end_time)
    day = {'day_begin': day_begin, 'day_end': day_end}
    return day


def translate_date(query):
    '''Принимает период из CALLBACK и возвращает день с которого нужно оформить
    отчет и период в формате DATETIME'''
    days_quanity = int(query)
    chosen_period = dt.timedelta(days=days_quanity)
    report_day = dt.datetime.now() - chosen_period
    return {'report_day': report_day, 'days_quanity':days_quanity}


def check_comment(items, category, begin_of_day, sum):
    ''''Проверяет есть ли коментарий при добавлении операции о расходе'''
    if len(items) > 3:
        counter = 3
        comment = ''
        while counter < len(items):
            comment += str(items[counter]) + ' '
            counter += 1
        add_to_db(category, begin_of_day, sum, comment=comment)
        comment = comment
    else:
        add_to_db(category, begin_of_day, sum)
        comment = 'Не указан'
    return comment


def period_of_report(callback_data):
    '''Примнимает количество дней из callback_data возвращает словарь, дата: траты по категории'''
    data_info = translate_date(callback_data)
    report_day = data_info['report_day']
    report_result = {}
    callback_data = int(callback_data) + 1
    for i in range(callback_data):
        broad = day_broads(report_day)
        current_day_report = db.costs.aggregate([
            {'$unwind': '$transaction_info'},
            {'$match': {'transaction_info.date':
                {'$gt': broad['day_begin'], '$lte': broad['day_end']}}},
            {'$group': {'_id': '$type', 'total_cost':
                {'$sum': '$transaction_info.amount'}}}
        ])
        values = {report_day: list(current_day_report)}
        report_result.update(values)
        report_day += dt.timedelta(days=1)
    return report_result


def format_deposit_report(data):
    '''Подготовка списка (в текстовом виде) пополнений'''
    if len(data) == 0:
        deposit_per_date = f"{EMOJI['no']}\n"
    else:
        count = 1
        deposit_per_date = '\n'
        for i in data:
            sum = format_num(i['transaction_info']['amount'])
            text = f"{count}. {sum}\n"
            deposit_per_date += text
            count += 1
    return deposit_per_date


def format_costs_report(costs_per_date):
    ''''Подготовка списка (в текстовом виде) категорий по которым были расходы'''
    if len(costs_per_date) == 0:
        text_category_price_total = f"{EMOJI['no']}"
    else:
        text_category_price_total = '\n'
        count = 1
        for costs_type in costs_per_date:
            category = costs_type.get('_id')
            category = category.replace('_', ' ').capitalize()
            price = costs_type.get('total_cost')
            price = format_num(price)
            text_category_price = f'{count}. {category}: {price}\n'
            text_category_price_total += text_category_price
            count += 1
    return text_category_price_total


def display_data(report_result):
    '''Подготовка отчета за выбранный период в текстовом виде'''
    final_text = f"Операции:{EMOJI['aprove']}\n\n"
    deposit_text = "\nПополнения\n"
    for key in report_result:
        data = get_deposit_report(key)
        deposit_per_date = format_deposit_report(data)
        array = report_result.get(key)
        text_category_price_total = format_costs_report(array)
        text_per_day = [f"{key.strftime('%d %b')} {EMOJI['calendar']}",
                        f"<b>Расходы</b> {text_category_price_total}"]
        deposit_text = f"<b>\nПополнения</b> {deposit_per_date}\n"
        final_text = final_text + '\n'.join(text_per_day) + deposit_text
    return final_text


def add_to_db(category, date, sum, comment=None):
    '''Обнавляет статью расходов в БД или добавляет к уже сущесвующей'''
    db.costs.update_one(
            {'type': category},
            {'$push': {'transaction_info': {
                'date': date, 'amount': sum, 'comment': comment}}},
            True)


def get_deposit_report(date):
    ''''Запрашивает из базы данных все пополнения с первой минуты суток дл последней'''
    day_for_deposit = day_broads(date)
    data = db.deposit.aggregate([
        {'$unwind': '$transaction_info'},
        {'$match': {'transaction_info.date': {'$gt': day_for_deposit['day_begin'],'$lte': day_for_deposit['day_end']}}}
    ])
    data = list(data)
    return data