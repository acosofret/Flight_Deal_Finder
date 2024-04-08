import requests

class FlightSearch: #This class is responsible for talking to the Flight Search API.
    def get_iata_code(self, destination, TEQUILA_ENDPOINT, TEQUILA_API_KEY):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {
            "apikey" : TEQUILA_API_KEY
        }
        parameters = {
            "term" : destination,
            "location_types" : "city"
        }
        response = requests.get(url=location_endpoint, headers=headers, params=parameters)
        result = response.json()["locations"]
        code = result[0]["code"]
        print(code)

test = FlightSearch()

my_test = test.get_iata_code(destination="Dubai", TEQUILA_ENDPOINT="https://api.tequile.kiwi.com/", TEQUILA_API_KEY="T7XnOp4vAX-DnIZbIBPQk73hviTLeSqy")