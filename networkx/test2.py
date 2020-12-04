from pathlib import Path

import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objects as go
import networkx as nx
import re

PATH_SRC = Path(__file__).resolve().parent
PATH_PROJECT = PATH_SRC.parent
PATH_DATA = PATH_PROJECT / 'data'

df = pd.read_csv(str(PATH_DATA/'test2.csv'))
print(df)