from mycroft import MycroftSkill, intent_file_handler


class WhatFreeWords(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('words.free.what.intent')
    def handle_words_free_what(self, message):
        self.speak_dialog('words.free.what')


def create_skill():
    return WhatFreeWords()

