""" Player Shot Scraper

This script scrapes play by play shot data from basketball-reference.com
and exports it as `shots.csv`

This script requires that `pandas` and 'bs4' be installed within the 
Python environment you are running this script in.

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.basketball-reference.com'

def data(pid, yid=''):
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

	# Print player name
	name = soup.find('div', id='pi').find('h1').getText().split(' ')[:2]
	print('Retrieving data for ' + ' '.join(name))

	data = []
	count = 1

	while soup.find('a', text='Next page'):
		print('Parsing page ' + str(count))
		# Get table
		t = table(soup)

		# Parse table
		data.extend(parse_table(t))

		# Update soup object
		href = soup.find('a', text='Next page').get('href')
		html = requests.get(url + href)
		soup = BeautifulSoup(html.content, 'html.parser')
		count += 1

	print('')
	df = pd.DataFrame(data)
	df.columns = ['home', 'distance', 'type', 'assisted', 'result']
	
	return df
			

def table(soup):
	""" Extracts raw table from shot finder

	Parameters
    ----------
    soup : BeautifulSoup
        A soup object for the shot finder page

    Returns
    -------
    DataFrame
        The raw table from the page
    """

	table = pd.read_html(soup.find('table').encode('utf-8'))[0].iloc[2:, :]
	table.columns = ['rk', 'player', 'date', 'team', 'home', 'opp', ' ', 'qtr', 'time', 'result', 'description']
	table = table.drop(columns=['rk', 'date', 'team', 'opp', ' ', 'qtr', 'time'])
	table = table[table['description'] != 'Description']

	return table


def parse_table(table):
	""" Parses and organizes data table, appending
	description data as well

	Parameters
    ----------
    table : DataFrame
        A data frame containing raw table from a 
        page

    Returns
    -------
    list : list
        A list of data rows
    """
	data = []
	for item in table.values.tolist():
		home = 0 if item[1] == '@' else 1
		result = item[2]
		data.append([home] + parse_description(item[-1]) )
	return data


def parse_description(desc):
	""" Parses a play by play description into a list of data

	Parameters
    ----------
    desc : str
        A sentence describing a shot taken

    Returns
    -------
    list
        A list of play by play data (shot_distance, 
        shot_type, assisted, result)
    """

	# Split on makes or misses
	if 'makes' in desc:
		result = 1
		split = desc.split(' makes ')
	elif 'misses' in desc:
		result = 0
		split = desc.split(' misses ')
	

	# Get player name
	name = split[0]
	desc = split[1]

	# Get shot type and distance
	if 'from' in desc:
		split = desc.split(' from ')
		shot_type = split[0]
		split = split[1].split(' ft')
		shot_distance = int(split[0])
	else:
		split = desc.split(' at ')
		shot_type = split[0]
		shot_distance = 0
	
	# Get assist
	assisted = 1 if 'assist' in desc else 0
	return [shot_distance, shot_type, assisted, result]



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


if __name__ == '__main__':
	lebron = data('jamesle01', '2020')
	harden = data('hardeja01', '2020')
	ball = data('balllo01', '2020')
	print(ball['result'])


	