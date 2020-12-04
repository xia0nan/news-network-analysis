import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

PATH_DB = Path.home()/Path('db/')
sys.path.append(str(PATH_DB))

from db import DB

def get_db(db):
    return DB(db)

df_watchlist = pd.read_csv("in_watchlist.csv")
# print(df_watchlist)
permid_list = df_watchlist['permid'].tolist()
# print(permid_list)

# # get list of permid
# permid_list = list(watchlist['permid'].drop_duplicates())
permid_list_in_subject = [f"P:{permid}" for permid in permid_list]
print(permid_list_in_subject)

# constant
date_from = [None, '2020-01-01 00:00:00'][1]
where_date = f"AND timestamp >= '{date_from}' "

# timer
start = time.time()

sql_news = f"""
SELECT 
guid,
data->>'headline' as headline,
data->>'body' as body,
data->>'subjects' as tags
FROM wm_alert.public.article_raw 
WHERE subjects::jsonb ?| array{permid_list_in_subject} 
AND data->>'pubStatus' = 'stat:usable' 
AND data->>'language' = 'en'
{where_date}
ORDER BY timestamp ASC
"""

print(sql_news)

db_archive = get_db('alert_prod')

news = pd.read_sql(sql_news, con=db_archive.sql_engine)

print("news\n", news)

# get original permids out
permid_col = []

for i, item in news.iterrows():
    guid = item['guid']
    headline = item['headline']
    body = item['body']
    tags = eval(item['tags'])
    assert type(tags) is list
    
    # get permids as filtered list
    permids = [tag[2:] for tag in tags if tag.startswith("P:")]

    if len(permids) > 20:
        permids = permids[:2]
    print(i)
    print(permids)

    # save as string
    permids_str = f"{permids}"
    permid_col.append(permids_str)

# convert to ndarray to append to dataframe
permid_col = np.array(permid_col)
# print(permid_col)

# replace news
news['permids'] = permid_col
news = news.drop('tags', 1)

# timer
end = time.time()
print(f'SQL in {end-start:.2f} sec')

# check result
print(news)

news.to_csv("11_news.csv", index=False)

import pickle
# save as pickle
with open('news.pkl', 'wb') as f:
    pickle.dump(news, f)
