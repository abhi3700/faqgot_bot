"""
    This file is to view the database data.
"""
import redis
import json
import pandas as pd
from input import *



# ---------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL)

# -----------------------------------------------------------------------------
print(r.keys())

# -----------------------------------------------------------------------------
"""print all keys"""
# quiz
for i in range(QUIZ_COUNT):
    print(json.loads(r.hget("quiz", str(i+1))))

keys_list = r.keys()
keys_list.remove(b'quiz')
# print(keys_list)

"""print user's details"""
for k in keys_list:
    k_decoded = k.decode('utf-8')
    print('==========================')
    print(k_decoded)
    print(json.loads(r.hget(k_decoded, "user")))
    print(json.loads(r.hget(k_decoded, "user"))['username'])
    print(json.loads(r.hget(k_decoded, "user"))['total_attempt'])
    print(json.loads(r.hget(k_decoded, "correct"))['count'])
    print(json.loads(r.hget(k_decoded, "incorrect"))['count'])
    print(json.loads(r.hget(k_decoded, "score")))
