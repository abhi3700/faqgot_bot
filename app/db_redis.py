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
# quiz
# for i in range(10):
#     r.hset("quiz", str(i), json.dumps(dict(que= que_list[i], ans= ans_list[i], a= a_list[i], b= b_list[i], c= c_list[i], d= d_list[i])))
# # user details
r.set("918145634656", json.dumps(dict(username="abhi3701",correct_count=4, incorrect_count=4, total_attempt=8,score=50)))
r.set("918264433324", json.dumps(dict(username="abhi3702",correct_count=4, incorrect_count=4, total_attempt=8,score=50)))

# -----------------------------------------------------------------------------
"""delete all stored keys"""
# for k in r.keys():
#     r.delete(k)

# -----------------------------------------------------------------------------
"""print all keys"""
# quiz
# for i in range(10):
#     print(json.loads(r.hget("quiz", str(i))))

keys_list = r.keys()
# print(keys_list.remove(b'quiz'))
keys_list.remove(b'quiz')
# print(keys_list)

"""print user's details"""
for k in keys_list:
    k_decoded = k.decode('utf-8')
    print(json.loads(r.get(k_decoded)))
    print(json.loads(r.get(k_decoded))['username'])
    print(json.loads(r.get(k_decoded))['correct_count'])
    print(json.loads(r.get(k_decoded))['incorrect_count'])
    print(json.loads(r.get(k_decoded))['total_attempt'])
    print(json.loads(r.get(k_decoded))['score'])
# -----------------------------------------------------------------------------
"""Finding the phone no. if username exists"""
key_phone = ""
for k in keys_list:
    # print(k.decode('utf-8'))
    dict_nested2_val2 = json.loads(r.get(k.decode('utf-8')))
    if dict_nested2_val2['username'] == 'abhi3701':
        key_phone = k.decode('utf-8')

print(key_phone)
