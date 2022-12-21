import json

class Theme():

    _themes = ('Green', 'Dark', 'White')

    def __init__(self, Theme = _themes[0]):

        try:
            with open("saves\\config.json", 'r') as f:
                json_file = json.load(f)
                self.Theme = json_file['Theme']
                