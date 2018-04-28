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

# Nicehash algorithms

nha_Scrypt = 0
nha_SHA256 = 1
nha_ScryptNf = 2
nha_X11 = 3
nha_X13 = 4
nha_Keccak = 5
nha_X15 = 6
nha_Nist5 = 7
nha_NeoScrypt = 8
nha_Lyra2RE = 9
nha_WhirlpoolX = 10
nha_Qubit = 11
nha_Quark = 12
nha_Axiom = 13
nha_Lyra2REv2 = 14
nha_ScryptJaneNf16 = 15
nha_Blake256r8 = 16
nha_Blake256r14 = 17
nha_Blake256r8vnl = 18
nha_Hodl = 19
nha_DaggerHashimoto = 20
nha_Decred = 21
nha_CryptoNight = 22
nha_Lbry = 23
nha_Equihash = 24
nha_Pascal = 25
nha_X11Gost = 26
nha_Sia = 27
nha_Blake2s = 28
nha_Skunk = 29

ALGO_CHOICES = (
    (nha_Scrypt, 'Scrypt'),
    (nha_SHA256, 'SHA256'),
    (nha_Nist5, 'Nist5'),
    (nha_Skunk, 'Skunk'),
    (nha_NeoScrypt, 'NeoScrypt'),
    (nha_Equihash, 'Equihash'),
    (nha_DaggerHashimoto, 'DaggerHashimoto'),
    (nha_X11, 'X11'),
    (nha_Decred, 'Decred'),
    (nha_CryptoNight, 'CryptoNight'),
    (nha_Qubit, 'Qubit'),
    (nha_Keccak, 'Keccak'),

)


tera_algo = [nha_X11, nha_Skunk]


def gen_speed(k):
    if k in tera_algo:
        return 'TH/s'
    else:
        return 'GH/s'


ALGO_SPEED = {k: gen_speed(k) for k, v in ALGO_CHOICES}

mil = 1000


# Nicehash order types

nhot_Standard_Order = 0
nhot_Fixed_Order = 1


# Nicehash Locations

nhl_Europe = 0
nhl_USA = 1

LOCATION_CHOICES = (
    (nhl_Europe, 'Europe'),
    (nhl_USA, 'USA'),
)


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


def set_limit(location, algo, order, limit):
    """
    https://api.nicehash.com/api?method=orders.set.limit&id=8&key=3583b1df-5e93-4ba0-96d7-7d621fe15a17&location=0&algo=0&order=1881&limit=1.0
    :param location:
    :param algo:
    :param order:
    :param limit:
    :return:
    """
    resp = query('orders.set.limit', {'location': location, 'algo': algo, 'order': order, 'limit': limit})
    ret = resp.json()
    return ret['result']


def set_price(location, algo, order, price):
    """
    https://api.nicehash.com/api?method=orders.set.price&id=8&key=3583b1df-5e93-4ba0-96d7-7d621fe15a17&location=0&algo=0&order=1881&price=2.1
    :param location:
    :param algo:
    :param order:
    :param price:
    :return:
    """
    resp = query('orders.set.price', {'location': location, 'algo': algo, 'order': order, 'price': price})
    ret = resp.json()
    return ret['result']


def refill(location, algo, order, amount):
    """
    https://api.nicehash.com/api?method=orders.refill&id=8&key=3583b1df-5e93-4ba0-96d7-7d621fe15a17&location=0&algo=0&order=123&amount=0.01
    :param location:
    :param algo:
    :param order:
    :param amount:
    :return:
    """
    resp = query('orders.refill', {'location': location, 'algo': algo, 'order': order, 'amount': amount})
    ret = resp.json()
    return ret['result']
