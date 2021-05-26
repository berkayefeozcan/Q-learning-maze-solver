import numpy as np
import tkinter as tk
import time  
from PIL import Image, ImageTk 
from configure import a,env_height,env_width,pixels
import matplotlib.pyplot as plt

class Drawler(tk.Tk, object):
    def __init__(self,startPosition,endPosition,obstacleCoordinats,finalRouteDic):
        super(Drawler, self).__init__()
        self.obstacleLocationsList = []
        self.action_space = ['up', 'down', 'left', 'right']
        self.n_actions = len(self.action_space)
        self.title('Shortest Path')
        width= self.winfo_screenwidth()       
        height= self.winfo_screenheight()       
        self.geometry('{0}x{1}'.format(env_width * pixels, env_height * pixels))
        # start and end point 
        self.startPixel=startPosition
        self.finishPixel = endPosition
        self.obstacleCoordinats= obstacleCoordinats
        self.build_environment()
    
  
        self.f = finalRouteDic
        self.final()


    def build_environment(self):
        self.canvas_widget = tk.Canvas(self,  bg='white',
                                       height=env_height * pixels,
                                       width=env_width * pixels)

   
        img_background = Image.open("images/background.jpg")
        img_background= img_background.resize((env_width * pixels,env_height * pixels),Image.NEAREST)
        self.background = ImageTk.PhotoImage(img_background)
    
        self.bg = self.canvas_widget.create_image(0, 0, anchor='nw',image=self.background)

        for column in range(0, env_width * pixels, pixels):
            x0, y0, x1, y1 = column, 0, column, env_height * pixels
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')
        for row in range(0, env_width * pixels, pixels):
            x0, y0, x1, y1 = 0, row, env_width * pixels, row
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')

       
        self.o = np.array([pixels / 2, pixels / 2])
        # print('aaas {0}'.format(self.o))
        for coordinats in self.obstacleCoordinats:
            obstacle_center = self.o + np.array([pixels*coordinats[0], pixels * coordinats[1]])
            obstacle = self.canvas_widget.create_rectangle(
            obstacle_center[0] - 10, obstacle_center[1] - 10,  
            obstacle_center[0] + 10, obstacle_center[1] + 10,  
            outline='#d40000', fill='#d40000')
            location = [self.canvas_widget.coords(obstacle)[0] + 3,
                                 self.canvas_widget.coords(obstacle)[1] + 3,
                                 self.canvas_widget.coords(obstacle)[2] - 3,
                                 self.canvas_widget.coords(obstacle)[3] - 3]
            self.obstacleLocationsList.append(location)
        
        # agent starting point 
        agentStartCoords = self.o + np.array([pixels*self.startPixel[0], pixels * self.startPixel[1]])
        self.canvas_widget.create_rectangle(
            agentStartCoords[0] - 10, agentStartCoords[1] - 10,  
            agentStartCoords[0] + 10, agentStartCoords[1] + 10,  
            outline='grey', fill='#47b8f5')
        self.agent = self.canvas_widget.create_oval(
            agentStartCoords[0] - 7, agentStartCoords[1] - 7,
            agentStartCoords[0] + 7, agentStartCoords[1] + 7,
            outline='grey', fill='black')
        # print(self.agent)
        # end point 
        flag_center = self.o + np.array([pixels * self.finishPixel[0], pixels * self.finishPixel[1]])
      
        self.flag = self.canvas_widget.create_rectangle(
            flag_center[0] - 10, flag_center[1] - 10,  
            flag_center[0] + 10, flag_center[1] + 10,  
            outline='grey', fill='green')
     
        self.coords_flag = [self.canvas_widget.coords(self.flag)[0] + 3,
                            self.canvas_widget.coords(self.flag)[1] + 3,
                            self.canvas_widget.coords(self.flag)[2] - 3,
                            self.canvas_widget.coords(self.flag)[3] - 3]

       
        self.canvas_widget.pack()


    def final(self):
       
        self.canvas_widget.delete(self.agent)
        print(self.f)
        # print('The shortest route:', self.shortest)
        # print('The longest route:', self.longest)

        # Creating initial point
        agentStartCoords = self.o + np.array([pixels*self.startPixel[0], pixels * self.startPixel[1]])
      
        self.initial_point = self.canvas_widget.create_oval(
            agentStartCoords[0] - 4, agentStartCoords[1] - 4,
            agentStartCoords[0] + 4, agentStartCoords[1] + 4,
            fill='blue', outline='red')

        # Filling the route
        for j in range(len(self.f)):
            # Showing the coordinates of the final route
            #print(self.f[j])
            time.sleep(0.05)
            agentStartCoords = self.o + np.array([pixels*self.f[j][0], pixels * self.f[j][1]])
            temp = self.canvas_widget.create_oval(
            agentStartCoords[0] - 5, agentStartCoords[1] - 5,
            agentStartCoords[0] + 5, agentStartCoords[1] + 5,
            fill='blue', outline='blue')

            self.f[j]=self.canvas_widget.coords(temp)
            self.update()

    def plotLineChart(self,steps,cost):
        f, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        #
        ax1.plot(np.arange(len(steps)), steps, 'b')
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Steps')
        ax1.set_title('Episode via steps')

        #
        ax2.plot(np.arange(len(cost)), cost, 'r')
        ax2.set_xlabel('Episode')
        ax2.set_ylabel('Cost')
        ax2.set_title('Episode via cost')

        plt.tight_layout()  
        plt.show()



# if __name__ == '__main__':
#     env = Drawler()
#     env.mainloop()
