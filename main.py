#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests
from my_vars import *
from pprint import pprint # to see the json() data formatted nicely
from flight_search import FlightSearch
from data_manager import *

# test the sheety api connection:

SHEETY_ENDPOINT = my_sheety_endpoint # saved in my_vars file, under .gitignore;

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
		location["iataCode"] = iata_code_search.get_iata_code(location["city"])
		# At this point, our code checks if "IATA code" cell is empty and it tells what value should it be.
		# Now we get the code (thru the data_manager module) to update this new value on the spreadsheet:
		row_edit_endpoint = f"{SHEETY_ENDPOINT}/{location["id"]}"
		new_data = {
			"price": {
				"iataCode": location["iataCode"]
			}
		}
		iata_code_update = DataManager(location).update_iata_codes(update_endpoint=row_edit_endpoint, new_data=new_data)

# At this stage out code checks if IATA code" cell is empty and corrects it with a testing "TEST" value.
# Next we get the IATA Codes using the Kiwi Partners API

