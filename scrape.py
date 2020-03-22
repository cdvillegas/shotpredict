""" Scrape

This file contains functions related to the scraping of play-
by-play data from basketball-reference.com

This file requires that `pandas` and 'bs4' be installed within the 
Python environment you are running this script in.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import util
import sys


url = 'https://www.basketball-reference.com'


def scrape(pid, yid='', export=False):
	""" Scrapes and parses play by play data for player 
	associated with player_id and, optionally, by season
	
	Parameters
    ----------
    pid : str
        The player ID assigned by basketball-reference.com

    yid : str (optional)
        The year ID for a specific season
        Example: yid for 2019/20 season is '2020'

    Returns
    -------
    DataFrame
        A data frame containing play by play data for player
        corresponding to pid
    """

	href = '/play-index/shot_finder.cgi?request=1&match=play&player_id=' + pid + '&year_id=' + yid
	href += '&order_by=date_game'
	html = requests.get(url + href)
	soup = BeautifulSoup(html.content, 'html.parser')

	# Print retrieval info
	name = soup.find('div', id='pi').find('h1').getText().split(' ')[:2]
	season =  'all seasons' if yid == '' else 'the ' + str(int(yid) - 1) + '/' + yid + ' season'
	print('Retrieving data for ' + ' '.join(name) + " from " + season)

	# Collect tables
	tables = util.collect_tables(url, soup)

	# Create data frame
	df = pd.DataFrame(util.data(tables))
	df.columns = ['home', 'distance', 'type', 'assisted', 'result']

	# Export if needed
	if export:
		df.to_csv('data/' + pid + yid + '.csv')
	
	return df


def search(query):
	""" Searches for players by query
	
	Parameters
    ----------
    query : str
        The query entered by the user

    Returns
    -------
    list : (str, str)
    	A list of tuples of the form (name, pid), 
    	name being the name of the player and pid
    	being the corresponding player ID assigned by 
    	basketball-reference.com
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


def seasons(pid):
	""" Lists all seasons played by a player

	Parameters
    ----------
    pid : str
        The player ID assigned by basketball-reference.com

    Returns
    -------
    list
        A list of year IDs corresponding to seasons
    """

	href = '/play-index/shot_finder.cgi?&player_id=' + pid
	html = requests.get(url + href)
	soup = BeautifulSoup(html.content, 'html.parser')
	seasons = [(item['value'], item.getText()) for item in soup.find('select').findAll('option')]
	
	return seasons


if __name__ == '__main__':
	print(search('brandon i'))
	lonzo = scrape('ingrabr01', '', export=True)

