import random
import numpy as np
import tkinter as tk
from tkinter import ttk
import time  # Time is needed to slow down the agent and to see how he runs
from PIL import Image, ImageTk  # For adding images into the canvas widget
from path import Environment
from agent import QLearningTable
from configure import episodeAmount,maxIndex,env_height,env_width,randomPixelRatio,startPageTitle,startPageResolation,startPositionCBOptions,endPostionCBOptions
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
        self.startPositionComboBoxX = ttk.Combobox(self,values=startPositionCBOptions,textvariable=self.startPosition[0],width=5)
        self.startPositionComboBoxX.place(x=150,y=60)
        self.startPositionComboBoxY = ttk.Combobox(self,values=startPositionCBOptions,textvariable=self.startPosition[1],width=5)
        self.startPositionComboBoxY.place(x=210,y=60)
        self.endPositionComboBoxX = ttk.Combobox(self,values=endPostionCBOptions,textvariable=self.endPosition[0],width=5)
        self.endPositionComboBoxX.place(x=150,y=100)
        self.endPositionComboBoxY = ttk.Combobox(self,values=endPostionCBOptions,textvariable=self.endPosition[1],width=5)
        self.endPositionComboBoxY.place(x=210,y=100)

    def startQLearning(self):
        self.destroy()
        startPixel = [int(self.startPosition[0].get()),int(self.startPosition[1].get())]
        finishPixel = [int(self.endPosition[0].get()),int(self.endPosition[1].get())]
        # random Obstacle coordinat list ex:5x5 [0,3]
        obstacleCoordinats = np.random.randint(maxIndex,size=(int(env_height*env_width*randomPixelRatio),2))
        for XY in obstacleCoordinats:
            if (XY[0]==finishPixel[0] and XY[1]==finishPixel[1]) or (XY[0]==startPixel[0] and XY[1]==startPixel[1]):
                print(obstacleCoordinats)
                np.delete(obstacleCoordinats,XY)
                print(obstacleCoordinats)
        self.env = Environment(startPixel ,finishPixel,obstacleCoordinats)
        # Calling for the main algorithm
        self.RL = QLearningTable(actions=list(range(self.env.n_actions)))
        # Running the main loop with Episodes by calling the function update()
        self.env.after(100, self.update)  # Or just update()
        self.env.mainloop()

    def update(self):
        # Resulted list for the plotting Episodes via Steps
        steps = []

    # Summed costs for all episodes in resulted list
        all_costs = []

        for episode in range(episodeAmount):
        # Initial Observation
            observation = self.env.reset()
        # Updating number of Steps for each Episode
            i = 0

        # Updating the cost for each episode
            cost = 0

            while True:
            # Refreshing environment
                self.env.render()

            # RL chooses action based on observation
                action = self.RL.choose_action(str(observation))

            # RL takes an action and get the next observation and reward
                observation_, reward, done = self.env.step(action)

            # RL learns from this transition and calculating the cost
                cost += self.RL.learn(str(observation), action, reward, str(observation_))

            # Swapping the observations - current and next
                observation = observation_

            # Calculating number of Steps in the current Episode
                i += 1

            # Break while loop when it is the end of current Episode
            # When agent reached the goal or obstacle
                if done:
                    steps += [i]
                    all_costs += [cost]
                    break

    # Showing the final route
        self.env.final()

    # Showing the Q-table with values for each action
        self.RL.print_q_table()

    # Plotting the results
        self.RL.plot_results(steps, all_costs)

# sadece bu dosya calistirilmak 
if __name__ == '__main__':
    env = HomePage()
    env.mainloop()
