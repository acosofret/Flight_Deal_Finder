#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests
from my_vars import *
from pprint import pprint # to see the json() data formatted nicely
from flight_search import FlightSearch
from data_manager import *

# test the sheety api connection:

SHEETY_ENDPOINT = my_sheety_endpoint # saved in my_vars file, under .gitignore;
TEQUILA_ENDPOINT = my_tequila_endpoint
TEQUILA_API_KEY = my_tequila_api_key

get_sheet_data = requests.get(url=SHEETY_ENDPOINT)
result = get_sheet_data.json()
destinations_sheet_data = result["prices"]
# pprint(destinations_sheet_data) # for testing only

# First we pass each city name in "destinations_sheet_data" one-by-one to the FlightSearch class (in flight_search module):
# In the FlightSearch class we'll have a function that will return the IATA code for each of the city names
# Then we update the "destinations_sheet_data" to include the IATA code for each Airport/city.
for location in destinations_sheet_data:
	if location["iataCode"] == "":
		iata_code_search = FlightSearch()
		location["iataCode"] = iata_code_search.get_iata_code(destination=location["city"], TEQUILA_ENDPOINT=TEQUILA_ENDPOINT, TEQUILA_API_KEY=TEQUILA_API_KEY)
		# At this point, our code checks if "IATA code" cell is empty and it tells what value should it be.
		# Now we get the code (thru the data_manager module) to update this new value on the spreadsheet:
		row_edit_endpoint = f"{SHEETY_ENDPOINT}/{location["id"]}"
		new_data = {
			"price": {
				"iataCode": location["iataCode"]
			}
		}
		iata_code_update = DataManager(location).update_iata_codes(update_endpoint=row_edit_endpoint, new_data=new_data)

# At this stage out code checks if 'IATA code' cell is empty and corrects it with the right code (getting it from Tequila API by Kiwi.com).
# Next we search for Cheap Flights:
	where_from = "LTN"
	where_to = location["iataCode"]
	from_date = "11/04/2024"
	to_date = "11/04/2024"
	min_length = 1
	max_length = 1
	stops = 0
	currency = "GBP"
	flight_searcher = FlightSearch()
	flights_data = flight_searcher.search_flights(departure=where_from, destination=where_to, date_from=from_date, date_to=to_date, stay_length_from=min_length, stay_length_to=max_length, max_stopovers=stops, currency=currency, TEQUILA_ENDPOINT=my_tequila_endpoint, TEQUILA_API_KEY=my_tequila_api_key)
	#flights = flights_data
	print(type(flights_data))