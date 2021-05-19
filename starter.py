import random
import numpy as np
import tkinter as tk
from tkinter import ttk
import time  
from PIL import Image, ImageTk  
from q_learning import Qlearning
from environment import Environment
from configure import episodeAmount,env_height,env_width,randomPixelRatio,startPageTitle,startPageResolation,XCBOptions,YCBOptions
from drawler import Drawler
class HomePage(tk.Tk, object):
    def __init__(self):
        super(HomePage, self).__init__()       
        #self.configure(bg="white")
        self.startPosition = [tk.StringVar(value=0),tk.StringVar(value=0)]
        self.endPosition = [tk.StringVar(value=0),tk.StringVar(value=0)]
        self.title(startPageTitle)
        self.geometry(startPageResolation)
        self.create_widgets()

    def create_widgets(self):
        self.startButton =  tk.Button(self,text="baslat",command=self.startQLearning)
        self.startButton.place(x = 190,y = 130)    
        self.startPositionLabel= tk.Label(self,text = "Başlangıç konumu :").place(x = 40,y = 60)
        self.endPositionLabel = tk.Label(self,text="Bitiş Konumu          :").place(x=40,y=100)
        self.startPositionComboBoxX = ttk.Combobox(self,values=XCBOptions,textvariable=self.startPosition[0],width=5)
        self.startPositionComboBoxX.place(x=150,y=60)
        self.startPositionComboBoxX.current(0)
        self.startPositionComboBoxY = ttk.Combobox(self,values=YCBOptions,textvariable=self.startPosition[1],width=5)
        self.startPositionComboBoxY.place(x=210,y=60)
        self.startPositionComboBoxY.current(0)
        # hedef konum labirentin sonuna yaikin olmasi acisindan degerler ters donduruluyor.
        self.endPositionComboBoxX = ttk.Combobox(self,values=XCBOptions[::-1],textvariable=self.endPosition[0],width=5)
        self.endPositionComboBoxX.place(x=150,y=100)
        self.endPositionComboBoxX.current(0)
        self.endPositionComboBoxY = ttk.Combobox(self,values=YCBOptions[::-1],textvariable=self.endPosition[1],width=5)
        self.endPositionComboBoxY.place(x=210,y=100)
        self.endPositionComboBoxY.current(0)
    def startQLearning(self):
        self.destroy()
        startPixel = (int(self.startPosition[0].get()),int(self.startPosition[1].get()))
        finishPixel = (int(self.endPosition[0].get()),int(self.endPosition[1].get()))
        start_time = time.time()
        learn_rate=0.9
        epsilon=0.05
        environment = Environment(startPixel,finishPixel)
        qLearn = Qlearning(environment,epsilon,learn_rate)
        shorthestPath,steps,allCost =qLearn.q_learn()

        print("--- %s seconds ---" % (time.time() - start_time))
        # cizdirme islemi 
        drawler = Drawler(startPixel,finishPixel,environment.ll_block,shorthestPath)
       
        drawler.plotLineChart(steps,allCost)
        # print(shorthestPath)
        # print(steps)
        # print(allCost)
        #qLearn.write_to_fle()
        
        drawler.mainloop()
    
# sadece bu dosya calistirilmak 
if __name__ == '__main__':
    env = HomePage()
    env.mainloop()
