import tkinter as tk
import numpy as np
from itertools import cycle

class window(tk.Frame):
    def __init__(self, master=None):
            self.PLAYING = False

            self.robotSize = 150

            self.poses = [(90, 450, 0)] #[(90, 450, 0), (250, 450, 0), (250, 200, np.deg2rad(-90)), (450, 200, np.deg2rad(-90)), (450, 900, np.deg2rad(-90))]

            self.robotPose = self.poses[0]

            tk.Frame.__init__(self, master)
            self.grid()

            self.menu = tk.Frame(self, highlightbackground="black", highlightthickness=1)
            self.menu.grid(column=0, row=1, sticky=tk.N)

            self.draw = tk.Button(self, text="Draw", command=self.draw)
            self.draw.grid(row=0, column=1, sticky=tk.W)

            self.drawing = False

            self.play = tk.Button(self.menu, text="Play", command=self.play)
            self.pause = tk.Button(self.menu, text="Pause", command=self.pause)
            self.stop = tk.Button(self.menu, text="Stop", command=self.stop)
            self.save = tk.Button(self.menu, text="Save")
            self.load = tk.Button(self.menu, text="Load")
            self.export = tk.Button(self.menu, text="Export")

            self.save.grid(row=0, column=0)
            self.load.grid(row=0, column=1)
            self.play.grid(row=1, column=0)
            self.pause.grid(row=1, column=1)
            self.stop.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.E+tk.S+tk.W)
            self.export.grid(row=3, column=0, columnspan=2, sticky=tk.N+tk.E+tk.S+tk.W)

            self.field = tk.Canvas(self, width=1080, height=1080, bg="gray")
            self.field.grid(column=1, row=1, rowspan=2)

            self.fieldImg = tk.PhotoImage(file="field_resize.png")
            self.field.create_image(0, 0, anchor=tk.NW, image=self.fieldImg)

            self.activeLine = self.field.create_line((0, 0), (0, 0), width=2)

            self.lastClick = (self.robotPose[0], self.robotPose[1])
            self.field.bind("<Button-1>", self.canvasClick)
            self.field.bind("<Motion>", self.canvasMouseMove)

            self.drawPoses(self.poses)
            
            self.path = cycle(self.genPath(self.poses))

            self.drawRobot(self.robotPose)

    def draw(self):
        self.drawing = not self.drawing
        if self.drawing:
            self.draw.config(relief=tk.SUNKEN)
        else:
            self.draw.config(relief=tk.RAISED)

            self.field.delete(self.activeLine)
            self.activeLine = self.field.create_line((0,0), (0,0), width=2)
    
    def canvasMouseMove(self, event):
        if self.drawing:
            self.field.delete(self.activeLine)
            self.activeLine = self.field.create_line(self.lastClick, (event.x, event.y), width=2)

    def lerp(self, a, b, t): return a + (b-a) * t

    def canvasClick(self, event):
        if self.drawing:
            self.lastClick = (event.x, event.y)
            print(self.lastClick)
            self.poses.append((event.x, event.y, 0))
            self.drawPoses(self.poses)

    def genPath(self, poses):
        out = []
        for p in range(len(poses)-1):
            pose = (self.poses[p][0], self.poses[p][1], self.poses[p][2])
            nextPose = (self.poses[p+1][0], self.poses[p+1][1], self.poses[p+1][2])
            for i in range(100):
                out.append((self.lerp(pose[0], nextPose[0], i/100), self.lerp(pose[1], nextPose[1], i/100), self.lerp(pose[2], nextPose[2], i/100)))
        
        return out
    
    def drawPoses(self, poses):
        if len(poses) > 1: 
            for p in range(len(poses)-1):
                pose = (poses[p][0], poses[p][1])
                nextPose = (poses[p+1][0], poses[p+1][1])
                self.field.create_line(pose, nextPose, width=2)

    def drawRobot(self, robotPose):
        r = np.sqrt(np.pow(self.robotSize, 2)/2)

        pt1 = (r * np.cos((1 * np.pi)/4 + robotPose[2]) + robotPose[0], r * np.sin((1 * np.pi)/4 + robotPose[2]) + robotPose[1])
        pt2 = (r * np.cos((3 * np.pi)/4 + robotPose[2]) + robotPose[0], r * np.sin((3 * np.pi)/4 + robotPose[2]) + robotPose[1])
        pt3 = (r * np.cos((5 * np.pi)/4 + robotPose[2]) + robotPose[0], r * np.sin((5 * np.pi)/4 + robotPose[2]) + robotPose[1])
        pt4 = (r * np.cos((7 * np.pi)/4 + robotPose[2]) + robotPose[0], r * np.sin((7 * np.pi)/4 + robotPose[2]) + robotPose[1])

        center = (robotPose[0], robotPose[1])

        self.robot = self.field.create_polygon(pt1, pt2, pt3, pt4, ((pt1[0]+pt4[0])/2, (pt1[1]+pt4[1])/2), center, ((pt1[0]+pt4[0])/2, (pt1[1]+pt4[1])/2), fill='', outline="black", width=3)
    
    def play(self):
        if not self.PLAYING:
            self.path = cycle(self.genPath(self.poses))
            self.PLAYING = True
            self.moveRobot()

    def pause(self):
        self.PLAYING = False
    
    def stop(self):
        self.PLAYING = False
        self.robotPose = self.poses[0]
        self.field.delete(self.robot)
        self.drawRobot(self.robotPose)
        self.path = cycle(self.genPath(self.poses))

    def moveRobot(self):
        if(self.PLAYING):
            self.field.delete(self.robot)
            self.robotPose = next(self.path)
            self.drawRobot(self.robotPose)
            self.field.after(10, self.moveRobot)
        
main = window()
main.master.title("Path Plotter")
main.mainloop()
