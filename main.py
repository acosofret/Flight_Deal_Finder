#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests
from my_vars import *
from pprint import pprint # to see the json() data formatted nicely
from flight_search import FlightSearch
from data_manager import *
from datetime import datetime, timedelta
from notification_manager import NotificationManager
from customers import NewCustomer

# test the sheety api connection:

SHEETY_ENDPOINT = my_sheety_endpoint # saved in my_vars file, under .gitignore;
TEQUILA_ENDPOINT = my_tequila_endpoint
TEQUILA_API_KEY = my_tequila_api_key
TWILIO_ENDPOINT = "https://api.twilio.com/2010-04-01"
TWILIO_ACC_SID = my_twilio_acc_sid
TWILIO_AUTH_TOKEN = my_twilio_auth_token
MY_PHONE_NUMBER = my_phone_number
MY_TWILIO_NUMBER = my_twilio_number # this twilio number has limited usage, unless account is upgraded

# Sign up new users:
new_user = NewCustomer()
new_user_signed = new_user.add_new_user(update_endpoint= my_users_spreadsheet, new_data=new_user.user_data)

# Chech the destinations spredsheet and Update IATA codes for flight search purposes
get_sheet_data = requests.get(url=SHEETY_ENDPOINT)
result = get_sheet_data.json()
destinations_sheet_data = result["prices"]
# pprint(destinations_sheet_data) # for testing only

# First we pass each city name in "destinations_sheet_data" one-by-one to the FlightSearch class (in flight_search module):
# In the FlightSearch class we'll have a function that will return the IATA code for each of the city names
# Then we update the "destinations_sheet_data" to include the IATA code for each Airport/city.
message = ""
for location in destinations_sheet_data:
	budget = location["lowestPrice"]
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
	where_from = "LTN" # this is the selected departure airport. can be improved to allow multiple choices & user input.
	where_to = location["iataCode"]
	from_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y") # we use .strftime method to convert it as required by Tequila API
	to_date = (datetime.now() + timedelta(days=180)).strftime("%d/%m/%Y")
	min_length = 4
	max_length = 7
	stops = 0
	currency = "GBP"
	flight_searcher = FlightSearch()
	flights_data = flight_searcher.search_flights(departure=where_from, destination=where_to, date_from=from_date, date_to=to_date, stay_length_from=min_length, stay_length_to=max_length, max_stopovers=stops, currency=currency, budget=budget,TEQUILA_ENDPOINT=my_tequila_endpoint, TEQUILA_API_KEY=my_tequila_api_key)

	if len(flights_data) == 0 :
		message += f"\n{location["city"]}: No flights within budgets yet.\n"
	else:
		for flight in flights_data:
			message += f"\n{flight["cityTo"]} Price Alert !!!\nFrom {flight["cityFrom"]} {flight["flyFrom"]} to {flight["cityTo"]} {flight["flyTo"]} for ONLY £{flight["price"]} !!!\nDeparture: {flight["local_departure"].split("T")[0]}, at {(flight["local_departure"].split("T")[1]).split(".")[0]}\nReturn: {flight["route"][1]["local_arrival"].split("T")[0]}, at {(flight["route"][1]["local_arrival"].split("T")[1]).split(".")[0]}\n (To include long links requires upgrade" #Seats going fast !!! Reserve yours now: {flight["deep_link"]}\n"
# print(message) # For testing only
# #Now that we got the right response in the 'message' variable(tested  through "print" function), we send it via SMS:
# notification = NotificationManager()
# notification.send_sms_notification(message_body=message)



