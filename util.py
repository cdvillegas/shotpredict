import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

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

def collect_tables(url, soup):
	progressMessage("Collecting tables", 0)
	tables = []
	while soup.find('a', text='Next page'):
		tables.append(table(soup))

		progressMessage("Collecting tables", len(tables))

		# Update soup object
		href = soup.find('a', text='Next page').get('href')
		html = requests.get(url + href)
		soup = BeautifulSoup(html.content, 'html.parser')
	progressMessage("Collecting tables: Success\n", 0)

	return tables

def data(tables):
	progressMessage("Parsing data", 0)
	data = []
	l = len(tables)
	for i, t in enumerate(tables):
		# Parse table
		data.extend(parse_table(t))
	progressMessage("Parsing tables: Success\n", 0)

	return data

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


def progressMessage(message, num):
    # percent float from 0 to 1. 
    sys.stdout.write('\x1b[2K')
    sys.stdout.write(message + ('.'* (num % 4)) + "\r")