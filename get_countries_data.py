import requests
import json
import hashlib
import pandas as pd
import time
import sqlite3
import pymongo

def get_all_regions():

	api_url = 'https://restcountries-v1.p.rapidapi.com/all'
	headers = {'Content-Type': 'application/json',"x-rapidapi-host": "restcountries-v1.p.rapidapi.com","x-rapidapi-key": "307a7442ddmshb24684e1e1177e1p1502d5jsn926cbeefd02d"}
	response = requests.request("GET", api_url, headers=headers)

	if response.status_code == 200:

		all_countries = json.loads(response.text)
		region_list = []
		i = 0

		for i in range(len(all_countries)):
			region = json.loads(response.text)[i].get('region')
			
			if region != '':
				region_list.append(region.lower())
		
		return list(set(region_list))

	else:
		return None


def get_country_by_region(region, given):

	api_url = 'https://restcountries.eu/rest/v2/region/'+region
	response = requests.request("GET", api_url)

	if response.status_code == 200:

		all_countries_by_region = json.loads(response.text)
		i = 0

		for i in range(len(all_countries_by_region)):
			country = json.loads(response.text)[i]

			if country.get('name') != '' and country.get('name') == given:
				return country
	else:
		return None


def json_factory(cursor, row):

	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d