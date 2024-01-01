import xml.etree.ElementTree as ET

from entities.wine import Wine

class Province:

    def __init__(self, name, country):
        Province.counter += 1
        self._id = Province.counter
        self._name = name
        self._wines = []
        self._country = country


    def add_wine(self, wine: Wine):
        self._wines.append(wine)

    def to_xml(self):
        el = ET.Element("Province")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("country_ref", str(self._country.get_id()))


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
