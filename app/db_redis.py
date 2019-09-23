"""
    This file - `db.py` is to check the database data.
"""
import redis
import json
from input import REDIS_URL



# ---------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL)

print(r.keys())

# -----------------------------------------------------------------------------
"""Finding the phone no. if username exists"""
# key_phone = ""
# for k in keys_list:
#     # print(k.decode('utf-8'))
#     dict_nested2_val2 = json.loads(r.get(k.decode('utf-8')))
#     if dict_nested2_val2['username'] == 'abhi3701':
#         key_phone = k.decode('utf-8')

# print(key_phone)

# -----------------------------------------------------------------------------
"""delete all stored keys"""
# for k in r.keys():
#     r.delete(k)

# -----------------------------------------------------------------------------
"""print all keys"""
# for k in r.keys():
#     k_decoded = k.decode('utf-8')
#     # print(k_decoded)
#     print(json.loads(r.get(k_decoded).decode('utf-8')))
    # print(json.loads(r.get(k_decoded).decode('utf-8'))['username'])
    # print(json.loads(r.get(k_decoded).decode('utf-8'))['breed_choice'])
# print(r.keys())