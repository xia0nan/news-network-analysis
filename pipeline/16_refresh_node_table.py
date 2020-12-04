import sys
from pathlib import Path

import pickle
import pandas as pd

PATH_DB = Path.home()/Path('db/')
sys.path.append(str(PATH_DB))
from db import DB

def get_db(db):
    return DB(db)
# initialize DB
db_web = get_db('network_analysis')

# get permid associated with names
sql_node_clean = """
SELECT DISTINCT
n.node_id, p.company as name, n.dtype, n.permid
FROM node n
JOIN permid p ON n.permid = p.permid
WHERE n.permid ~ '^[0-9\.]+$'
UNION
SELECT DISTINCT *
FROM node n
WHERE NOT n.permid ~ '^[0-9\.]+$';
"""

node_clean = pd.read_sql(sql_node_clean, con=db_web.sql_engine)
print(node_clean)

# replace in postgres
node_clean.to_sql('node', con=db_web.sql_engine, if_exists='replace', index=False)
