import os
import re

import requests
import random

NH_API_CREATE_REAL_ORDER = int(os.environ.get('NH_API_CREATE_REAL_ORDER', 0))

NH_API_ID = os.environ.get('NH_API_ID')
NH_API_KEY = os.environ.get('NH_API_KEY')

API_URL = 'https://api.nicehash.com/api'

PRIVATE_METHODS = ['orders.get&my', 'orders.create', 'orders.refill', 'orders.remove', 'orders.set.price',
                   'orders.set.price.decrease', 'orders.set.limit', 'balance']


def query(method, params=None):
    params = params or {}
    if method == 'orders.get&my':
        params['method'] = 'orders.get'
        params['my'] = 1
    else:
        params['method'] = method
    if method in PRIVATE_METHODS:
        params['id'] = NH_API_ID
        params['key'] = NH_API_KEY

    ret = requests.get(API_URL, params)
    return ret


def balance():
    resp = query('balance')
    ret = resp.json()
    result = ret['result']
    confirmed, pending = float(result['balance_confirmed']), float(result['balance_pending'])
    return confirmed, pending


def hashing_power(algo):
    resp = query('stats.global.current')
    ret = resp.json()
    stats = ret['result']['stats']
    for stat in stats:
        if stat['algo'] == algo:
            return float(stat['speed'])


def fake_orders_iter():
    random.seed()
    start = random.randint(385, 200000)
    for i in range(start, start + 20000):
        yield i


fake_orders = fake_orders_iter()


def create_order(algo, location, amount, price, limit, pool_host, pool_port, pool_user, pool_pass):
    params = {
        'location': location,
        'algo': algo,
        'amount': amount,
        'price': price,
        'limit': limit,
        'pool_host': pool_host,
        'pool_port': pool_port,
        'pool_user': pool_user,
        'pool_pass': pool_pass,

    }
    print("Creating NH order with params:", params)
    if NH_API_CREATE_REAL_ORDER:
        resp = query('orders.create', params)
        ret = resp.json()
        # {'result': {'success': 'Order #134627 created.'}, 'method': 'orders.create'}
        result = ret['result']
        order = result.get('success')
        if order:
            order_no = re.compile(r'#(?P<order>[\d]+)').findall(order)[0]
            return order_no
        else:
            print('Error:')
            print(ret)
    else:
        return next(fake_orders)


def my_open_orders(location, algo):
    resp = query('orders.get&my', {'location': location, 'algo': algo})
    ret = resp.json()
    return ret['result']['orders']


def close_order(location, algo, order):
    resp = query('orders.remove', {'location': location, 'algo': algo, 'order': order})
    ret = resp.json()
    return ret['result']

