
import os
import requests
from bs4 import BeautifulSoup as bs4
from funcs import *
import time

logger = init_logging('./logs/get_rosters.log')
URL = "http://www.sports-reference.com/cbb/schools/{school_abbrev}/{yyyy}.html"

WRITE_DIR_FMT = './data/teams{yyyy}'
WRITE_FILE_FMT = 'players-{school_abbrev}.csv'


def get_player_info(row):
  row_head = row.find('th', {'data-stat' : 'player'})
  playerName = row_head.text
  playerId = row_head.attrs.get('data-append-csv')
  player = {td.attrs.get('data-stat') : td.text.strip() for td in row.findAll('td')}
  player['playerName'] = playerName
  player['playerId'] = playerId
  return player

def height_to_inches(height):
  ft, inches = height.split('-')
  height_inches = int(ft)*12 + int(inches)
  return height_inches

def convert_players_heights_to_inches(players):
  for player in players:
    try:
      player['height'] = height_to_inches(player.get('height'))
    except:
      continue
  return players

def list_of_dicts_to_header_and_lists(list_of_dicts):
  headers = list_of_dicts[0].keys()
  lists = []
  for record in list_of_dicts:
    lists.append([record.get(column) for column in headers])
  return headers, lists

def get_team_roster(school_abbrev, year):
  writedir = create_dir_if_not_exists(WRITE_DIR_FMT.format(yyyy = year))
  writefile = WRITE_FILE_FMT.format(school_abbrev = school_abbrev)
  writepath = os.path.join(writedir, writefile)

  try:
    url = URL.format(school_abbrev = school_abbrev, yyyy = year)
  except requests.ConnectionError:
    url = URL.format(school_abbrev = school_abbrev, yyyy = year)
  html = get_html(url)
  soup = soupify_html(html)
  tbl = get_table_by_id(soup, 'roster')
  rows = get_table_body_rows(tbl)

  players = convert_players_heights_to_inches([get_player_info(row) for row in rows])
  headers, players = list_of_dicts_to_header_and_lists(players)

  write_to_file(players, writepath, headers = headers, sep = '\t') 
  logger.info('%s rows written to %s.' % (len(players), writefile))

def get_all_rosters(args):
  teams = load_teams(args.year)
  for team, school_abbrev in teams:
    print team
    logger.info(team)
    get_team_roster(school_abbrev, args.year)
    time.sleep(1)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='')
  parser.add_argument('-y', action='store', dest = 'year')
  args = parser.parse_args()


  for yr in range(2007, 2016):
    print yr
    args.year = yr
    get_all_rosters(args)
