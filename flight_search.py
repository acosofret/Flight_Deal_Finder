import requests
from flight_data import FlightData


class FlightSearch: #This class is responsible for talking to the Flight Search API.
    def get_iata_code(self, destination, TEQUILA_ENDPOINT, TEQUILA_API_KEY):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {
            "apikey" : TEQUILA_API_KEY
        }
        parameters = {
            "term" : destination,
        }
        response = requests.get(url=location_endpoint, headers=headers, params=parameters)
        response.raise_for_status()
        code = response.json()["locations"][0]["code"]
        return code

    def search_flights(self, departure, destination, date_from, date_to, stay_length_from, stay_length_to, max_stopovers, currency, TEQUILA_ENDPOINT, TEQUILA_API_KEY):
        flight_search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {
            "apikey": TEQUILA_API_KEY
        }

        parameters = {
            "fly_from": departure,
            "fly_to" : destination,
            "date_from" : date_from,
            "date_to" : date_to,
            "nights_in_dst_from" : stay_length_from,
            "nights_in_dst_to" : stay_length_to,
            "max_stopovers" : max_stopovers,
            "curr" : currency,
        }

        response = requests.get(url=flight_search_endpoint, headers=headers, params=parameters)
        try:
            result = response.json()["data"][0]
        except IndexError:
            print(f"No flights available for {destination}")
            return None
        flight_data = FlightData(
            price=result["price"],
            origin_city=result["route"][0]["cityFrom"],
            origin_airport=result["route"][0]["flyFrom"],
            destination_city=result["route"][0]["cityTo"],
            destination_airport=result["route"][0]["flyTo"],
            out_date=result["route"][0]["local_departure"].split("T")[0],
            return_date=result["route"][1]["local_departure"].split("T")[0],
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data