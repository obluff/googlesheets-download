
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import io
from creds import url


# In[18]:


#dictionary of sheet names and their respective ids 
sheets = {'generalData': '720376750', 'projected': '1359182790', 'actual': '774530743'}


# In[11]:


#function that returns a pandas dataframe of the spreadsheet
def getData(gid, name):
    r = requests.get(url + '=' + gid)
    s = r.content
    return pd.read_csv(io.StringIO(s.decode('utf-8')))


# In[19]:


#populating a dictionary with all the items in the sheets df
dfs = {}
for x in sheets.keys():
    dfs[x] = getData(sheets[x], x)


# In[20]:


#writing information from google sheets into the database 
from sqlTool import to_sql_auto
from credentials import connectionString

engine = sqlalchemy.create_engine(connectionString)

for x in dfs.keys():
    print('writing ' + x + ' to the database')
    to_sql_auto(engine, dfs[x], 'gsheets_' + x)

