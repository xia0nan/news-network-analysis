import sys
from pathlib import Path

PATH_DB = Path.home()/Path('db/')
sys.path.append(str(PATH_DB))
from db import DB

def get_db(db):
    return DB(db)
# initialize DB
db_web = get_db('network_analysis')

print("successful")

print(db_web.table_names())
