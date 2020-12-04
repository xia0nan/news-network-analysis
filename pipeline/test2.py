import pickle

import pandas as pd

# read pickle from step 02
with open('news.pkl', 'rb') as f:
    news = pickle.load(f)

print(news.info())