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

def data(player_url):
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

    html = requests.get(player_url)
	soup = BeautifulSoup(html.content, 'html.parser')


def search(query):
	""" Searches for players by query
	
	Parameters
    ----------
    query : str
        The query entered by the user

    Returns
    -------
    list : (str, str)
        
    """

	html = requests.get(url + '/search/search.fcgi?search=' + query)
	soup = BeautifulSoup(html.content, 'html.parser')

	if not soup.find('strong', text='Search Results'):
		# If automatically redirects, return current url
		name = soup.find('h1', itemprop="name").getText()
		href = url + soup.find('a', text=name + ' Overview').get('href')

		return [(name, href)]
	else:
		# If returns a list, parse it
		items = soup.findAll('div', {"class": "search-item"})
		name = lambda s: s.find('a').getText()
		href = lambda s: s.find('a').get('href')
		players = [(name(item), url + href(item)) for item in items if 'players' in href(item)]

		return players


if __name__ == '__main__':
	print(search('lebron'))

	