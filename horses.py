from random import randint, choice, uniform
from tkinter import*
from tkinter import messagebox
from os import listdir

from Theme import Theme

class Horse():
    states = {
        1 : "Отлично себя чувствует, рвется вперед.", 
        2 : "Все хорошо.", 
        3 : "В напряжении, подергивается веко.", 
        4 : "кажется несварение, плохо себя чувствует."
        }

    _winner = None #Переменная определяющая, есть ли победитель среди лошадей 
    speed = None
    
    def __init__(self, name, y, photoFile):
        self.name = name
        self.posX = 20     
        self.posY = y
        #Копия координаты У чтобы ПОМНИТЬ где была изначально лошадь
        self.SETAP_POS_X = 20
        self.reverse = False
        self.play = True
        self.fastSpeed = False     
        self.state = self.states[randint(1, 4)] #Состояние
        self.factor = round(uniform(1, 5), 2) #Коофицент 

        self.win = None #Эта лощадь победитель?

        self.horseImage = PhotoImage(file=photoFile) 
        #Скачивал рисунки я не с учебника, разрешение у них разное
        #Здесь я пытаюсь подогнать изображение до приемлемого
        #Если не использовать отдельную переменную то этот алгоритм не работает :\
        self.hgth = self.horseImage.height()

        while self.hgth >= 80:
            if self.hgth >= 500:
                self.horseImage = self.horseImage.subsample(3, 3) #уменьшение в три раза по высоте и ширине
                self.hgth = self.horseImage.height()              
            else:
                self.horseImage = self.horseImage.subsample(2, 2)
                self.hgth = self.horseImage.height()
                
        self.label = Label(image=self.horseImage)
        self.label.place(x=self.posX, y=self.posY)

        #Установить лошадь по координатам
    def moveHorse(self):
        self.label.place(x=self.posX, y=self.posY)

        #Сбросить координаты к дефолтным
    def setapHorse(self):
        self.posX = self.SETAP_POS_X
        self.factor = round(uniform(1, 12), 2)
        self.state = self.states[randint(1, 4)]
        self.reverse = False
        self.play = True
        self.fastSpeed = False 
        self.moveHorse()
        self.win = None
        self.set_reset_Win(False)
    
    @classmethod
    def set_reset_Win(cls, state) -> bool:
        '''Передаем True если нужно проверить _winner и в случае если он None поместить в него информацию и возвратить True иначе False
           Передаем False если нужно сбросить значение _winner
           Функция нужна для того чтобы определить победителя и запомнить что он уже определен при следующем вызове функции
           возможно этого результата можно добиться более простым способом \-_-/'''

        if state is True:
            if cls._winner is None:
                cls._winner = True
                return True
            return False
        else:
            cls._winner = None

    def problemHorse(self, weather, time):

        if (randint(0, 250 +  weather + time + int(list(self.states.keys())[list(self.states.values()).index(self.state)]))) < 1:
            print("Внимание!")

            if randint(1, 3) == 1:
                self.fastSpeed = True
                messagebox.showinfo("Внимание!", f"{self.name} рвется вперед! ")
            else:
                if randint(0, 1) == 0:
                    self.reverse = True
                    messagebox.showinfo("Внимание!", f"{self.name} Бежит обратно к финишу!! ")
                else:
                    self.play = False
                    messagebox.showinfo("Внимание!", f"У {self.name} слетел наездник! ")

    def run(self, weather_speed, weather_problem, time_speed, time_problem) -> int:

        if randint(0 , 100) < 20 and self.play and not self.reverse:
            self.problemHorse(weather_problem, time_problem)
 
        #Произвожу расчет скорости
        if self.state == self.states[1]:
            self.speed = choice([2.5, 2.1, 2.3, 3])
        elif self.state == self.states[2]:
            self.speed = choice([2, 2.1, 2.3, 1.8])
        elif self.state == self.states[3]:
            self.speed = choice([2, 1.8, 1.9])
        elif self.state == self.states[4]:
            self.speed = choice([1.7, 1.8, 1.6])

        #плюшки или дебафы от погоды
        self.speed += choice(weather_speed)
        #времени суток..
        self.speed += choice(time_speed)
        #Проверка на маркеры состояний
        if self.reverse:
            self.posX -= self.speed
        elif self.play and self.reverse == False:
            if self.fastSpeed:
                self.posX += self.speed * 1.12
            else:
                self.posX += self.speed
             

        if self.posX < 952:
            if self.play == True and self.reverse == False: #Если бежит, возвращаем 1 Прибежала -> 0
                self.moveHorse()
                return 1
            else:
                if self.reverse:
                    self.moveHorse()
                return 0
        else:
            if self.set_reset_Win(True) == True:
                self.win = True
            return 0


class HorseLabel:
    #счетчик класов, в зависимости от того каким по счету был создан экземпляр его наполнение POS_CHECK\POS_LABELS\lab будет изменятся
    amount = 1
    POS_CHECK = {
        1: 448,
        2: 478,
        3: 508,
        4: 538
        }

    POS_LABELS = {
        1: 450,
        2: 480,
        3: 510,
        4: 540
        }

    def __init__(self):
        self.theme = Theme()
        self.horsesNames = listdir('textures\\horses\\used')
        self.lab = Label(text=f"Ставка на лошадь №{self.amount}", background=self.theme.bc)
        self.lab.place(x=20, y=self.POS_LABELS[self.amount])
        self.name = self.horsesNames[self.amount - 1].removesuffix(".png")
        print(self.name)

        self.checkVar = BooleanVar()
        self.checkVar.set(0)
        self.horseCheck = Checkbutton(
            text=self.name, 
            variable=self.checkVar, 
            bg=self.theme.bc, 
            state="disabled"
            )

        self.horseCheck.place(x=150, y=self.POS_CHECK[self.amount])
        self.howMany(True)
            
    @classmethod
    def howMany(cls, addReset: bool) -> None:
        '''True увеличивает количество на 1, False сбрасывает к единице'''
        if addReset:
            cls.amount += 1
        else:
            cls.amount = 1
   
