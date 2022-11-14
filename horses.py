from random import randint
from tkinter import*
from copy import copy

class Horse():
    states = {1 : "Отличное, рвется вперед", 
              2 : "Все хорошо", 
              3 : "Не выспалась, подергивается веко", 
              4 : "У нее несварение, она плохо себя чувствует"}

    def __init__(self, name, y, photoFile):
        self.name = name
        self.posX = 20     
        self.posY = y
        #Копия координаты У чтобы ПОМНИТЬ где была изначально лошадь
        self.POSY = copy(self.posY)

        self.reverse = False
        self.play = True
        self.fastSpeed = False     
        self.state = self.states[randint(1, 4)]

        self.horseImage = PhotoImage(file=photoFile) 
        
        while self.horseImage.height() > 80:
            if self.horseImage.height() >= 500:
                self.horseImage.subsample(3, 3)
            else:
                self.horseImage.subsample(2, 2)
   
        self.label = Label(image=self.horseImage)
        self.label.place(x = self.posX, y=self.posY)

        #Установить лошадь по координатам
    def moveHorse(self):
        self.label.place(x = self.posX, y=self.posY)

        #Сбросить координаты к дефолтным
    def setapHorse(self):
        self.posY = copy(self.POSY)
        self.state = self.states[randint(1, 5)]
        self.label.place(x = self.posX, y=self.posY)
    
    def problemHorse(self):
        pass

    def run(self):
        if randint(0 , 100) < 20:
            problemHorse()
   

