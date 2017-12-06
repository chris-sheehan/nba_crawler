import numpy as np
import pandas as pd
import datetime
import multiprocessing

df_stats = pd.read_csv('player_stats.csv')
df_stats.drop(df_stats.columns[0], axis = 1, inplace= True)
df_stats_backup = df_stats.copy()


REORDER_COLS = ['player_id', 'player', 'team', 'gm', 'mp', 'fg', 'fga', 'fg_pct', 'fg2', 'fg2a', 'fg2_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts']

df_stats = df_stats[REORDER_COLS]
df_stats.insert(3, 'dt', df_stats.gm.apply(lambda g: datetime.datetime.strptime(g[:10], "%Y-%m-%d").date() ))
df_stats.sort(['dt', 'gm', 'team', 'player_id'], inplace = True)
df_stats.reset_index(inplace = True, drop = True)

df_stats.insert(4, 'season', df_stats.dt.apply(lambda d:  d.year+1 if d.month > 4 else d.year))
df_stats.insert(6, 'home_team', df_stats.apply(lambda r: r.team in r.gm, axis = 1))

df_stats_backup= df_stats.copy()

numb_cols = df_stats_cum.columns[7:]

def break_up_df_by_column(df, column):
	dfs = {}
	columns = df[column].unique()
	for c in columns:
	    dfs[c] = df.loc[df[column] == c]
	return dfs

def cumsum_player_stats(df, numb_cols = numb_cols):
	df.loc[:, numb_cols] = df.loc[:, numb_cols].cumsum(axis = 0)
	return df


seasons_dfs = break_up_df_by_column(df_stats, 'season')

df = seasons_dfs[2011]
players = df.player_id.unique()[:500]
df_final = pd.DataFrame()
for p in players:
	dftmp = df[df.player_id == p]
	df_final = df_final.concat(cumsum_player_stats(dftmp))	

# df = df_stats[['player_id', 'season']].drop_duplicates().head(500)
res = []
p = multiprocessing.Process(target = test_len, args = df)
res.append(p)
p.start()

