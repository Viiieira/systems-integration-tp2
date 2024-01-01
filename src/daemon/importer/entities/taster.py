import xml.etree.ElementTree as ET


class Taster:

    def __init__(self, name, twitter_handle):
        Taster.counter += 1
        self._id =  Taster.counter
        self._name = name
        self._twitter_handle = twitter_handle

    def to_xml(self):
        el = ET.Element("Taster")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("twitter_handle", self._twitter_handle)
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name},  twitter_handle:{self._twitter_handle} , id:{self._id}"


Taster.counter = 0
