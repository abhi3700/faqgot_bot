"""
    This file - `db.py` is to check the database data.
"""
import redis
import json
import pandas as pd
from input import REDIS_URL



# ---------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL)

print(r.keys())

# ---------------------------------------------------------------
df = pd.read_csv("../data/quiz.csv")
# print(df.head(10))

# all lists
que_list = df.question.tolist()
ans_list = df.answer.tolist()
a_list = df.a.tolist()
b_list = df.b.tolist()
c_list = df.c.tolist()
d_list = df.d.tolist()
# -----------------------------------------------------------------------------
"""Setting the database"""
for i in range(10):
    r.hset("quiz", str(i), json.dumps(dict(que= que_list[i], ans= ans_list[i], a= a_list[i], b= b_list[i], c= c_list[i], d= d_list[i])))


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
# quiz
for i in range(10):
    print(json.loads(r.hget("quiz", str(i))))