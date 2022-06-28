import json


class Cities:
    def __init__(self, filename):
        self.cities_dict = json.loads(open(filename, "r", encoding="UTF-8").read())

    def get_cities(self):
        cities = []
        for item in self.cities_dict:
            cities.append(item["city"])
        return cities


