import os
import sys
from pathlib import Path
import random

import numpy as np
import pandas as pd

PATH_SRC = Path(__file__).resolve().parent
PATH_PROJECT = PATH_SRC.parent
PATH_DATA = PATH_PROJECT / 'data'

abbr_name = 'abbreviations.csv'

target_path = "../d3-network-analysis/static/data/"

df = pd.read_csv(str(PATH_DATA/'network_banks_temp4.csv'))
df.dropna(inplace=True)
# print(df.head())

df_abbr = pd.read_csv(target_path + abbr_name)
# print(df_abbr.head())

df_temp = df.join(df_abbr.set_index('name'), on='source_company')
# print(df_temp)

df_temp = df_temp.rename(columns={'source_company': 'to_drop', 'abbr': 'source_company'})
# print(df_temp)

df_temp = df_temp[['source_company', 'target_company', 'c_news']]
# print(df_temp)

df_temp = df_temp.join(df_abbr.set_index('name'), on='target_company')
# print(df_temp)

df_temp = df_temp.rename(columns={'target_company': 'to_drop', 'abbr': 'target_company'})
# print(df_temp)

df_temp = df_temp[['source_company', 'target_company', 'c_news']]
# print(df_temp)

df_temp.to_csv(str(PATH_DATA/'network_banks_temp5.csv'), index=False)

