from tkinter import Label
from tkinter import messagebox

class Money():

    def __init__(self, name):
        self.name = name
        self.money = self.load()
        #Проверка на кэш, если нет предупреждение
        assert self.money > 0 , self.error() 
        #Удоли
        print(f"Money {self.money}")

        self.label = Label(text=f"Осталось {self.money} рублей", bg="#4a898a", font="arial 16")
        self.label.place(x=20, y=600)

    def load(self) -> int:
        try:
            with open("saves\\money.dat", "r") as f:
                return int(f.read())
            
        except:
            with open("saves\\money.dat", 'w') as f:
                f.write('10000')
                return 10000
            
    def save(self) -> None:
        try:
            with open("saves\\money.dat", 'w') as f:
                f.write(str(self.money))
        except:
            messagebox.showinfo('Ошибка', f'Не получается сохранить {self.name}')

    def error(self) -> None:
        messagebox.showerror("Внимание!", "У вас недостаточно денег!")
        quit()