from random import randint, choice
import json as js
from textwrap import indent
class Weather(object):

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
        if self.state == self.states[1]:
            return [0.3, 0.4, 0.5]
        elif self.state == self.states[2]:
            return [0, 0.1, 0.2]
        elif self.state == self.states[3]:
            return [-0.1, -0.2, -0.3]
        elif self.state == self.states[4]:
            return [-0.2, -0.3, -0.4]

    def impact_on_problem(self) -> int:
        if self.state == self.states[1]:
            return choice([10, 8, 5])
        elif self.state == self.states[2]:
            return choice([15, 12, 8])
        elif self.state == self.states[3]:
            return choice([17, 14, 3])
        elif self.state == self.states[4]:
            return choice([18, 15, 4])


class Time(Weather):

    states = {
        1: "Утро",
        2: 'День',
        3: 'Вечер',
        4: 'Ночь'
        }

    def __init__(self) -> None:
        super().__init__()

    def impact_on_speed(self) -> list:
        if self.state == self.states[1]:
            return [0.3, 0.4]
        elif self.state == self.states[2]:
            return [0, 0.1]
        elif self.state == self.states[3]:
            return [0, -0.1]
        elif self.state == self.states[4]:
            return [-0.2, -0.3, -0.4]

    def impact_on_problem(self) -> int:
        if self.state == self.states[1]:
            return choice([10, 8, 5])
        elif self.state == self.states[2]:
            return choice([15, 12, 8]) 
        elif self.state == self.states[3]:
            return choice([17, 14, 3])
        elif self.state == self.states[4]:
            return choice([18, 15, 4])


class EventRate():

    _events = ("Often", "Normal", "Rarely")
    def __init__(self, ev_rate = _events[1]) -> None:
        try:
            with open('saves\\event.json', 'r') as f:
                json_file = js.load(f)
                self.ev_rate = json_file['rate']
                self.impact = json_file[self.ev_rate]

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

if __name__ == "__main__":
    with open('saves\\event.json', 'w') as f:
                js.dump({
                    'rate': "Normal",
                    'Often': -40,
                    'Normal': 0,
                    "Rarely": 40
                    }, f, indent=2)