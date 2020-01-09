""" Player Shot Scraper

This script scrapes play by play shot data from basketball-reference.com
and exports it as `shots.csv`

This script requires that `pandas` and 'bs4' be installed within the 
Python environment you are running this script in.

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

import sys
reload(sys)
sys.setdefaultencoding('utf8')


url = 'https://www.basketball-reference.com'

def data(player_id, year=''):
	""" Scrapes, parses, and exports play by play data
	for player associated with player_url
	
	Parameters
    ----------
    query : str
        The user query

    Returns
    -------
    DataFrame
        A data frame containing play by play data
    """

	href = '/play-index/shot_finder.cgi?request=1&match=play&player_id=' + player_id + '&year_id=' + year
	href += '&order_by=date_game'
	html = requests.get(url + href)
	soup = BeautifulSoup(html.content, 'html.parser')
	table = pd.read_html(soup.find('table').encode('utf-8'))[0].iloc[2:, :]
	table.columns = ['rk', 'player', 'date', 'team', '1', 'opp', '2', 'qtr', 'time', 'result', 'description']
	table = table.drop(columns=['rk', 'date', 'team', '1', 'opp', '2'])
	table = table[table['description'] != 'Description']
	print(table.columns)
	# while soup.find('a', text='Next page'):
		
def table(player_id, year=''):
	
	
def seasons(player_id):
	href = '/play-index/shot_finder.cgi?&player_id=' + player_id
	html = requests.get(url + href)
	soup = BeautifulSoup(html.content, 'html.parser')
	seasons = [(item['value'], item.getText()) for item in soup.find('select').findAll('option')]
	
	return seasons


def search(query):
	""" Searches for players by query
	
	Parameters
    ----------
    query : str
        The query entered by the user

    Returns
    -------
    list : (str, str)
    	A list of tuples of the form (name, href), 
    	name being the name of the player and href
    	being the full url of that player's page 
    """

	html = requests.get(url + '/search/search.fcgi?search=' + query)
	soup = BeautifulSoup(html.content, 'html.parser')

	if not soup.find('strong', text='Search Results'):
		# If automatically redirects, return current url
		name = soup.find('h1', itemprop="name").getText()
		href = url + soup.find('a', text=name + ' Overview').get('href')
		player_id = href.split("/")[-1].split('.')[0]

		return [(name, player_id)]
	else:
		# Parse each returned player
		items = soup.findAll('div', {"class": "search-item"})
		name = lambda s: s.find('a').getText()
		href = lambda s: s.find('a').get('href')
		player_id = lambda s: s.split("/")[-1].split('.')[0]
		players = [(name(item), player_id(href(item))) for item in items if 'players' in href(item)]

		return players


def player_id(href):
	'https://www.basketball-reference.com/play-index/shot_finder.cgi?request=1&match=play&player_id=artesro01&order_by=date_game'

if __name__ == '__main__':
	data('crawfja01', '2019')

	