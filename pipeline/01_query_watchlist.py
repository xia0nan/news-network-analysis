"""
01. Query watchlist from wm_alert.watchlist to get list of permids
"""
import sys
import pandas as pd
from pathlib import Path
import pickle
import time

PATH_DB = Path.home()/Path('db/')
sys.path.append(str(PATH_DB))
from db import DB

def get_db(db):
    return DB(db)

db_web = get_db('alert_prod')

sql_watchlist = """
    SELECT DISTINCT 
    w.permid, p.company 
    FROM watchlist_entity w 
    JOIN permid p ON w.permid = p.permid 
    WHERE w.permid IS NOT NULL
    LIMIT 5
    """

watchlist = pd.read_sql(sql_watchlist, con=db_web.sql_engine)
print(watchlist)

# save as pickle
with open('watchlist.pkl', 'wb') as f:
    pickle.dump(watchlist, f)
