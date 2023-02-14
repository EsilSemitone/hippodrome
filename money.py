from tkinter import Label
from tkinter import messagebox

from Theme import Theme

class Money():

    def __init__(self, name="Рублей"):
        self.th = Theme()
        self.name = name
        self.money = self.load()
        #Проверка на кэш, если нет предупреждение
        assert self.money > 0 , self.error() 
        #Это надпись в левом углу
        self.label = Label(text=f"Осталось {self.money} рублей", bg=self.th.bc, font="arial 16")
        self.label.place(x=20, y=600)

    def __add__(self, other):
        self.money += other
        return self.money

    def __sub__(self, other):
        self.money -= other 
        return self.money

    def load(self) -> int:
        #Функция загрузки денег из файла
        try:
            with open("saves\\money.dat", "r") as f:
                return int(f.read())
            
        except:
            with open("saves\\money.dat", 'w') as f:
                f.write('10000')
                return 10000
            
    def save(self) -> None:
        #Сохранения
        try:
            with open("saves\\money.dat", 'w') as f:
                f.write(str(self.money))
        except:
            messagebox.showinfo('Ошибка', f'Не получается сохранить {self.name}')

    def update_lab(self) -> None:
        #Обновить надпись
        self.label = Label(text=f"Осталось {self.money} рублей", bg=self.th.bc, font="arial 16")
        self.label.place(x=20, y=600)

    def error(self) -> None:
        messagebox.showerror("Внимание!", "У вас недостаточно денег!")
        quit()

    def get(self) -> int:
        return self.money