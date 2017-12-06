import numpy as np
# import pandas as pd

import requests
from bs4 import BeautifulSoup as bsoup

_URL_PATTERN_TEAM_SCHEDULE = "http://www.sports-reference.com/cbb/schools/{tm_link}/{year}-schedule.html"

class YearTeamGameSummaryScraper(object):
	def __init__(self, year, tm_link):
		self.year = year
		self.tm_link = tm_link

	def get_soup(self):
		self.url = _URL_PATTERN_TEAM_SCHEDULE.format(tm_link = self.tm_link, year = self.year)
		html = requests.get(self.url)
		soup = bsoup(html.text, 'html.parser')
		self.soup = soup


	def get_game_flds(self):
		schedule = self.soup.find('table',{'id':'schedule'})
		self.schedule_tbl = schedule
		flds = ['Team'] + [th.text for th in schedule.find('thead').find('tr').findAll('th')] + ['Year', 'box']
		self.schedule_flds = flds

	def get_games(self):
		games = []
		rows = self.schedule_tbl.tbody.findAll('tr', {'class' : ''})
		# rows = schedule.tbody.findAll('tr', {'class' : ''})
		for row in rows:
			cells = row.findAll('td')
			game = [self.tm_link] + [c.text for c in cells] + [self.year]
			lnk = cells[1].find('a').attrs['href'].replace('/cbb/boxscores/', '').replace('.html', '')
			game.append(lnk)
			game_dict = {fld : g for fld, g in zip(self.schedule_flds, game)}
			games.append(game_dict)

		self.games = games

	def get_year_team_summaries(self):
		self.get_soup()
		self.get_game_flds()
		self.get_games()
		return self.games