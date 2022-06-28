import json


class Cities:
    def __init__(self, filename):
        self.cities_dict = json.loads(open(filename, "r", encoding="UTF-8").read())
        self.cities = self.get_cities()

    def get_cities(self):
        cities = set()
        for item in self.cities_dict:
            cities.add(item["city"])
        return cities


