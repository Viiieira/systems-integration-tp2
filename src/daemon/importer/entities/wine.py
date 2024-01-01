import xml.etree.ElementTree as ET

class Wine:

    def __init__(self, name, points, price, variety, province, taster, winery):
        Wine.counter += 1
        self._id = Wine.counter
        self._name = name
        self._points = points
        self._price = price
        self._variety = variety
        self._province = province
        self._taster = taster
        self._winery = winery

    def to_xml(self):
        el = ET.Element("Wine")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("points", self._points)
        el.set("price", self._price)
        el.set("variety", self._variety)
        el.set("province_ref", str(self._province.get_id()))
        el.set("taster_ref", str(self._taster.get_id()))
        el.set("winery_ref", str(self._winery.get_id()))

        return el

    def __str__(self):
        return f"{self._name}, points:{self._points}, price:{self._price}, variety:{self._variety}"

Wine.counter = 0