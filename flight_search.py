import requests

class FlightSearch: #This class is responsible for talking to the Flight Search API.
    def get_iata_code(self, destination, TEQUILA_ENDPOINT, TEQUILA_API_KEY):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {
            "apikey" : TEQUILA_API_KEY
        }
        parameters = {
            "term" : destination,
            #"location_types" : "city"
        }
        response = requests.get(url=location_endpoint, headers=headers, params=parameters)
        response.raise_for_status()
        code = response.json()["locations"][0]["code"]
        return code