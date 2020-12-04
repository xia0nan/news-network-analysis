import sys
import time
from pathlib import Path

import pandas as pd

PATH_DB = Path.home()/Path('db/')
sys.path.append(str(PATH_DB))

from db import DB

def get_db(db):
    return DB(db)

db_archive = get_db('alert_prod')


sql = """
SELECT
guid,
data->>'headline' as headline,
data->>'body' as body,
data->>'subjects' as tags
FROM wm_alert.public.article_raw
WHERE subjects::jsonb ?| array['P:4295887834', 'P:4295888106', 'P:5000074278', 'P:4295884238', 'P:4295883663', 'P:4295863670']
AND data->>'pubStatus' = 'stat:usable'
AND data->>'language' = 'en'
AND timestamp >= '2020-07-01 00:00:00'
ORDER BY timestamp ASC
"""

news = pd.read_sql(sql, con=db_archive.sql_engine)
print(news)
