﻿from random import randint, choice
import json as js

class Weather(object):

    #Класс погоды
    states = {
        1 : "Ясно, на небе не тучки",
        2 : "Облачно",
        3 : "Дождь такая себе погодка",
        4 : "Гроза, может это знак?"
        }

    state = None 

    def __init__(self) -> None:
        self.state = self.states[randint(1, 4)]

    def update(self) -> None:
        self.state = self.states[randint(1, 4)]

    def get_state(self) -> str:
        return self.state

    def impact_on_speed(self) -> list:
        #Как погода будет влиять на скорость
        if self.state == self.states[1]:
            return [0.3, 0.4, 0.5]
        elif self.state == self.states[2]:
            return [0, 0.1, 0.2]
        elif self.state == self.states[3]:
            return [-0.1, -0.2, -0.3]
        elif self.state == self.states[4]:
            return [-0.2, -0.3, -0.4]

    def impact_on_problem(self) -> int:
        #Как погода будет влиять на проблемы
        if self.state == self.states[1]:
            return choice([10, 8, 5])
        elif self.state == self.states[2]:
            return choice([15, 12, 8])
        elif self.state == self.states[3]:
            return choice([17, 14, 3])
        elif self.state == self.states[4]:
            return choice([18, 15, 4])


class Time(Weather):
    #Время суток
    states = {
        1: "Утро",
        2: 'День',
        3: 'Вечер',
        4: 'Ночь'
        }

    def __init__(self) -> None:
        super().__init__()

    def impact_on_speed(self) -> list:
        #Как будет влиять на скорость
        if self.state == self.states[1]:
            return [0.3, 0.4]
        elif self.state == self.states[2]:
            return [0, 0.1]
        elif self.state == self.states[3]:
            return [0, -0.1]
        elif self.state == self.states[4]:
            return [-0.2, -0.3, -0.4]

    def impact_on_problem(self) -> int:
        #Какбудет влиять на проблемы
        if self.state == self.states[1]:
            return choice([10, 8, 5])
        elif self.state == self.states[2]:
            return choice([15, 12, 8]) 
        elif self.state == self.states[3]:
            return choice([17, 14, 3])
        elif self.state == self.states[4]:
            return choice([18, 15, 4])


class EventRate():
    #Частота событий\проблем во время забега
    _events = ("Often", "Normal", "Rarely")

    def __init__(self) -> None:
        self.checkout()
        
    def checkout(self) -> None:
        '''Чтение файла, если ошибка, то создадим))'''
        try:
            with open('saves\\event.json', 'r') as f:
                json_file = js.load(f)                

        except (FileNotFoundError, js.JSONDecodeError):
            with open('saves\\event.json', 'w') as f:
                js.dump({
                    'rate': "Normal",
                    'Often': -40,
                    'Normal': 0,
                    "Rarely": 40
                    }, f, indent=2)
        finally:
            with open('saves\\event.json', 'r') as f:
                json_file = js.load(f)
                self.ev_rate = json_file['rate']
                self.impact = json_file[self.ev_rate]

    def write_new(self, value: str) -> None:
        """Перезапись в файл и повторное чтение для перезаписи атрибутов"""
        with open('saves\\event.json', 'r') as f:
            json_file = js.load(f)
            json_file['rate'] = value
        with open('saves\\event.json', 'w') as f:
            js.dump(json_file, f, indent=2)
        self.checkout()

    def get(self) -> tuple:
        return self._events

if __name__ == "__main__":
    with open('saves\\event.json', 'w') as f:
                js.dump({
                    'rate': "Normal",
                    'Often': -40,
                    'Normal': 0,
                    "Rarely": 40
                    }, f, indent=2)