# -*- coding: utf-8 -*-
import json
import click
import requests
from blessings import Terminal
from terminaltables import AsciiTable

config = dict()

def read_config(config_file_path):
	"""
	Function is used to read config file into config dictionary
	"""
	global config
	config = json.loads(open(config_file_path).read())

def get_events(city):
	"""
	This method is used to get list of evens for a given city
	"""
	results = []

	#Prams for Meetup
	# City ID: 1018090
	# Category ID for Tech: 34
	# Category ID for Career & Business: 2
	URL = "https://api.meetup.com/2/concierge?offset=0&city=%s&format=json&category_id=34&photo-host=public&page=500&sign=true&key=%s&raduis=100" % (city, config.get('meetup_api_key'))
	
	response = requests.get(URL)

	if response.status_code == 200:
		data = json.loads(response.text)
		for event in data['results']:
			record = []

			record.append(event['group']['name'])
			if 'venue' in event and 'name' in event['venue']:
				record.append(event['venue']['name'])

			if 'venue' in event and 'address_1' in event['venue']:
				record.append(event['venue']['address_1'])

			record.append(event['event_url'])
			results.append(record)

	return results

@click.command()
@click.option('--city', default='mumbai', help='City from where you want to see events of')
def show_events(city):
	events = [['Group Name', 'Venue Name','Address', 'URL']] + get_events(city)
	
	terminal = Terminal()
	print "Showing events from city:", terminal.bold(city)
	
	event_table = AsciiTable(events)
	print event_table.table

if __name__ == "__main__":
	read_config('config.json')
	show_events()