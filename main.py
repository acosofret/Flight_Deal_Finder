#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests
from my_vars import *
from pprint import pprint # to see the json() data formatted nicely
from flight_search import FlightSearch

# test the sheety api connection:

SHEETY_ENDPOINT = my_sheety_endpoint

get_sheet_rows = requests.get(SHEETY_ENDPOINT)
result = get_sheet_rows.json()
destinations_sheet_data = result["prices"]
# First we pass each city name in "destinations_sheet_data" one-by-one to the FlightSearch class (in flight_search module):
# In the FlightSearch class we'll have a function that will return the IATA code for each of the city names
# Then we update the "destinations_sheet_data" to include the IATA code for each Airport/city.
for location in destinations_sheet_data:
	city = location["city"]
	iata_code = FlightSearch(city)
	location["iataCode"] = iata_code

pprint(destinations_sheet_data)