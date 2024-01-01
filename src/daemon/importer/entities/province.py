import xml.etree.ElementTree as ET

import json
import urllib.parse
import urllib.request

from entities.wine import Wine

class Province:

    def __init__(self, name, country):
        Province.counter += 1
        self._id = Province.counter
        self._name = name
        self._wines = []
        self._country = country
        self._latitude = None
        self._longitude = None
        self.fetch_coordinates()

    def fetch_coordinates(self):
        # Use Nominatim API to fetch coordinates for the country
        endpoint = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": self._name,
            "format": "json",
            "limit": 1,
        }
        url = f"{endpoint}?{urllib.parse.urlencode(params)}"

        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            if data:
                location = data[0]
                self._latitude = float(location.get("lat"))
                self._longitude = float(location.get("lon"))

    def add_wine(self, wine: Wine):
        self._wines.append(wine)

    def to_xml(self):
        el = ET.Element("Province")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("country_ref", str(self._country.get_id()))
        el.set("latitude", str(self._latitude))
        el.set("longitude", str(self._longitude))


        wines_el = ET.Element("Wines")
        for wine in self._wines:
            wines_el.append(wine.to_xml())

        el.append(wines_el)

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"


Province.counter = 0
