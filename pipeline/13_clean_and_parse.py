import re
import pickle
import pandas as pd
import numpy as np

# read pickle from step 02
with open('12_api_out.pkl', 'rb') as f:
    api_out = pickle.load(f)

# print(api_out)

def clean_name(text):
    if text[0]=='n':
        text=text[1:]
    elif text[0:2]=="b\'":
        text=text[2:]
    
    text = text.replace('\\n', ' ')
    return text

# clean up names
api_out['name'] = api_out['name'].apply(clean_name)

# map name as permid for people
api_out['permid'] = np.where(api_out.dtype == 'Person',api_out['name'], api_out['permid'])

def first_digit(text):
    if text[0].isdigit():
        return True
    return False

# remove those with stock symbol
api_out = api_out[~api_out['name'].map(first_digit)]
# print(api_out)

# change permid dtype to string
api_out.permid.apply(str)

def invalid_permid(permid):
    if permid==-1:
        return False
    elif permid == 'https://permid.org/1-404010':   # Organization
        return False
    elif re.match("[a-zA-Z\s]", permid):   # Person
        return True

    if len(permid)==10 and permid.isdigit():
        return True
    
    return False

# print(invalid_permid('4295863670'))

# remove invalid permid
api_out = api_out[api_out['permid'].map(invalid_permid)]
# print(api_out)

# remove if only one news
api_out = api_out.groupby("news_id").filter(lambda x: len(x) > 1)
print(api_out)

api_out.to_csv("13_clean.csv", index=False)

# csv has formatting issue, use pickle between stages
with open('13_out.pkl', 'wb') as f:
    pickle.dump(api_out, f)
