import pandas as pd
import numpy as np


df = pd.read_csv('data/quiz.csv')
df = df.iloc[np.random.permutation(len(df))]
df.reset_index(drop= True, inplace=True)
print(len(df))
print(df.head(10))