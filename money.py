from tkinter import *
from tkinter import messagebox

class Money():

    def __init__(self, path: str, name):
        self.name = name
        self.money = 0
        self.path = path

    def load(self):
        try:
            with open(self.path, "r") as f:
                self.money = int(f.read())
        except:
            with open(self.path, 'w') as f:
                self.money = 10000
                f.write('10000')

    def save(self):
        try:
            with open(self.path, 'w') as f:
                f.write(str(self.money))
        except:
            messagebox.showinfo('Ошибка', f'Не получается сохранить {Money}')
        