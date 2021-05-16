import numpy as np
import tkinter as tk
import time  # Time is needed to slow down the agent and to see how he runs
from PIL import Image, ImageTk  # For adding images into the canvas widget
from configure import a,env_height,env_width,pixels

# Creating class for the environment
class Environment(tk.Tk, object):
    def __init__(self,startPosition,endPosition,obstacleCoordinats):
        super(Environment, self).__init__()
        self.obstacleLocationsList = []
        self.action_space = ['up', 'down', 'left', 'right']
        self.n_actions = len(self.action_space)
        self.title('Path Following')
        self.geometry('{0}x{1}'.format(env_height * pixels, env_height * pixels))
        #baslangic ve bitis konumlari - int 
        self.startPixel=startPosition
        self.finishPixel = endPosition
        self.obstacleCoordinats= obstacleCoordinats
        self.build_environment()
        # Dictionaries to draw the final route
        self.d = {}
        self.f = {}

        # Key for the dictionaries
        self.i = 0

        # Writing the final dictionary first time
        self.c = True

        # Showing the steps for longest found route
        self.longest = 0

        # Showing the steps for the shortest route
        self.shortest = 0

    # Function to build the environment
    def build_environment(self):
        self.canvas_widget = tk.Canvas(self,  bg='white',
                                       height=env_height * pixels,
                                       width=env_width * pixels)

        # Uploading an image for background
        img_background = Image.open("images/bg.png")
        self.background = ImageTk.PhotoImage(img_background)
        # Creating background on the widget
        self.bg = self.canvas_widget.create_image(0, 0, anchor='nw', image=self.background)

        # Creating grid lines
        for column in range(0, env_width * pixels, pixels):
            x0, y0, x1, y1 = column, 0, column, env_height * pixels
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')
        for row in range(0, env_height * pixels, pixels):
            x0, y0, x1, y1 = 0, row, env_height * pixels, row
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')

        # Creating objects of  Obstacles
        # An array to help with building rectangles
        self.o = np.array([pixels / 2, pixels / 2])
        print('aaas {0}'.format(self.o))
        for coordinats in self.obstacleCoordinats:
            obstacle_center = self.o + np.array([pixels*coordinats[0], pixels * coordinats[1]])
            obstacle = self.canvas_widget.create_rectangle(
            obstacle_center[0] - 10, obstacle_center[1] - 10,  # Top left corner
            obstacle_center[0] + 10, obstacle_center[1] + 10,  # Bottom right corner
            outline='grey', fill='#00BFFF')
            location = [self.canvas_widget.coords(obstacle)[0] + 3,
                                 self.canvas_widget.coords(obstacle)[1] + 3,
                                 self.canvas_widget.coords(obstacle)[2] - 3,
                                 self.canvas_widget.coords(obstacle)[3] - 3]
            self.obstacleLocationsList.append(location)
        
        # Creating an agent of Mobile Robot - red point
        agentStartCoords = self.o + np.array([pixels*self.startPixel[0], pixels * self.startPixel[1]])
        self.agent = self.canvas_widget.create_oval(
            agentStartCoords[0] - 7, agentStartCoords[1] - 7,
            agentStartCoords[0] + 7, agentStartCoords[1] + 7,
            outline='#FF1493', fill='#FF1493')
        print(self.agent)
        # Final Point - yellow point
        flag_center = self.o + np.array([pixels * self.finishPixel[0], pixels * self.finishPixel[1]])
        # Building the flag
        self.flag = self.canvas_widget.create_rectangle(
            flag_center[0] - 10, flag_center[1] - 10,  # Top left corner
            flag_center[0] + 10, flag_center[1] + 10,  # Bottom right corner
            outline='grey', fill='yellow')
        # Saving the coordinates of the final point according to the size of agent
        # In order to fit the coordinates of the agent
        self.coords_flag = [self.canvas_widget.coords(self.flag)[0] + 3,
                            self.canvas_widget.coords(self.flag)[1] + 3,
                            self.canvas_widget.coords(self.flag)[2] - 3,
                            self.canvas_widget.coords(self.flag)[3] - 3]

        # Packing everything
        self.canvas_widget.pack()

    # Function to reset the environment and start new Episode
    def reset(self):
        self.update()
        #time.sleep(0.5)

        # Updating agent
        self.canvas_widget.delete(self.agent)
        agentStartCoords = self.o + np.array([pixels*self.startPixel[0], pixels * self.startPixel[1]])
        self.agent = self.canvas_widget.create_oval(
            agentStartCoords[0] - 7, agentStartCoords[1] - 7,
            agentStartCoords[0] + 7, agentStartCoords[1] + 7,
            outline='#FF1493', fill='#FF1493')

        # Clearing the dictionary and the i
        self.d = {}
        self.i = 0

        # Return observation
        return self.canvas_widget.coords(self.agent)

    # Function to get the next observation and reward by doing next step
    def step(self, action):
        # Current state of the agent
        state = self.canvas_widget.coords(self.agent)
        base_action = np.array([0, 0])

        # Updating next state according to the action
        # Action 'up'
        if action == 0:
            if state[1] >= pixels:
                base_action[1] -= pixels
        # Action 'down'
        elif action == 1:
            if state[1] < (env_height - 1) * pixels:
                base_action[1] += pixels
        # Action right
        elif action == 2:
            if state[0] < (env_width - 1) * pixels:
                base_action[0] += pixels
        # Action left
        elif action == 3:
            if state[0] >= pixels:
                base_action[0] -= pixels

        # Moving the agent according to the action
        self.canvas_widget.move(self.agent, base_action[0], base_action[1])

        # Writing in the dictionary coordinates of found route
        self.d[self.i] = self.canvas_widget.coords(self.agent)

        # Updating next state
        next_state = self.d[self.i]

        # Updating key for the dictionary
        self.i += 1

        # Calculating the reward for the agent
        if next_state == self.coords_flag:
            time.sleep(0.1)
            reward = 5
            done = True
            next_state = 'goal'

            # Filling the dictionary first time
            if self.c == True:
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]
                self.c = False
                self.longest = len(self.d)
                self.shortest = len(self.d)

            # Checking if the currently found route is shorter
            if len(self.d) < len(self.f):
                # Saving the number of steps for the shortest route
                self.shortest = len(self.d)
                # Clearing the dictionary for the final route
                self.f = {}
                # Reassigning the dictionary
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]

            # Saving the number of steps for the longest route
            if len(self.d) > self.longest:
                self.longest = len(self.d)

        elif next_state in self.obstacleLocationsList:

            reward = -5
            done = True
            next_state = 'obstacle'

            # Clearing the dictionary and the i
            self.d = {}
            self.i = 0

        else:
            reward = 3
            done = False

        return next_state, reward, done

    # Function to refresh the environment
    def render(self):
        #time.sleep(0.03)
        self.update()

    # Function to show the found route
    def final(self):
        # Deleting the agent at the end
        self.canvas_widget.delete(self.agent)

        # Showing the number of steps
        print('The shortest route:', self.shortest)
        print('The longest route:', self.longest)

        # Creating initial point
        agentStartCoords = self.o + np.array([pixels*self.startPixel[0], pixels * self.startPixel[1]])
      
        self.initial_point = self.canvas_widget.create_oval(
            agentStartCoords[0] - 4, agentStartCoords[1] - 4,
            agentStartCoords[0] + 4, agentStartCoords[1] + 4,
            fill='blue', outline='blue')

        # Filling the route
        for j in range(len(self.f)):
            # Showing the coordinates of the final route
            print(self.f[j])
            self.track = self.canvas_widget.create_oval(
                self.f[j][0] - 3 + self.o[0] - 4, self.f[j][1] - 3 + self.o[1] - 4,
                self.f[j][0] - 3 + self.o[0] + 4, self.f[j][1] - 3 + self.o[1] + 4,
                fill='blue', outline='blue')
            # Writing the final route in the global variable a
            a[j] = self.f[j]


# Returning the final dictionary with route coordinates
# Then it will be used in agent_brain.py
def final_states():
    return a


# This we need to debug the environment
# If we want to run and see the environment without running full algorithm
if __name__ == '__main__':
    env = Environment()
    env.mainloop()
