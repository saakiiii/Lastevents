import json

class CountriesStatesCities:

    def __init__(self) -> None:
        with open("/home/forlanching/mysite/NewFolder/c+s.json", 'r') as file:
        # with open("c+s.json", 'r') as file:
            self.val = json.loads(file.read())

    def getCountries(self):
        return [x["country"] for x in self.val["countries"]]

    def getStatesByCountry(self, country):
        for i in self.val["countries"]:
           if i["country"] == country:
              return i["states"]