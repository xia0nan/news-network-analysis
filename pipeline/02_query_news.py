import sys
import time
from pathlib import Path
import pickle

import numpy as np
import pandas as pd

PATH_DB = Path.home()/Path('db/')
sys.path.append(str(PATH_DB))

from db import DB

def get_db(db):
    return DB(db)

# read pickle from step 01
with open('watchlist.pkl', 'rb') as f:
    watchlist = pickle.load(f)

# get list of permid
permid_list = list(watchlist['permid'].drop_duplicates())
permid_list_in_subject = [f"P:{permid}" for permid in permid_list]

# constant
date_from = [None, '2020-07-01 00:00:00'][1]
where_date = f"AND timestamp >= '{date_from}' "

# timer
start = time.time()

sql_news = f"""
SELECT 
guid,
data->>'headline' as headline,
data->>'body' as body,
data->>'subjects' as tags
FROM article_raw 
WHERE subjects::jsonb ?| array{permid_list_in_subject} 
AND data->>'pubStatus' = 'stat:usable' 
AND data->>'language' = 'en'
{where_date}
ORDER BY timestamp DESC
LIMIT 3
"""

db_archive = get_db('wm_alert')

news = pd.read_sql(sql_news, con=db_archive.sql_engine)
# print(news)

permid_col = []

for i, item in news.iterrows():
    guid = item['guid']
    headline = item['headline']
    body = item['body']
    tags = eval(item['tags'])
    assert type(tags) is list
    
    # get permids as filtered list
    permids = [tag[2:] for tag in tags if tag.startswith("P:")]
    # print(i)
    # print(permids)

    # save as string
    permids_str = f"{permids}"
    permid_col.append(permids_str)

# convert to ndarray to append to dataframe
permid_col = np.array(permid_col)
# print(permid_col)

# replace news
news['permids'] = permid_col
news = news.drop('tags', 1)

# print(news.columns)
# print(news)

# save as pickle
with open('news.pkl', 'wb') as f:
    pickle.dump(news, f)
