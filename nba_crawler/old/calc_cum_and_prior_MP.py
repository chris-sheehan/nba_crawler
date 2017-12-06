import numpy as np
import pandas as pd

import time
import multiprocessing as mp

dfTeamGames = pd.read_csv('team_level_game_stats.csv')

# Parse into season-specific dataframes
dfBySeason = {y : dfTeamGames[dfTeamGames.season == y] for y in dfTeamGames.season.unique()}
for yr in dfBySeason:
	dfBySeason[yr].sort(['team', 'dt'], inplace = True)

ignore_cols = ['opp_link', 'conference', 'opp_conference', 'team_opp']
numb_cols = [c for c in dfTeamGames.columns[7:].tolist() if c not in ignore_cols]

def log_result(result):
	result_list.append(result)

def get_team_cum_stats_entering_game(df):
	global numb_cols
	# Get cum stats including current game and set to [fld_name]_cum
	cum_cols = [c + '_cum' for c in numb_cols]
	prior_cols = [c + '_prior' for c in numb_cols]

	for nc, cc, pc in zip(numb_cols, cum_cols, prior_cols):
		df[cc] = None
		df[pc] = None

	for t in df.team.unique():
		df.loc[df.team == t, cum_cols] = df.loc[df.team == t, numb_cols].cumsum(axis = 0).values
		for nc, cc, pc in zip(numb_cols, cum_cols, prior_cols):
			df.loc[df.team == t, pc] = df.loc[df.team == t, cc] - df.loc[df.team == t, nc]
	print df.season.values[0]
	return df

def calculate_percentages(df):
	for c in [x for x in df.columns if 'pct' in x]:
		if 'net' in c:
			off_col = c.replace('_net', '')
			def_col = c.replace('_net', '_opp')
			df[c] = df[off_col] - df[def_col]
		else:
			join_char = '_' if len(c.split('_')) > 2 else ''
			numerator = join_char.join([c.split('_')[0]] + c.split('_')[2:])
			denominator = join_char.join([c.split('_')[0] + 'a'] + c.split('_')[2:])
			# print '{0} = {1}/{2}'.format(c, numerator, denominator)
			df[c] = df[numerator].map(float)/df[denominator].map(float)
	return df

if __name__ == '__main__':
	result_list = []
	pool = mp.Pool()
	for df in dfBySeason.values():
		# pool.apply_async(get_num_unique_teams, args = (df, )fg_pct_net, callback = log_result)
		pool.apply_async(get_team_cum_stats_entering_game, args = (df[df.team.isin(df.team.unique())], ), callback = log_result)
	pool.close()
	pool.join()
	# print(result_list)
	df_final = pd.concat(result_list, axis = 0)
	df_final = calculate_percentages(df_final)
	df_final.to_csv('team_game_final.csv', index = False)
	print 'Done.'