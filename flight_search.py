class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self, destination):
        self.destination = destination # this will be used as city name to get the right IATA code
        self.code = "No_IATA_code_yet" # this will be the IATA code returned in one of the functions below:(function not added yet)
    def __repr__(self):
        #grab code from relevant endpoint
        return repr(self.code)

