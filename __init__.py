from mycroft import MycroftSkill, intent_file_handler
from mycroft.configuration import Configuration as config
from whatfreewords import WhatFreeWords as WFW
import maidenhead as mh

class WhatFreeWords(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.wfw = None

    def initialize(self):
        self.wfw = WFW()
        #self.wfw.latlon2words(37.234332, -115.806657) # == "joyful.nail.harmonica"
        #self.wfw.words2latlon("joyful.nail.harmonica") # == [37.234328, -115.806657]

    @intent_file_handler('maidenhead.location.intent')
    def handle_maidenhead_location(self, message):
        lon = config.get()['location']['coordinate']['longitude']
        lat = config.get()['location']['coordinate']['latitude']
        if lon and lat:
            self.log.debug("lon: {} lat: {}".format(lon, lat))
            mhl = mh.toMaiden(lat, lon,precision=4)

            self.speak_dialog("maidenhead.locator",{"mhl": self._letterize(mhl)})
        else:
            self.speak_dialog("error")

    @intent_file_handler('coordinates.from.words.intent')
    def handle_coords_from_words(self, message):
        w1 = w2 = w3 = None
        if message.data.get("w1"):
            w1 = message.data.get("w1").lower()
        if message.data.get("w2"):
            w2 = message.data.get("w2").lower()
        if message.data.get("w3"):
            w3 = message.data.get("w3").lower()

        if w1 and w2 and w3:
            latlon = self.wfw.words2latlon("{}.{}.{}",format(w1, w2, w3))
            self.speak_dialog('coordinates', {"lat": latlon[0], "lon": latlon[1]})

    @intent_file_handler('words.from.coordinates.intent')
    def handle_words_from_coordinates(self, message):
        self.speak_dialog('words.free.what')

    @intent_file_handler('what.free.words.intent')
    def handle_what_free_words(self, message):
        lon = config.get()['location']['coordinate']['longitude']
        lat = config.get()['location']['coordinate']['latitude']
        if lon and lat:
            self.log.debug("lon: {} lat: {}".format(lon, lat))
            my_free_words = self.wfw.latlon2words(lat, lon)
            self.speak_dialog("words",{"words": my_free_words})
        else:
            self.speak_dialog("error")

    def _letterize(self, s = ""):
        if s:
            s = " ".join(s[i:i+1] for i in range(0, len(s), 1))
        return s

def create_skill():
    return WhatFreeWords()

