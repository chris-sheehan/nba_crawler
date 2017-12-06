
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

import datetime

pd.set_option('display.max_columns', 150)


# In[87]:

import timeit
import multiprocessing
import threading


# In[11]:

df_stats = pd.read_csv('player_stats.csv')
df_stats.drop(df_stats.columns[0], axis = 1, inplace= True)
df_stats_backup = df_stats.copy()


# In[12]:

REORDER_COLS = ['player_id', 'player', 'team', 'gm', 'mp', 'fg', 'fga', 'fg_pct', 'fg2', 'fg2a', 'fg2_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts']


# In[13]:

df_stats = df_stats[REORDER_COLS]
df_stats.insert(3, 'dt', df_stats.gm.apply(lambda g: datetime.datetime.strptime(g[:10], "%Y-%m-%d").date() ))
df_stats.sort(['dt', 'gm', 'team', 'player_id'], inplace = True)

df_stats.reset_index(inplace = True, drop = True)


# In[25]:

df_stats.insert(4, 'season', df_stats.dt.apply(lambda d:  d.year+1 if d.month > 4 else d.year))


# In[14]:

df_stats.insert(6, 'home_team', df_stats.apply(lambda r: r.team in r.gm, axis = 1))


# In[35]:

# df_stats_cum = df_stats.copy()
df_stats_backup= df_stats.copy()


# In[27]:

for c in df_stats_cum.columns:
    if 'pct' in c:
        df_stats_cum[c] = None


# In[ ]:

# numb_cols = df_stats_cum.columns[7:]
# for p in df_stats_cum.player_id.unique()[:20]:
#     print p
#     df_stats_cum.loc[df_stats_cum.player_id == p, numb_cols] = df_stats_cum.loc[df_stats_cum.player_id == p, numb_cols].cumsum(axis = 0)


# In[41]:

players = df_stats.player_id.unique()[:1000]


# In[97]:

def get_length_of_dataframe(p, y, numb_cols = numb_cols):
    # print p
    return df_stats.loc[(df_stats.player_id == p) & (df_stats.season == y), numb_cols].cumsum(axis = 0)
    pass

# def test_len(nn = 100):
#     print datetime.datetime.now()
#     df_stats[['player_id', 'season']].drop_duplicates().head(nn).apply(lambda r: get_length_of_dataframe(r.player_id, r.season), axis = 1)
#     print datetime.datetime.now()
    
def test_len(df):
    print datetime.datetime.now()
    df.apply(lambda r: get_length_of_dataframe(r.player_id, r.season), axis = 1)
    print datetime.datetime.now()


# In[86]:

test_len(500)


# In[103]:

df = df_stats[['player_id', 'season']].drop_duplicates().head(500)
res = []

t = threading.Thread(target = test_len, args = df)
res.append(t)
t.start()

# p = multiprocessing.Process(target = test_len, args = df)
# res.append(p)
# p.start()


# In[ ]:

# p = multiprocessing.Process(target=apply_find_opp, args=(df,counter,))
# p.start()


# In[ ]:




# In[ ]:




# In[83]:

print len(df_stats.player_id.unique())
print len(df_stats[['player_id', 'season']].drop_duplicates())


# In[34]:

df_stats_cum.loc[df_stats_cum.player_id.isin(df_stats_cum.player_id.unique()[:20])].sort('player_id').head()


# In[ ]:




# In[ ]:



