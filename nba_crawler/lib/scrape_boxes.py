import os
import time
import numpy as np
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
from GameBoxScraper import GameBoxScraper


GAMES_DIR = '/Users/csheehan/Documents/projects/nba/data'
GAMES_FILE = 'games_%s.txt'

BOX_DIR = '/Users/csheehan/Documents/projects/nba/data/boxes/'

YEARS = [2013,2014,2015,2016,2017]

def get_games(yr):
	filename = os.path.join(GAMES_DIR, GAMES_FILE % yr)
	csvr = csv.reader(open(filename, 'r'), delimiter = '\t')
	csvr.next()
	games = [row[0].split('/')[-1].replace('.html', '') for row in csvr]
	return games


def main():
	for yr in YEARS[1:]:
		print yr
		games = get_games(yr)
		for game in games:
			# print game,
			box = GameBoxScraper(game)
			stats, adv = box.get_game_stats()
			stats.to_csv(BOX_DIR + '%s.csv' % game, index = False)
			adv.to_csv(BOX_DIR + '%s_adv.csv' % game, index = False)
			time.sleep(1)

if __name__ == '__main__':
	main()