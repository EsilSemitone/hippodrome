from random import randint, choice, uniform
from tkinter import*
from tkinter import messagebox
from os import listdir, replace


from Theme import Theme
from globalState import EventRate
from money import Money

class Horse():
    #Состояния 
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
        #Частота событий
        self.event = EventRate()

        #Скачивал рисунки я не с учебника, разрешение у них разное
        self.horseImage = PhotoImage(file=photoFile) 
       
        #Здесь я пытаюсь подогнать изображение до приемлемого
        self.horseImage = self.littlePhoto(self.horseImage)
                
        self.label = Label(image=self.horseImage)
        self.label.place(x=self.posX, y=self.posY)

    def littlePhoto(self, photo):
        '''Функция для уменьшения фотографий
        Только под конец пришло в голову создать для этого отдельную функцию :)'''
        #Узнаем высоту изображения (Раз оно квадратное то высоты должно быть достаточно)
        hght = photo.height()
        while hght >= 80:
            #Путем экспериметов заметил что так он более точно уменьшает изображение 
            if hght >= 500:
                #Уменьшаем изображение
                photo = photo.subsample(3, 3)
                hght = photo.height()
            else:
                photo = photo.subsample(2, 2)
                hght = photo.height()

        return photo

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
        #Герерируем проблемы
        if (randint(0, 250 +  weather + time + int(list(self.states.keys())[list(self.states.values()).index(self.state)]) + self.event.impact))  < 1:
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
        #По воле рандома и если лошадь не бежит назад то похоже будут проблемы
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
            #Если бежит, возвращаем 1 
            if self.play == True and self.reverse == False: 
                self.moveHorse()
                return 1
            else:
                #Иначе возвращаем 0
                if self.reverse:
                    self.moveHorse()
                return 0
        else:
            #Если прибежала то выставляем маркер что эта лошадь пришла к финишу 
            if self.set_reset_Win(True) == True:
                self.win = True
            return 0


class HorseLabel:
    #Класс размещающий иконку лошади и тд

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
        #Получаем список файлов-имен в папке с текстурами
        self.horsesNames = listdir('textures\\horses\\used')

        self.lab = Label(text=f"Ставка на лошадь №{self.amount}", background=self.theme.bc)
        self.lab.place(x=20, y=self.POS_LABELS[self.amount])
        #Определяем имя
        self.name = self.horsesNames[self.amount - 1].removesuffix(".png")

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
        '''
        На сколько помню я создал этот метод для того чтобы отслеживать и контролировать количество экземпляров класса

        True увеличивает количество на 1, False сбрасывает к единице
        '''
        if addReset:
            cls.amount += 1
        else:
            cls.amount = 1


class ShopLabel():
    '''Класс для размещения кнопок\текстур в окне магазина '''

    POS_LABELS = {
        1: 450,
        2: 600,
        3: 750
        }
    
    count = 0

    def __init__(self):
        self.th = Theme()

        #Если папка с конями пустая то выводим другую надпись
        if self.how_much_files < 1:
            self._no_products()

        #Изначатьно написал как в примере ниже но вызывается исключение None, почему?
        #assert self.how_much_files < 1, self._no_products()

        if self.how_much_files > 0: 
            self.money = Money()
            #Определяю что классов стало на 1 больше
            self.add_count()

            self.textureLab = Label(text='Купить новую лошадь!', bg=self.th.bc, font='arial 15')
            self.textureLab.place(x=510, y=100)
            self.mlab = Label(text='50000 рублей!', bg=self.th.bc, font='arial 12')
            self.mlab.place(x=550, y=140)
            #Список лошадей для покупки
            self.sale_list = listdir('textures\\horses\\not used')

            #Пробуем создать кнопку с изображением, если не получается не беда
            try:
                self.name = self.sale_list[self.count - 1]

                self.button_image = PhotoImage(file= 'textures\\horses\\not used\\' + self.sale_list[self.count - 1])
                self.button_image = self.littlePhoto(self.button_image)

                self.button = Button(image=self.button_image, command=self.buy_horse)
                self.button.place(x=self.POS_LABELS[self.count], y=200)

                self.horse_name = Label(text=self.sale_list[self.count - 1].removesuffix('.png'), bg=self.th.bc, font='arial 10')
                self.horse_name.place(x=self.POS_LABELS[self.count], y=300)

            except:
                pass

    #Где-то тут я вспомнил что недавно узнал про свойства классов и решил их применить :}
    @property
    def how_much_files(self) -> int:
        #Возвращает кол-во файлов в директории с текстурами коней
        return len(listdir('textures\\horses\\not used'))

    def _no_products(self) -> None:
        #Вызывается в случае если не осталось файлов в папке "not used" 
        self.textureLab = Label(text='Нет лошадей на продажу!!', bg=self.th.bc, font='arial 15')
        self.textureLab.place(x=510, y=100)

    @classmethod
    def reset_count(cls) -> None:
        #Сброс количества классов
        cls.count = 0

    @classmethod
    def add_count(cls) -> None:
        cls.count += 1

    def littlePhoto(self, photo):
        #Та же самая функция уменьшения фотографий
        hght = photo.height()
        while hght >= 100:
            if hght >= 500:
                photo = photo.subsample(3, 3)
                hght = photo.height()
            else:
                photo = photo.subsample(2, 2)
                hght = photo.height()
        return photo

    def buy_horse(self) -> None:
        #Функция покупки
        if self.money.get() < 50000:
            messagebox.showerror('Внимание!','Недостаточно денег для покупки!')
        else:
            #Здесь мы уменьшаем мани, сохраняем, перемещаем текстуру в папку с используемыми лошадьми, а текстуру старой в папку reserve
            self.money - 50000
            self.money.save()          
            replace('textures\\horses\\not used\\' + self.name, 'textures\\horses\\used\\' + self.name)
            self.old_image = listdir('textures\\horses\\used')[1]       
            replace('textures\\horses\\used\\' + self.old_image, 'textures\\horses\\reserve\\' + self.old_image)
            messagebox.showinfo('Внимание!', f"Покупка прошла успешно, вы купили {self.name.removesuffix('.png')}")
            self.money.update_lab()
            #Удаляем кнопку
            self.button.destroy()
            self.horse_name.destroy()