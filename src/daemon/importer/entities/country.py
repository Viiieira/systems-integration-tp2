import xml.etree.ElementTree as ET

from entities.province import Province

class Country:

    def __init__(self, name):
        Country.counter += 1
        self._id = Country.counter
        self._name = name
        self._provinces = []

    def add_province(self, province: Province):
        self._provinces.append(province)

    def to_xml(self):
        el = ET.Element("Country")
        el.set("id", str(self._id))
        el.set("name", self._name)

        provinces_el = ET.Element("Provinces")
        for province in self._provinces:
            provinces_el.append(province.to_xml())

        el.append(provinces_el)

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"


Country.counter = 0
