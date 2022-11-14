from tkinter import *
from horses import Horse
from money import Money

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
    root.config(bg="#4a898a")

    def __init__(self):
        self.root.config(bg="#4a898a")
        self.roadImage = PhotoImage(file="textures\\other\\road.png")
        self.road = Label(self.root, image=self.roadImage)
        self.road.place(x=0, y=17)
        self.Horse01 = Horse("Яблонька", 20, "textures\\horses\\used\\лошадь1.png")
        self.Horse02 = Horse("Кобылка", 100, "textures\\horses\\used\\лошадь2.png")
        self.Horse03 = Horse("Жемчужина", 180, "textures\\horses\\used\\лошадь3.png")
        self.Horse04 = Horse("Быстряк", 260, "textures\\horses\\used\\лошадь4.png")
        
        
        self.money = Money("saves\\money.dat", "Рублей")
        self.money.load() 
        self.startButton = Button(text='Старт', font="arial-20", width=30, state="disabled", bg="#37AA37", fg='#FFFFFF', bd=3, command=self.Start)



    def Start(self):
        self.Horse01.run()
        self.Horse02.run()
        self.Horse03.run()
        self.Horse04.run()

class MenuGameWindow(GameWindow):
    pass

class Shop(GameWindow):
  
    pass

class Settings(GameWindow):
    pass