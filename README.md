# nicehash_api

python nicehash wrapper

## Installing

pip install https://github.com/degconnect/nicehash_api/archive/master.zip

or

git+git://github.com/edilio/nicehash_api.git # from requirement file

## Use

Using public methods don't required any config so you can start using it after installing:

ex.

```python
import nicehash_api

print(nicehash_api.hashing_power(nicehash_api.nha_Equihash))
```
Private methods need NH_API_ID, NH_API_KEY set on your environment following best practices so you don't expose them.

Supposing that your credentials are already on your envirorment variables:

```python
import nicehash_api

print(nicehash_api.balance())
```


## Donations

You can support this project donating to degconnect:

BTC : 18TAw57LUveA5CoqMfkWheNGXiDpqRcwmn

ETH: 0x23efacc1634d8b12a9e5acee330b1f28b1a3068c

LTC: Lcw9cWpW72E18m2LJRe8YG2Pk6AC2K5FN4

ZEC: t1QZVBhVviLwr1D9qpk9U6pSmLrEFNcU1Wq
