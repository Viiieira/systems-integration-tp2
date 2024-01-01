import xml.etree.ElementTree as ET

from entities.wine import Wine

class Winery:

    def __init__(self, name, province):
        Winery.counter += 1
        self._id = Winery.counter
        self._name = name
        self._province = province

    def to_xml(self):
        el = ET.Element("Winery")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("province_ref", str(self._province.get_id()))

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id:{self._id}"

Winery.counter = 0
