import os
import requests
from bs4 import BeautifulSoup
from funcs import *

SAVE_DIR = '/Users/csheehan/Documents/projects/nba/data'
SAVE_AS = 'games_{YYYY}.txt'
URL = 'https://www.basketball-reference.com/leagues/NBA_{YYYY}_games-{mnth}.html'
MONTHS = ("october", "november", "december", "january", "february", "march", "april", "may", "june")


def get_season_month_html(yr, mnth):
	url = URL.format(YYYY = yr, mnth = mnth)
	html = get_html(url)
	return html

def write_season(yr, game_records):
	headers = ['url', 
			   'game_start_time',
			   'home_team_name', 
			   'home_team_score', 
			   'visitor_team_name', 
			   'visitor_team_score',
			   'overtime'
			   ]
	save_path = os.path.join(SAVE_DIR, SAVE_AS.format(YYYY = yr))
	with open(save_path, 'w') as f:
		f.write('\t'.join(headers) + '\n')
		for game in game_records:
			row = '\t'.join([game.get(h, '') for h in headers]) + '\n'
			f.write(row)

def main():
	years = [2013,2014,2015,2016,2017]
	for yr in years:
		print yr
		game_records = list()
		for mnth in MONTHS:
			print '--%s' % mnth
			html = get_season_month_html(yr, mnth)
			if not html:
				continue
			soup = soupify_html(html)

			games_tbl = get_table_by_id(soup, 'schedule')
			games = get_table_body_rows(games_tbl)
			games = [row for row in games if 'thead' not in row.attrs.get('class', [])]

			for game in games:
				record = {fld.attrs['data-stat'] : fld.text for fld in game.findAll('td')}
				record['url'] = game.find('td', {'data-stat' : 'box_score_text'}).find('a').attrs['href']
				game_records.append(record)
		write_season(yr, game_records)


if __name__ == '__main__':
	main()