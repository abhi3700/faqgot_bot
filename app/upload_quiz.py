"""
    This file is to upload the QUIZ (in CSV) data to Redis DB.
"""
import redis
import json
import pandas as pd
from input import REDIS_URL



# ---------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL)

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
for i in range(len(a_list)):     # loop from 1 to 10
    r.hset("quiz", str(i+1), json.dumps(dict(que= que_list[i], ans= ans_list[i], a= a_list[i], b= b_list[i], c= c_list[i], d= d_list[i])))
