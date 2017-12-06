
import os
import argparse
import time
import requests
from bs4 import BeautifulSoup as bsoup
from funcs import *

# URL = "http://www.sports-reference.com/cbb/seasons/2017-ratings.html"
URL = "http://www.sports-reference.com/cbb/seasons/{yyyy}-ratings.html"
WRITE_DIR_FMT = './data'
WRITE_FILE_FMT = 'teams{yyyy}.csv'

def get_ratings_table(soup):
  tbl = soup.find('table', {'id' : 'ratings'})
  return tbl

def filter_rows_for_non_header(rows):
  rows = [row for row in rows if row.attrs.get('class') is None]
  return rows

def get_team_name_and_abbrev(row):
  cell = row.find('td', {'data-stat' : 'school_name'})
  school_name = cell.text.strip()
  abbrev = cell.find('a').attrs.get('href').split('/')[3]
  return school_name, abbrev


def get_schools(args):
  html = get_html(URL.format(yyyy = args.year))
  soup = soupify_html(html)
  tbl = get_table_by_id(soup, 'ratings')
  rows = get_table_body_rows(tbl)
  rows = filter_rows_for_non_header(rows)
  schools = [get_team_name_and_abbrev(row) for row in rows]

  writedir = create_dir_if_not_exists(WRITE_DIR_FMT)
  writefile = WRITE_FILE_FMT.format(yyyy = args.year)
  writepath = os.path.join(writedir, writefile)
  write_to_file(schools, writepath, headers = ['school_name', 'school_abbrev'])
  print 'This is done.'


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='')
  # parser.add_argument('-y', action='store', dest = 'year', required = True)
  parser.add_argument('-y', action='store', dest = 'year')
  # parser.add_argument('-w', action='store', dest = 'writefile')
  args = parser.parse_args()

  for yr in range(2002, 2016):
    print yr
    args.year = yr
    get_schools(args)

