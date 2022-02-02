from pymongo import MongoClient

import settings


client = MongoClient(settings.MONGO_LINK)
db = client[settings.MONGO_DB]


def update_add_transaction(update, date, sum):
    '''Обновляет информацию о пополнениях в базе'''
    db.deposit.update_one(
        {'id': update.effective_user.id},
        {'$push': {'transaction_info': {'date': date, 'amount': sum}}},
        True)


#добавить вывод существующих категорий для удобного ввода
def get_category_list(db):
    '''Получения из базы списков всех категорий расходов'''
    category = db.costs.find({}, {'type': 1, '_id': 0})
    category_list = list(category)
    new_list = []
    for i in category_list:
        element = list(i.values())
        new_list.append(element[0])
    return new_list


def get_total_costs(total=False):
    '''Получение всех расходов по каждой категории'''
    category_list = get_category_list(db)
    cost_per_category = {}
    total_sum = 0
    for i in category_list:
        sum = get_price_per_category(i)
        total_sum += sum
        cost_per_category[i] = sum
    if total is False:
        return cost_per_category
    else:
        return total_sum


def get_total_deposit(id):
    '''Достает из базы все пополнения'''
    total_cost = db.deposit.aggregate([
        {'$match': {'id': id}},
        {'$unwind': {'path': '$transaction_info'}},
        {'$group': {'_id': id, 'total_sum': {'$sum': '$transaction_info.amount'}}}
        ])
    total_deposit = next(total_cost, None)
    if total_deposit:
        return total_deposit['total_sum']
    return 0


def get_price_per_category(category_name):
    '''Достает из базы все категории и общие расходы по ним'''
    total_cost = db.costs.aggregate([
        {'$match': {'type': category_name}},
        {'$unwind': {'path': '$transaction_info'}},
        {'$group': {
            '_id': category_name, 'total_sum': {
                '$sum': '$transaction_info.amount'}}}
        ])
    total_cost = next(total_cost, None)
    if total_cost:
        return total_cost['total_sum']
    return 0