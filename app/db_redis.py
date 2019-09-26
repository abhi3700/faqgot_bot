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

# -----------------------------------------------------------------------------
"""delete all stored keys"""
for k in r.keys():
    r.delete(k)

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
for i in range(10):     # loop from 1 to 10
    r.hset("quiz", str(i+1), json.dumps(dict(que= que_list[i], ans= ans_list[i], a= a_list[i], b= b_list[i], c= c_list[i], d= d_list[i])))

# user details
r.hset("91834234567", "user", json.dumps(dict(username="abhi3703", total_attempt=-1)))
r.hset("91834234567", "correct", json.dumps(dict(count= 0)))
r.hset("91834234567", "incorrect", json.dumps(dict(count= 0)))
r.hset("91834234567", "score", 0)

r.hset("91814563465", "user", json.dumps(dict(username="abhi3702", total_attempt=-1)))
r.hset("91814563465", "correct", json.dumps(dict(count= 0)))
r.hset("91814563465", "incorrect", json.dumps(dict(count= 0)))
r.hset("91814563465", "score", 0)

r.hset("91826443332", "user", json.dumps(dict(username="abhi3701", total_attempt=-1)))
r.hset("91826443332", "correct", json.dumps(dict(count= 0)))
r.hset("91826443332", "incorrect", json.dumps(dict(count= 0)))
r.hset("91826443332", "score", 0)

# update the correct count and check if it is affecting other trees - incorrect, score
r.hset("91834234567", "correct", json.dumps(dict(count= 34)))

# -----------------------------------------------------------------------------
"""print all keys"""
# quiz
for i in range(10):
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

# -----------------------------------------------------------------------------
"""Finding the phone no. if username exists"""
# key_phone = ""
# for k in keys_list:
#     # print(k.decode('utf-8'))
#     dict_nested2_val2 = json.loads(r.get(k.decode('utf-8')))
#     if dict_nested2_val2['username'] == 'abhi3701':
#         key_phone = k.decode('utf-8')

# print(key_phone)


# curr_ans = json.loads(r.hget("quiz", str(0)))['ans']
# print(curr_ans[0].lower())

print(r.keys())
