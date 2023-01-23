from os import listdir
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from horses import Horse, HorseLabel
from money import Money
from globalState import Weather, Time
from Theme import Theme

class GameWindow():
    
    root = Tk()
    WIDTH = 1024
    HEIGTH = 640
    POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
    POS_Y = root.winfo_screenheight() // 2 - HEIGTH // 2
    iconPhoto = "textures\\icon\\horse.png"
    root.title("Ипподром")
    root.iconphoto(True, PhotoImage(file=iconPhoto))
    root.geometry(f"{WIDTH}x{HEIGTH}+{POS_X}+{POS_Y}")
    root.resizable(False, False)
    

    def __init__(self):
        self.theme = Theme()
        self.root.config(bg=self.theme.bc)
        self.roadImage = PhotoImage(file="textures\\other\\road.png")
        self.road = Label(self.root, image=self.roadImage)
        self.road.place(x=0, y=17)
        #беру названия изображений лошадей в виде списка
        self.horsesNames = listdir('textures\\horses\\used')
        #И присваиваю лошадям имя файла и путь к текстурам
        self.Horse01 = Horse(f"{self.horsesNames[0].removesuffix('.png')}", 20, f"textures\\horses\\used\\{self.horsesNames[0]}")
        self.Horse02 = Horse(f"{self.horsesNames[1].removesuffix('.png')}", 100, f"textures\\horses\\used\\{self.horsesNames[1]}")
        self.Horse03 = Horse(f"{self.horsesNames[2].removesuffix('.png')}", 180, f"textures\\horses\\used\\{self.horsesNames[2]}")
        self.Horse04 = Horse(f"{self.horsesNames[3].removesuffix('.png')}", 260, f"textures\\horses\\used\\{self.horsesNames[3]}")
        #баблишко
        self.money = Money("Рублей")
        #Кнопки
        self.startButton = Button(text='Старт', font="arial 18", width=30, state="disabled", bg=self.theme.button, fg='#FFFFFF', bd=3, command=self.Start)
        self.startButton.place(x=20, y=370)

        self.settingButton = Button(text="Настройки", font="arial 18", width=15, bg=self.theme.button, fg='#FFFFFF', bd=3, command=self.goSettings)
        self.settingButton.place(x=510, y=370)
        self.settingImage = PhotoImage(file="textures\\buttons\\settings.png")
        self.settingImage = self.settingImage.subsample(12, 12)
        self.settingIco = Label(self.root, image=self.settingImage)
        self.settingIco.place(x=455, y=370)

        self.shopButton = Button(text="Магазин", font="arial 18", width=15, bg=self.theme.button, fg='#FFFFFF', bd=3, command=self.goMall)
        self.shopButton.place(x=795, y=370)
        self.shopImage = PhotoImage(file="textures\\buttons\\shop1.png")
        self.shopImage = self.shopImage.subsample(12, 12)
        self.shopIco = Label(self.root, image=self.shopImage)
        self.shopIco.place(x=740, y=370)
        
        self.lab1 = HorseLabel()
        self.lab2 = HorseLabel()
        self.lab3 = HorseLabel()
        self.lab4 = HorseLabel()

        self.bet01 = IntVar() 
        self.bet02 = IntVar() 
        self.bet03 = IntVar() 
        self.bet04 = IntVar() 

        self.box01 = ttk.Combobox(self.root, state="readonly", values=self.betList(), textvariable=self.bet01)
        self.box02 = ttk.Combobox(self.root, state="readonly", values=self.betList(), textvariable=self.bet02)
        self.box03 = ttk.Combobox(self.root, state="readonly", values=self.betList(), textvariable=self.bet03)
        self.box04 = ttk.Combobox(self.root, state="readonly", values=self.betList(), textvariable=self.bet04)

        self.box01.current(0)
        self.box02.current(0)
        self.box03.current(0)
        self.box04.current(0)

        self.box01.bind("<<ComboboxSelected>>", self.betSelected)
        self.box02.bind("<<ComboboxSelected>>", self.betSelected)
        self.box03.bind("<<ComboboxSelected>>", self.betSelected)
        self.box04.bind("<<ComboboxSelected>>", self.betSelected)

        self.box01.place(x=280, y=450)
        self.box02.place(x=280, y=480)
        self.box03.place(x=280, y=510)
        self.box04.place(x=280, y=540)

        self.textInfo = Text(width=70, height=10, wrap=WORD, bg=self.theme.bc_text_field, fg='#FFFFFF')
        self.textInfo.place(x=430, y=450)

        self.scroll = Scrollbar(command=self.textInfo.yview, width=20, bg="#314545")
        self.scroll.place(x=990, y=450, height=164)
        self.textInfo["yscrollcommand"] = self.scroll.set
        #Устанавливаю погоду и время суток 
        self.weather = Weather()
        self.time_set = Time()
        
        #Отображаю ее в чате
        self.setText()
    

    def setText(self) -> None:
        '''установка информациив чат'''
        self.text = f"Сейчас на улице {self.time_set.get_state()}, {self.weather.get_state()}." + '\n'
        self.textInfo.insert(INSERT, self.text  + '\n')
        self.textInfo.insert(INSERT, f'{self.Horse01.name}, {self.Horse01.state} {self.Horse01.factor}:1' + '\n')
        self.textInfo.insert(INSERT, f'{self.Horse02.name}, {self.Horse02.state} {self.Horse02.factor}:1' + '\n')
        self.textInfo.insert(INSERT, f'{self.Horse03.name}, {self.Horse03.state} {self.Horse03.factor}:1' + '\n')
        self.textInfo.insert(INSERT, f'{self.Horse04.name}, {self.Horse04.state} {self.Horse04.factor}:1' + '\n')
        #Смотреть в конец
        self.textInfo.see(END)

    def Kill(self) -> None:
        #функция очищающая окно, спасибо Илье, подсмотрел в головоломке!
        for self.child in self.root.winfo_children():
            self.child.destroy()
      
    def sumBets(self) -> list:
        '''Функция возвращающая сумму ставок'''
        return sum([
            self.bet01.get(),
            self.bet02.get(),
            self.bet03.get(),
            self.bet04.get()])

    def betSelected(self, *args) -> None:
        lst = self.sumBets()

        self.money.label['text'] = f"Осталось {self.money.money - lst} рублей"

        self.box01['values'] = self.betList()
        self.box02['values'] = self.betList()
        self.box03['values'] = self.betList()
        self.box04['values'] = self.betList()

        if lst > 0:
            self.startButton["state"] = "normal"
        else:
            self.startButton["state"] = "disabled"

        if self.bet01.get():
            self.lab1.checkVar.set(1)
        else:
            self.lab1.checkVar.set(0)

        if self.bet02.get():
            self.lab2.checkVar.set(1)
        else:
            self.lab2.checkVar.set(0) 
            
        if self.bet03.get():
            self.lab3.checkVar.set(1)
        else:
            self.lab3.checkVar.set(0)

        if self.bet04.get():
            self.lab4.checkVar.set(1)
        else:
            self.lab4.checkVar.set(0)

    def betList(self):
        self.mon = self.money.money - self.sumBets()

        if self.mon <= 0:
            return 0

        if self.mon <= 100:
            return [self.mon]

        return [self.mon // 100 * 10 * i for i in range(0, 11)]

    def winner(self, res) -> None:

        self.lst = [
            [self.bet01.get(), self.Horse01.factor, self.Horse01.name], 
            [self.bet02.get(), self.Horse02.factor, self.Horse02.name], 
            [self.bet03.get(), self.Horse03.factor, self.Horse03.name], 
            [self.bet04.get(), self.Horse04.factor, self.Horse04.name]
            ]

        if res != None:
            if self.lst[res - 1][0] > 0:
                self.money + int(self.lst[res - 1][0] * self.lst[res - 1][1])
                #self.money.money += int(self.lst[res - 1][0] * self.lst[res - 1][1])
                self.money.save()
                self.textInfo.insert(INSERT, '   ' + '\n')
                self.textInfo.insert(INSERT, f'Победитель {self.lst[res - 1][2]}!' + '\n')
                self.textInfo.insert(INSERT, '   ')
                self.textInfo.see(END)
                messagebox.showinfo('Поздравляю!',f'Вы выйграли {int(self.lst[res - 1][0] * self.lst[res - 1][1])} {self.money.name}!')    
                
            else:           
                self.textInfo.insert(INSERT, '   ' + '\n')
                self.textInfo.insert(INSERT, f'Победитель {self.lst[res - 1][2]}!' + '\n')
                self.textInfo.see(END)
                messagebox.showinfo('Эх','Вы ничего не выйграли!')
                for i in self.lst:
                    self.money - int(i[0])
                    #self.money.money -= int(i[0])
                    self.money.save()
                
        elif res == None:
            messagebox.showinfo('Эх','Ни одна лошадь не пришла к финишу!')

            for i in self.lst:
                self.money.money -= int(i[0])
                self.money.save()

        self.box01.current(0)
        self.box02.current(0)
        self.box03.current(0)
        self.box04.current(0)

    def win_round(self, res):      
        
        self.winner(res)


        self.weather = Weather()
        self.time_set = Time()
        self.Horse01.setapHorse()
        self.Horse02.setapHorse()
        self.Horse03.setapHorse()
        self.Horse04.setapHorse()
        self.setText()


    def Start(self) -> None:

        self.horse_finish =[
            self.Horse01.run(self.weather.impact_on_speed(), self.weather.impact_on_problem(), self.time_set.impact_on_speed(), self.time_set.impact_on_problem()),
            self.Horse02.run(self.weather.impact_on_speed(), self.weather.impact_on_problem(), self.time_set.impact_on_speed(), self.time_set.impact_on_problem()),
            self.Horse03.run(self.weather.impact_on_speed(), self.weather.impact_on_problem(), self.time_set.impact_on_speed(), self.time_set.impact_on_problem()),
            self.Horse04.run(self.weather.impact_on_speed(), self.weather.impact_on_problem(), self.time_set.impact_on_speed(), self.time_set.impact_on_problem())
        ]

        #сначала проверка на то прибежали лошади к финишу или нет
        if any([i == 1 for i in self.horse_finish]):                
            self.root.after(5, self.Start) 
            #Ниже я пока не понимаю как правильно написать, в плане чтобы выглядело красиво
        else:
            for key, value in {
                    1: self.Horse01.win,
                    2: self.Horse02.win,
                    3: self.Horse03.win,
                    4: self.Horse04.win}.items():
                print(value)#Для себя
                if value != None:  
                    print(value)#Для себя
                    self.win_round(key)
                    break

    def goMall(self):
        self.Kill()
        self.shop = Shop()
        
    def goSettings(self):
        self.Kill()
        HorseLabel.howMany(False)
        self.setting = Settings()

    def goMenu(self):
        self.Kill()
        HorseLabel.howMany(False)
        self.menu = MenuGameWindow()

    def goGame(self):
        self.Kill()
        HorseLabel.howMany(False)
        self.game = GameWindow()

    def Exit(self):
        self.root.destroy()


class MenuGameWindow(GameWindow):
    
    def __init__(self):
        self.menuImage = PhotoImage(file='textures\\other\\менюшка.png')

        #Здесь тоже подгоняю размер      
        self.menuImage = self.menuImage.subsample(5, 4)
        self.menu = Label(image=self.menuImage)
        self.menu.place(x=0, y=0)
        self.gameButton = Button(text='Играть', font="arial 18", width=50, command=self.goGame, bg='#FFB266', activebackground='#FFCC99')
        self.gameButton.place(x=155, y=420)
        self.settingButton = Button(text="Настройки", font='arial 18', width=50, command=self.goSettings, bg='#FFB266', activebackground='#FFCC99')
        self.settingButton.place(x=155, y=470)
        self.quitButton = Button(text="Выход", font='arial 18', width=50, command=self.Exit, bg='#FFB266', activebackground='#FFCC99')
        self.quitButton.place(x=155, y=520)
        self.mainTextLabel = Label(text="Ипподром", width=50, font='arial 20', bg='#FFB266')
        self.mainTextLabel.place(x = 110, y = 80)
       
    
class Shop(GameWindow):
    pass


class Settings(GameWindow):

    def __init__(self):
        
        self.th = Theme()
        self.root.config(bg=self.th.bc)
        self.lab = Label(text='Настройки', font='arial 30', bg=self.th.bc)
        self.lab.place(x=410, y=20)
        self.lab_theme = Label(text="Тема", font="arial 15", bg=self.th.bc)
        self.lab_theme.place(x=20, y=110)

        self.event_lab = Label(text='Частота событий', font='arial 15', bg=self.th.bc)
        self.event_lab.place(x=20, y=200)
        self.event_var = StringVar

        self.theme_var = StringVar()
        self.theme = ttk.Combobox(self.root, state='readonly', values=self.th.get_theme(), textvariable=self.theme_var, width=30)
        self.theme.place(x=20, y=150)
        self.theme.set(self.th.theme)
        self.theme.bind("<<ComboboxSelected>>", self.theme_select)

        

    
    def theme_select(self, *args) -> None:
        self.theme_update(self.theme_var.get())
        self.th = Theme()
        self.root.config(bg=self.th.bc)
        self.lab = Label(text='Настройки', font='arial 30', bg=self.th.bc)
        self.lab.place(x=410, y=20)
        self.lab_theme = Label(text="Тема", font="arial 15", bg=self.th.bc)
        self.lab_theme.place(x=20, y=110)
        self.event_lab = Label(text='Частота событий', font='arial 15', bg=self.th.bc)
        self.event_lab.place(x=20, y=200)

        

    def theme_update(self, var) -> None:
        print(f'Выбрана тема {var}')
        self.th.select_theme(var)
        