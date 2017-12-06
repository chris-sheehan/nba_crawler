import os
import requests
from bs4 import BeautifulSoup
from funcs import *

import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup as bsoup


_URL_PATTERN_GAME_BOX = "https://www.basketball-reference.com/boxscores/{game_id}.html"


class GameBoxScraper(object):
	def __init__(self, game_id):
		self.game_id = game_id

	def get_soup(self):
		self.url = _URL_PATTERN_GAME_BOX.format(game_id = self.game_id)
		html = requests.get(self.url)
		soup = bsoup(html.text, 'html.parser')
		self.soup = soup

	def get_stat_tbls(self):
		self.stat_tbls = self.soup.findAll('table', {'class':'sortable'})

	def crawl_all_stat_tables(self):
		dfStats = pd.DataFrame()
		dfStatsAdvanced = pd.DataFrame()
		for tbl in self.stat_tbls:
			stats_dict = self.crawl_table(tbl)
			df = pd.DataFrame(stats_dict)
			if 'advanced' in tbl.attrs['id']:
				dfStatsAdvanced = pd.concat([dfStatsAdvanced, df], axis = 0)
			else:
				dfStats = pd.concat([dfStats, df], axis = 0)
		self.dfStats = dfStats
		self.dfStatsAdvanced = dfStatsAdvanced

	def crawl_table(self, tbl):
		flds = self.get_flds(tbl)
		player_stats = self.get_player_stats(tbl, flds)
		return player_stats

	def get_flds(self, tbl):
		thead = tbl.find('th', {'data-stat' : 'player'}).parent
		flds = [th_.attrs['data-stat'] for th_ in thead.findAll('th')]
		return flds

	def get_player_stats(self, tbl, flds):
		player_rows = tbl.tbody.findAll('tr', {'class' : ''})
		player_stats = []
		for player in player_rows:
			player_cell = player.findAll('th')
			stats_cells = player.findAll('td')
			row_cells = player_cell + stats_cells
			stats = {fld : cell.text for fld, cell in zip(flds, row_cells)}
			player_id = self.get_player_id(player.find('th'))
			stats['player_id'] = player_id
			team = tbl.attrs['id'].split('_')[1]
			stats['team'] = team
			stats['gm'] = self.game_id
			player_stats.append(stats)
		return player_stats

	def get_player_id(self, cell):
		try:
			player_id = cell.find('a').attrs['href'].split('/')[-1].replace('.html', '')
		except:
			player_id = None
		return player_id

	def get_game_stats(self):
		self.get_soup()
		self.get_stat_tbls()
		self.crawl_all_stat_tables()
		return self.dfStats, self.dfStatsAdvanced
