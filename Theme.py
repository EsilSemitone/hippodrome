import json

class Theme():

    _themes = ('Green', 'Dark', 'White')

    def __init__(self, theme = _themes[0]):

        try:
            with open("saves\\config.json", 'r') as f:
                json_file = json.load(f)
                self.theme = json_file['theme']
                self.button = json_file[self.theme]['button']
                self.bc = json_file[self.theme]['bc']
                self.back_text = json_file[self.theme]['back_text']
                self.bc_text_field = json_file[self.theme]['bc_text_field']
        except (FileNotFoundError, json.JSONDecodeError):
            with open("saves\\config.json", 'w') as f:
                json.dump({
            "theme": 'Green',
            'Dark':{
                'bc': '#404040', 
                'button': '#999797',
                'back_text': '#999797',
                'bc_text_field': '#999797'}, 
            'Green':{
                'bc': '#4a898a', 
                'button': "#37AA37",
                'back_text': '#000000',
                'bc_text_field': '#314545'}, 
            'White':{
                'bc': '#948788', 
                'button': '#5e5354',
                'back_text': '#948788',
                'bc_text_field': '#5e5354'},
            }, f, indent=2)
        finally:
            with open("saves\\config.json", 'r') as f:
                json_file = json.load(f)
                self.theme = json_file['theme']
                self.button = json_file[self.theme]['button']
                self.bc = json_file[self.theme]['bc']
                self.back_text = json_file[self.theme]['back_text']
                self.bc_text_field = json_file[self.theme]['bc_text_field']

    def select_theme(self, theme : str) -> None:
        #Меняем тему
        if theme in self._themes:
            with open('saves\\config.json', 'r') as f:
                json_file = json.load(f)
                json_file['theme'] = theme
            with open('saves\\config.json', 'w') as f:
                json.dump(json_file, f, indent=2)

    def get_theme(self) -> tuple:
        #Что-то забыл зачем его написал, может вспомню
        return self._themes


if __name__ == "__main__":
   with open("saves\\config.json", 'w') as f:
                json.dump({
            "theme": 'Green',
            'Dark':{
                'bc': '#404040', 
                'button': '#999797',
                'back_text': '#999797',
                'bc_text_field': '#999797'}, 
            'Green':{
                'bc': '#4a898a', 
                'button': "#37AA37",
                'back_text': '#000000',
                'bc_text_field': '#314545'}, 
            'White':{
                'bc': '#948788', 
                'button': '#5e5354',
                'back_text': '#948788',
                'bc_text_field': '#5e5354'},
            }, f, indent=2)
    #test