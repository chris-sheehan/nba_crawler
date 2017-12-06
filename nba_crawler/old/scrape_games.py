# python
# Scrape box scores for team-level stats

import numpy as np
import pandas as pd

import datetime
from dateutil import relativedelta

import requests
from bs4 import BeautifulSoup as bsoup
# import re

re_trim_rank_pattern = "^\([0-9]*\)\s"
url_pattern = "http://www.sports-reference.com/cbb/boxscores/index.cgi?month=%d&day=%d&year=%d"

# date variables
start_date = datetime.datetime(2016,11,11)
tdelta = relativedelta.relativedelta(days=1)
# end_date = datetime.datetime.today()
end_date = start_date + tdelta
game_date = start_date

# scraping variables
game_tbl_class = "no_highlight stats_table wide_table"
url_class = "align_right bold_text"

def get_teams_from_game_tbl(tbl_):
	tms = tbl_.find('table', {'class' : 'no_highlight wide_table'}).findAll('tr')
	v = re.sub(re_trim_rank_pattern,"",tms[0].find('td').text)
	h = re.sub(re_trim_rank_pattern,"",tms[1].find('td').text)
	return v,h

def get_game_stats(url_):
	gm_html = requests.get(url_)
	gbsoup = soup(gm_html.text, 'html.parser')

	pass



while game_date != end_date:
	games_dict = {}
	url = url_pattern % (game_date.month, game_date.day, game_date.year)
	print url
	html = requests.get(url)
	soup = bsoup(html.text, 'html.parser')
	game_tbls = soup.findAll('table', {'class' : game_tbl_class})
	for game in game_tbls:
		game_dict = {}
		gm_tms = get_teams_from_game_tbl(game)
		game_dict['visitor'] = gm_tms[0]
		game_dict['home'] = gm_tms[1]
		gm_url = game.find('td', {'class' : url_class}).find('a').attrs['href']
		gm_stats = get_game_stats(gm_url)

	game_date = game_date + tdelta




# start_date = start_date + tdelta
