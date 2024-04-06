import requests

class DataManager:
    def __init__(self, destinations_data):
        self.destination_data = destinations_data

    def update_iata_codes(self, update_endpoint, new_data):
        response = requests.put(url=update_endpoint, json=new_data)
        # if response.status_code == 200:
        #     result = response.json()
        #     print("IATA codes Updated Successfully.")
        # else:
        #     print("Error:", response.status_code)
        # print(response.text)


    #This class is responsible for talking to the Google Sheet.
    pass