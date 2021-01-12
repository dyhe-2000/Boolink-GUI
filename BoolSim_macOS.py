# warning about specific nodes
# drag
# write instructions
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
#from matplotlib import style


import tkinter as tk
from tkinter import ttk
from tkinter import *

import urllib
import urllib.request
import json

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import matplotlib.pyplot as plt

import subprocess
import sys, os, getopt
import time

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

orange_bkg = '#ffcc99'
blue_bkg = '#99ccff'

HEIGHT=400
WIDTH=400

style.use("ggplot")

f = Figure()
a = f.add_subplot(111)

def popupmsg(msg):
    popup = tk.Tk()
    
    def leavemini():
        popup.destroy()
    
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = leavemini)
    B1.pack()
    #popup.mainloop()
    
#=================================================================================
# core update function
def animate(i):
    pullData = open("ploting points file.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x, y = eachLine.split(' ')
            xList.append(float(x))
            yList.append(float(y))
            
    a.clear()
    a.plot(xList, yList)
    
    #a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
    
    title = "The curve shows out of n initializations, the percentage of closure is 1 at each time step."
    a.set_title(title)
    
#=================================================================================

def setFile(s, fileName):
    f = open(fileName, 'r+')
    f.truncate(0) # need '0' when using r+
    f.close()
    
    file1 = open(fileName, "a")  # append mode 
    file1.write(str(s))
    file1.close() 
    
def clearFileAndQuit(fileName):
    f = open(fileName, 'r+')
    f.truncate(0) # need '0' when using r+
    f.close()
    quit
    
eachNodeColor = []

class Boolean_Network_App(tk.Tk):
    #self is implied
    def __init__(self, *args, **kwargs):
        global eachNodeColor
        
        file1 = open('eachNodeColor.txt', 'r') 
        eachNodeColor = file1.read().splitlines()
        
        
        
        self.network = []
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        #tk.Tk.iconbitmap(self, default="Capture.ico") # change icon
        tk.Tk.wm_title(self,"BoolSim") # change title
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported just yet!"))
        #filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        # inputStateChoice = tk.Menu(menubar, tearoff=0)
        # inputStateChoice.add_command(label="Set To 1", command=lambda: setFile(1,"Input Setting.txt"))
        # inputStateChoice.add_command(label="Set To 0", command=lambda: setFile(0,"Input Setting.txt"))
        
        # menubar.add_cascade(label="Set Input Node State", menu=inputStateChoice)
        

        nodes = NetDropDown(menubar)
        eqns = BoolEqns(menubar)
        menubar.add_cascade(label='Network', menu=nodes.netmenu)
        menubar.add_cascade(label='Connections', menu=eqns.eqnmenu)

        initializationChoice = tk.Menu(menubar, tearoff=0)
        initializationChoice.add_command(label = "1 Initialization", command=lambda: setFile(1, "Initialization Setting.txt"))
        initializationChoice.add_command(label = "10 Initializations", command=lambda: setFile(10, "Initialization Setting.txt"))
        initializationChoice.add_command(label = "50 Initializations", command=lambda: setFile(50, "Initialization Setting.txt"))
        initializationChoice.add_command(label = "100 Initializations", command=lambda: setFile(100, "Initialization Setting.txt"))
        initializationChoice.add_command(label = "500 Initializations", command=lambda: setFile(500, "Initialization Setting.txt"))
        initializationChoice.add_command(label = "1000 Initializations", command=lambda: setFile(1000, "Initialization Setting.txt"))
        initializationChoice.add_command(label = "1500 Initializations", command=lambda: setFile(1500, "Initialization Setting.txt"))
        initializationChoice.add_command(label = "2500 Initializations", command=lambda: setFile(2500, "Initialization Setting.txt"))
        initializationChoice.add_command(label = "input arbitrary initializations", command=lambda: setArbitraryInitializations(self))
        menubar.add_cascade(label = "Set Simulation Initializations", menu = initializationChoice)
        
        timeStepChoice = tk.Menu(menubar, tearoff=0)
        timeStepChoice.add_command(label = "1 time step", command=lambda: setFile(1, "Time Steps Setting.txt"))
        timeStepChoice.add_command(label = "10 time steps", command=lambda: setFile(10, "Time Steps Setting.txt"))
        timeStepChoice.add_command(label = "20 time steps", command=lambda: setFile(20, "Time Steps Setting.txt"))
        timeStepChoice.add_command(label = "50 time steps", command=lambda: setFile(50, "Time Steps Setting.txt"))
        timeStepChoice.add_command(label = "input arbitrary time steps", command=lambda: setArbitraryTimeSteps(self))
        menubar.add_cascade(label = "Set Simulation time step", menu = timeStepChoice)
        
        specificNodeToAnalyze = tk.Menu(menubar, tearoff=0)
        specificNodeToAnalyze.add_command(label = "set node", command=lambda: setANode(self))
        menubar.add_cascade(label = "Set nodes to see their graphical result", menu = specificNodeToAnalyze)
        
        tk.Tk.config(self, menu=menubar)
        
        self.frames = {}
        
        for F in (StartPage, HomePage, GraphPage, RelationalModelGraphPage):
        
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column = 0, sticky="nsew")
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        #print(frame.getType()
        if frame.getType() == "GraphPage":
            popupmsg("Make sure you have set nodes to see their graphical result\nalways hit the refresh button before reading, just do it since many things are related\nthat's it, everytime you done a simulation, adjusted some specific nodes settings, and ready to read graph, hit refresh first")
            runParseResultAndShowGraph()
        frame.tkraise()
        
#=================================================================================  
def setANode(self):      
    self.root_new = tk.Tk()
    self.root_new.wm_title("Adding Nodes")
    self.canvas_new = tk.Canvas(self.root_new, width=WIDTH, height=HEIGHT/4)
    self.canvas_new.pack()
    
    self.frame_new = tk.Frame(self.canvas_new, bg=blue_bkg, bd=10)
    self.frame_new.place(relwidth=1, relheight=1)
    
    self.entry_new = tk.Entry(self.frame_new, font=30)
    self.entry_new.place(relx=0.1, rely=0.1, relwidth=0.5, relheight=0.35)    
    
    self.button_new = tk.Button(self.frame_new, text='Add', font=30, command=lambda: setSpecificNode(self))
    self.button_new.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.35)        
                
    self.root_new.mainloop()
    
# this function can also modefy a node's state
def setSpecificNode(self):
    s = self.entry_new.get()
    
    self.network.clear()
    f = open('specific node.txt', 'r+')
    f.truncate(0) # need '0' when using r+
    f.close()
    
    file1 = open("specific node.txt", "a")  # append mode 
    file1.write(s)
    file1.close() 
    self.entry_new.delete(0, len(s))
#=================================================================================  
def setArbitraryInitializations(self):
    self.root_new = tk.Tk()
    self.root_new.wm_title("input arbitrary initializations, only number input is valid")
    self.canvas_new = tk.Canvas(self.root_new, width=WIDTH, height=HEIGHT/4)
    self.canvas_new.pack()
    
    self.frame_new = tk.Frame(self.canvas_new, bg=blue_bkg, bd=10)
    self.frame_new.place(relwidth=1, relheight=1)
    
    self.entry_new = tk.Entry(self.frame_new, font=30)
    self.entry_new.place(relx=0.1, rely=0.1, relwidth=0.5, relheight=0.35)    
    
    self.button_new = tk.Button(self.frame_new, text='Add', font=30, command=lambda: setSpecificInitializations(self))
    self.button_new.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.35)        
                
    self.root_new.mainloop()
    
def setSpecificInitializations(self):
    s = self.entry_new.get()
    #print(s)
    setFile(s, "Initialization Setting.txt")
    self.entry_new.delete(0, len(s))
    
#=================================================================================  
def setArbitraryTimeSteps(self):
    self.root_new = tk.Tk()
    self.root_new.wm_title("input arbitrary time steps, only number input is valid")
    self.canvas_new = tk.Canvas(self.root_new, width=WIDTH, height=HEIGHT/4)
    self.canvas_new.pack()
    
    self.frame_new = tk.Frame(self.canvas_new, bg=blue_bkg, bd=10)
    self.frame_new.place(relwidth=1, relheight=1)
    
    self.entry_new = tk.Entry(self.frame_new, font=30)
    self.entry_new.place(relx=0.1, rely=0.1, relwidth=0.5, relheight=0.35)    
    
    self.button_new = tk.Button(self.frame_new, text='Add', font=30, command=lambda: setSpecificTimeSteps(self))
    self.button_new.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.35)        
                
    self.root_new.mainloop()
    
def setSpecificTimeSteps(self):
    s = self.entry_new.get()
    #print(s)
    setFile(s, "Time Steps Setting.txt")
    self.entry_new.delete(0, len(s))




class NetDropDown(tk.Tk):
    def __init__(self, parent):        
        self.network = []
        
        self.netmenu = tk.Menu(parent, tearoff=0)
        self.netmenu.add_command(label='Add Node', command=lambda:self.NewNodePopUp())
        #self.netmenu.add_command(label='Remove Node', command=lambda:self.RemoveNodePopUp())
        #self.netmenu.add_command(label='Print Network', command=lambda:self.PrintNetPopUp())
        #self.netmenu.add_command(label='Clear Network Nodes', command=lambda:self.ClearNetWorks())

        
    def NewNodePopUp(self):      
        self.root_new = tk.Tk()
        self.root_new.wm_title("Adding Nodes")
        self.canvas_new = tk.Canvas(self.root_new, width=WIDTH, height=HEIGHT/4)
        self.canvas_new.pack()
        
        self.frame_new = tk.Frame(self.canvas_new, bg=blue_bkg, bd=10)
        self.frame_new.place(relwidth=1, relheight=1)
        
        self.entry_new = tk.Entry(self.frame_new, font=30)
        self.entry_new.place(relx=0.1, rely=0.1, relwidth=0.5, relheight=0.35)    
        
        self.button_new = tk.Button(self.frame_new, text='Add', font=30, command=lambda:self.AddNode())
        self.button_new.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.35)        
                    
        self.root_new.mainloop()
        
    # this function can also modefy a node's state
    def AddNode(self):
        s = self.entry_new.get()
        
        self.network.clear()
        f = open('Node Name and their initial state.txt', 'r+')
        f.truncate(0) # need '0' when using r+
        f.close()
        
        #print(s)
        
        # pullData = open("Node Name and their initial state.txt","r").read()
        # dataList = pullData.split('\n')
        # for eachLine in dataList: #iterate through all items in the file
            # x = eachLine.split(' ')
            # print(x[0])
            # theList = s.split('\n')
                # for eachIt in theList: #iterate through all items in the input
                # y = eachIt.split(' ')
                # if x[0] == y[0]:
                    # eachLine = eachIt
                    
                    
        enteredListSplitByLine = s.splitlines(True) # with /n at the end
        eachElementIsAListOfStr = []
        global eachNodeColor
        eachNodeColor.clear()
        for a in range(len(enteredListSplitByLine)):
            #print(enteredListSplitByLine[a].split())
            eachElementIsAListOfStr.append(enteredListSplitByLine[a].split())
            #print(len(enteredListSplitByLine[a]))
            #print(enteredListSplitByLine[a][len(enteredListSplitByLine[a])-1] == '\n') #print last char
            
        #print(eachElementIsAListOfStr)
        
        file1 = open("Node Name and their initial state.txt", "a")  # append mode 
        
        for a in range(len(eachElementIsAListOfStr)): # iterate through all the string list
            print(eachElementIsAListOfStr[a])
            
            if len(eachElementIsAListOfStr[a]) >= 2: # node name, optional init state, optional color
                if a != len(eachElementIsAListOfStr) - 1:
                    if "red" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1] or "yellow" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1] or "blue" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1] or "pink" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1] or "green" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1] or "purple" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1]:
                        eachNodeColor.append(eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1])
                        eachElementIsAListOfStr[a].pop()
                        # the following for loop writes the str list for each element separate by space, last element followed by \n
                        for b in range (len(eachElementIsAListOfStr[a])):
                            if b != len(eachElementIsAListOfStr[a]) - 1:
                                file1.write(eachElementIsAListOfStr[a][b])
                                file1.write(' ')
                            elif b == len(eachElementIsAListOfStr[a]) - 1:
                                file1.write(eachElementIsAListOfStr[a][b])
                                file1.write('\n')
                    else:
                        eachNodeColor.append("yellow")
                        # the following for loop writes the str list for each element separate by space, last element followed by \n
                        for b in range (len(eachElementIsAListOfStr[a])):
                            if b != len(eachElementIsAListOfStr[a]) - 1:
                                file1.write(eachElementIsAListOfStr[a][b])
                                file1.write(' ')
                            elif b == len(eachElementIsAListOfStr[a]) - 1:
                                file1.write(eachElementIsAListOfStr[a][b])
                                file1.write('\n')
                if a == len(eachElementIsAListOfStr) - 1:
                    if "red" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1] or "yellow" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1] or "blue" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1] or "pink" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1] or "green" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1] or "purple" == eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1]:
                        eachNodeColor.append(eachElementIsAListOfStr[a][len(eachElementIsAListOfStr[a]) - 1])
                        eachElementIsAListOfStr[a].pop()
                        # the following for loop writes the str list for each element separate by space
                        for b in range (len(eachElementIsAListOfStr[a])):
                            if b != len(eachElementIsAListOfStr[a]) - 1:
                                file1.write(eachElementIsAListOfStr[a][b])
                                file1.write(' ')
                            elif b == len(eachElementIsAListOfStr[a]) - 1:
                                file1.write(eachElementIsAListOfStr[a][b])
                    else:
                        eachNodeColor.append("yellow")
                        # the following for loop writes the str list for each element separate by space, last element followed by \n
                        for b in range (len(eachElementIsAListOfStr[a])):
                            if b != len(eachElementIsAListOfStr[a]) - 1:
                                file1.write(eachElementIsAListOfStr[a][b])
                                file1.write(' ')
                            elif b == len(eachElementIsAListOfStr[a]) - 1:
                                file1.write(eachElementIsAListOfStr[a][b])
            else:
                eachNodeColor.append("yellow")
                
                if a != len(eachElementIsAListOfStr) - 1:
                    # the following for loop writes the str list for each element separate by space, last element followed by \n
                    for b in range (len(eachElementIsAListOfStr[a])):
                        if b != len(eachElementIsAListOfStr[a]) - 1:
                            file1.write(eachElementIsAListOfStr[a][b])
                            file1.write(' ')
                        elif b == len(eachElementIsAListOfStr[a]) - 1:
                            file1.write(eachElementIsAListOfStr[a][b])
                            file1.write('\n')
                if a == len(eachElementIsAListOfStr) - 1:
                    for b in range (len(eachElementIsAListOfStr[a])):
                        if b != len(eachElementIsAListOfStr[a]) - 1:
                            file1.write(eachElementIsAListOfStr[a][b])
                            file1.write(' ')
                        elif b == len(eachElementIsAListOfStr[a]) - 1:
                            file1.write(eachElementIsAListOfStr[a][b])
                           
                
        
        
        
        file1.close()
        
        f = open('eachNodeColor.txt', 'r+')
        f.truncate(0) # need '0' when using r+
        f.close()

        file1 = open("eachNodeColor.txt", "a")
        for a in range(len(eachNodeColor)):
            if a != len(eachNodeColor) - 1:
                file1.write(eachNodeColor[a])
                file1.write('\n')
            if a == len(eachNodeColor) - 1:
                file1.write(eachNodeColor[a])
        
        
        self.network.append(s)
        self.entry_new.delete(0, len(s))
        self.label_new = tk.Label(self.frame_new, text='Added {}'.format(s), font=30)
        self.label_new.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.35)
        
    def RemoveNodePopUp(self):
        self.root_rmv = tk.Tk()
        self.canvas_rmv = tk.Canvas(self.root_rmv, width=WIDTH, height=HEIGHT/4)
        self.canvas_rmv.pack()
        
        self.frame_rmv = tk.Frame(self.canvas_rmv, bg=blue_bkg, bd=10)
        self.frame_rmv.place(relwidth=1, relheight=1)
        
        self.entry_rmv = tk.Entry(self.frame_rmv, font=30)
        self.entry_rmv.place(relx=0.1, rely=0.1, relwidth=0.5, relheight=0.35)    
        
        self.button_rmv = tk.Button(self.frame_rmv, text='Remove', font=30, command=lambda:self.RemoveNode())
        self.button_rmv.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.35)        
                    
        self.root_rmv.mainloop()
        
    def RemoveNode(self):
        s = self.entry_rmv.get()
        try:
            self.network.remove(s)
            self.entry_rmv.delete(0, len(s))
            self.label_rmv = tk.Label(self.frame_rmv, text='Removed {}'.format(s), font=30)
            self.label_rmv.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.35)
        except:
            self.entry_rmv.delete(0, len(s))
            self.label_rmv = tk.Label(self.frame_rmv, text='No {} in the network'.format(s), font=30)
            self.label_rmv.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.35)
        
    def PrintNetPopUp(self):
        self.root_print = tk.Tk()
        self.canvas_print = tk.Canvas(self.root_print, width=WIDTH, height=HEIGHT)
        self.canvas_print.pack()
        
        self.frame_print = tk.Frame(self.canvas_print, bg=blue_bkg, bd=10)
        self.frame_print.place(relwidth=1, relheight=1)
        
        self.PrintNet()        
        self.root_print.mainloop()

    def PrintNet(self):        
        self.label_print_title = tk.Label(self.frame_print, text='List of nodes in the network', font=30)
        self.label_print_title.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.1)
        
        self.button_print = tk.Button(self.frame_print, text='Refresh', font=30, command=lambda:self.PrintNet())
        self.button_print.place(relx=0.3, rely=0.20, relwidth=0.4, relheight=0.1)
        
        disp = ''
        for w in self.network:
            #print(w)
            disp += w+'\n'
        
        self.label_print = tk.Label(self.frame_print, text=disp, font=30)
        self.label_print.place(relx=0.05, rely=0.35, relheight=0.6, relwidth=0.9) 
     
    def ClearNetWorks(self):
        self.network.clear()
        f = open('Node Name and their initial state.txt', 'r+')
        f.truncate(0) # need '0' when using r+
        f.close()
        
class BoolEqns(tk.Tk):
    def __init__(self, parent):
        
        self.eqnmenu = tk.Menu(parent, tearoff=0)
        self.eqnmenu.add_command(label='Add Eqns In Index Form', command=lambda: self.NewEqnPopUp())
        self.eqnmenu.add_command(label='Add Eqns In Word Form', command=lambda: self.NewEqnPopUpWord())
        
    def NewEqnPopUp(self):
        self.root_new = tk.Tk()
        self.root_new.wm_title("Adding Eqns")
        self.canvas_new = tk.Canvas(self.root_new, width=WIDTH, height=HEIGHT/4)
        self.canvas_new.pack()
        
        self.frame_new = tk.Frame(self.canvas_new, bg=blue_bkg, bd=10)
        self.frame_new.place(relwidth=1, relheight=1)
        
        self.entry_new = tk.Entry(self.frame_new, font=30)
        self.entry_new.place(relx=0.1, rely=0.1, relwidth=0.5, relheight=0.35)    
        
        self.button_new = tk.Button(self.frame_new, text='Add', font=30, command=lambda:self.AddEqn())
        self.button_new.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.35)        
                    
        self.root_new.mainloop()
        
    def NewEqnPopUpWord(self):
        self.root_new = tk.Tk()
        self.root_new.wm_title("Adding Eqns")
        self.canvas_new = tk.Canvas(self.root_new, width=WIDTH, height=HEIGHT/4)
        self.canvas_new.pack()
        
        self.frame_new = tk.Frame(self.canvas_new, bg=blue_bkg, bd=10)
        self.frame_new.place(relwidth=1, relheight=1)
        
        self.entry_new = tk.Entry(self.frame_new, font=30)
        self.entry_new.place(relx=0.1, rely=0.1, relwidth=0.5, relheight=0.35)    
        
        self.button_new = tk.Button(self.frame_new, text='Add', font=30, command=lambda:self.AddEqnWord())
        self.button_new.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.35)        
                    
        self.root_new.mainloop()
        
    def AddEqn(self):
        s = self.entry_new.get()
        
        f = open('Boolean Equations File.txt', 'r+')
        f.truncate(0) # need '0' when using r+
        
        #print(s)
        
        # pullData = open("Node Name and their initial state.txt","r").read()
        # dataList = pullData.split('\n')
        # for eachLine in dataList: #iterate through all items in the file
            # x = eachLine.split(' ')
            # print(x[0])
            # theList = s.split('\n')
                # for eachIt in theList: #iterate through all items in the input
                # y = eachIt.split(' ')
                # if x[0] == y[0]:
                    # eachLine = eachIt
                    
                    
            
        file1 = open("Boolean Equations File.txt", "a")  # append mode 
        file1.write(s)
        file1.close() 
        
        self.entry_new.delete(0, len(s))
        self.label_new = tk.Label(self.frame_new, text='Added {}'.format(s), font=30)
        self.label_new.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.35) 
        
        
    def AddEqnWord(self):
        s = self.entry_new.get()
        
        f = open('Word Boolean Equations File.txt', 'r+')
        f.truncate(0) # need '0' when using r+
        
        #print(s)
        
        # pullData = open("Node Name and their initial state.txt","r").read()
        # dataList = pullData.split('\n')
        # for eachLine in dataList: #iterate through all items in the file
            # x = eachLine.split(' ')
            # print(x[0])
            # theList = s.split('\n')
                # for eachIt in theList: #iterate through all items in the input
                # y = eachIt.split(' ')
                # if x[0] == y[0]:
                    # eachLine = eachIt
                    
                    
            
        file1 = open("Word Boolean Equations File.txt", "a")  # append mode 
        file1.write(s)
        file1.close() 
        
        self.entry_new.delete(0, len(s))
        self.label_new = tk.Label(self.frame_new, text='Added {}'.format(s), font=30)
        self.label_new.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.35) 
        exec(open("word_eqn_parser.py").read())

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("""Boolean Network GUI Application
        use at your own risk. There is no promise of warranty
        
        Instructions: 
        1. Simulate after setting nodes and boolean equations
        2. Input node is always assumed to be in the network, do not need to insert input node
        3. Input node is default 1, change it's initial state through interface after agreeing
        4. Once add nodes or eqns, whole network is destroyed and started over, so change both nodes and eqns
        5. When running the simulation, please be patient, while it is running, the application will freeze, after it is done, you can see results"""), font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        
        button1 = ttk.Button(self, text="Agree",
                            command = lambda: controller.show_frame(HomePage))
        button1.pack()
        
        button2 = ttk.Button(self, text="Disagree",
                            command = quit)
        button2.pack()
        
    def getType(self):
        return "StartPage"
       
        
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Boolean Network Home Page", font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        
        button1 = ttk.Button(self, text="Back to Start Page",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        
        button3 = ttk.Button(self, text="See graphical network",
                            command = lambda: controller.show_frame(RelationalModelGraphPage))
        button3.pack()
        
        button4 = ttk.Button(self, text="Start Simulate Process",
                            command = lambda: runSimulationCpp("Biology_Binary_Project.cpp", "Biology_Binary_Project.exe"))
        button4.pack()
        
        button2 = ttk.Button(self, text="See graphical analysis from simulation",
                            command = lambda: controller.show_frame(GraphPage))
        button2.pack()
        
        
        
        #button5 = ttk.Button(self, text="See Result", command = lambda: os.system("notepad.exe Result.txt"))
        #button5.pack()
    def getType(self):
        return "HomePage"
        

# graph page        
class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        
        button1 = ttk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(HomePage))
        button1.pack()
        
        button2 = ttk.Button(self, text="Refresh",
                            command = lambda: self.reload())
        button2.pack()
        
        
        #======================================================================================================================
        #interactive plot updated in real time code
        
        # canvas = FigureCanvasTkAgg(f, self)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        
        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        #======================================================================================================================
        

        # f = Figure(figsize=(5,5), dpi=100)
        # a = f.add_subplot(111)
        # a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        ## LOADING STUFF
        # file that contains all node names
        f_all_node_name = open('Node Name and their initial state.txt', 'r')

        # load the result array
        try:
            bool_net = np.load('net_after_parsing.npy')
        except:
            return

        # file that has names of nodes to plot
        f_plot_node_name = open('specific node.txt', 'r')


        ## PROCESSING DATA
        # make a dictionary with node names
        all_nodes = []
        for line in f_all_node_name:
            for i in range(len(line)):
                if(line[i] in [' ', '\n']):
                    s = line[0:i].strip()
                    if(len(s)):
                        all_nodes.append(s)
                    break
            
        num2name = dict([(i,all_nodes[i]) for i in range(len(all_nodes))])
        name2num = dict([(all_nodes[i],i) for i in range(len(all_nodes))])

        # read which nodes you want to plot
        plot_nodes = []
        for line in f_plot_node_name:
            s = line.strip()
            if(len(s)):
                plot_nodes.append(s)  
                
        plt.clf()
        plt.figure(1)
        f = plt.figure(1)
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                
        # some tests on all_nodes and plot_nodes
        if(len(plot_nodes)==0):
            return
            sys.exit('No node names to plot.')
            
        for n in plot_nodes:
            if(n not in all_nodes):
                return
                sys.exit('{} not found in the set of nodes. (Check spelling and formatting.)'.format(n))
                
        # passed the tests!

        # PLOT
        t_list = range(bool_net.shape[1])   # points on time-axis
        init_cond = bool_net.shape[0]       # number of initial conditions
        try: 
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError: 
            pass
        plt.clf()
        plt.figure(1)
        for n in plot_nodes:
            avg_act = 100*np.sum(bool_net[:,:,name2num[n]], axis=0)/init_cond
            plt.plot(t_list, avg_act)
            
        plt.xlabel('Time')
        plt.ylabel('Activity percentage')
        plt.xticks(range(0,1+bool_net.shape[1],4))
        plt.yticks(range(0,101,20))
        plt.legend(plot_nodes)
        f = plt.figure(1)
        
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def reload(self):
        ## LOADING STUFF
        # file that contains all node names
        f_all_node_name = open('Node Name and their initial state.txt', 'r')

        # load the result array
        #bool_net = np.load('net_after_parsing.npy')
        try:
            bool_net = np.load('net_after_parsing.npy')
        except:
            return

        # file that has names of nodes to plot
        f_plot_node_name = open('specific node.txt', 'r')


        ## PROCESSING DATA
        # make a dictionary with node names
        all_nodes = []
        for line in f_all_node_name:
            for i in range(len(line)):
                if(line[i] in [' ', '\n']):
                    s = line[0:i].strip()
                    if(len(s)):
                        all_nodes.append(s)
                    break
            
        num2name = dict([(i,all_nodes[i]) for i in range(len(all_nodes))])
        name2num = dict([(all_nodes[i],i) for i in range(len(all_nodes))])

        # read which nodes you want to plot
        plot_nodes = []
        for line in f_plot_node_name:
            s = line.strip()
            if(len(s)):
                plot_nodes.append(s)   
                
        # some tests on all_nodes and plot_nodes
        if(len(plot_nodes)==0):
            return
            sys.exit('No node names to plot.')
            
        for n in plot_nodes:
            if(n not in all_nodes):
                return
                sys.exit('{} not found in the set of nodes. (Check spelling and formatting.)'.format(n))
                
        # passed the tests!

        # PLOT
        t_list = range(bool_net.shape[1])   # points on time-axis
        init_cond = bool_net.shape[0]       # number of initial conditions
        try: 
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError: 
            pass
        plt.clf()
        plt.figure(1)
        for n in plot_nodes:
            avg_act = 100*np.sum(bool_net[:,:,name2num[n]], axis=0)/init_cond
            plt.plot(t_list, avg_act)
            
        plt.xlabel('Time')
        plt.ylabel('Activity percentage')
        plt.xticks(range(0,1+bool_net.shape[1],4))
        plt.yticks(range(0,101,20))
        plt.legend(plot_nodes)
        f = plt.figure(1)
        
        self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        
        
        
    def getType(self):
        return "GraphPage"

w = 1400
h = 600
x = w/2
y = h/2

# relational model graph page        
class RelationalModelGraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Relational Model Graph Page!", font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        
        button1 = ttk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(HomePage))
        button1.pack()   

        button2 = ttk.Button(self, text="Refresh",
                            command = lambda: self.reload())
        button2.pack()
        
        self.my_canvas = Canvas(self, width=w, height=h, bg="White")
        self.my_canvas.pack(pady=20)
        
        self.reload()
        
        self.movingNode = 0
        self.movingConnections = []
        self.movingNotConnections = []
        
        
    def getType(self):
        return "RelationalModelGraphPage"
        
    def reload(self):   
        #print("in reload function")
        self.my_canvas.delete("all")
        
        # self.my_line = self.my_canvas.create_line(x,y, x, y, fill="red")
        # self.my_circle = self.my_canvas.create_oval(x-30, y-30, x+30, y+30, fill="yellow")
        # self.my_text = self.my_canvas.create_text(x,y,text="mytext")
        
        self.nodeNames = []
        self.eqns = []
        self.notEqns = []
        
        self.nodeCircles = []
        self.nodeTexts = []
        self.nodeConnections = []
        self.nodeNotConnections = []
        
        for it in self.nodeCircles:
            self.my_canvas.delete(it)
            
        for it in self.nodeTexts:
            self.my_canvas.delete(it)
            
        for it in self.nodeConnections:
            self.my_canvas.delete(it)
        
        self.nodeNames.clear()
        self.eqns.clear()
        
        self.nodeCircles.clear()
        self.nodeTexts.clear()
        self.nodeConnections.clear()
        
        pullData = open("Node Name and their initial state.txt","r").read()
        dataList = pullData.split('\n')
        for eachLine in dataList: #iterate through all items in the file
            nodeName = eachLine.split(' ')
            self.nodeNames.append(nodeName[0])
            
        # print("nodeNames array")
        # for a in range(len(self.nodeNames)):
            # print(str(a))
            # print(self.nodeNames[a])
            
        pullEqns = open("Boolean Equations File.txt","r").read()
        tempEqns = pullEqns.split('\n') # a list of string eqns
        
        
        for a in range(len(tempEqns)): # iterate through all the string eqns in the list
            #print(tempEqns[a]) # one single string eqn for node index a
            tempStr = []
            tempStr.clear()
            for charIndex in range(len(tempEqns[a])):
                #print(self.eqns[a][charIndex])
                if tempEqns[a][charIndex] == '|' or tempEqns[a][charIndex] == '&' or tempEqns[a][charIndex] == '~':
                    tempStr.append(' ')
                else:
                    tempStr.append(tempEqns[a][charIndex])
            #print("".join(tempStr))
            self.eqns.append("".join(tempStr))
            
        for a in range(len(self.eqns)):
            #print(self.eqns[a])
            numberList = [int(s) for s in self.eqns[a].split() if s.isdigit()]
            self.eqns[a] = numberList
            
        try:
            while(len(self.eqns[len(self.eqns) - 1]) == 0):
                self.eqns.pop()
        except:
            pass

        
        # print("eqns array")
        # for a in range(len(self.eqns)):
            # print(self.eqns[a]) # at this point, each element in seld.eqns is a list, starting with node index 1, the nodes related with 
            
        tempEqns1 = pullEqns.split('\n') # a list of string eqns
        
        for a in range(len(tempEqns1)): # iterate through all the string eqns in the list
            #print(tempEqns[a]) # one single string eqn for node index a
            tempStr = []
            tempStr.clear()
            notStarted = False
            for charIndex in range(len(tempEqns[a])):
                #print(self.eqns[a][charIndex])
                
                if tempEqns[a][charIndex] == '|' or tempEqns[a][charIndex] == '&':
                    notStarted = False
                    tempStr.append(' ')
                elif tempEqns[a][charIndex] == '~':
                    notStarted = True
                    tempStr.append(' ')
                    continue
                if notStarted:
                    tempStr.append(tempEqns[a][charIndex])
            #print("".join(tempStr))
            self.notEqns.append("".join(tempStr))
        
        for a in range(len(self.notEqns)):
            #print(self.eqns[a])
            numberList = [int(s) for s in self.notEqns[a].split() if s.isdigit()]
            self.notEqns[a] = numberList
        
        while(len(self.notEqns) != len(self.eqns)):
            self.notEqns.pop()
        
        #not eqns is goood
        # print("notEqns array")
        # for a in range(len(self.notEqns)):
            # print(str(a))
            # print(self.notEqns[a]) 
       
        
        global eachNodeColor
        
        # print("len(self.nodeNames)" + str(len(self.nodeNames)))
        # print("len(self.eqns)" + str(len(self.eqns)))
        # print("len(self.notEqns)" + str(len(self.notEqns)))
        
        
        '''
        for a in range(len(self.nodeNames)+1):
            xpos = (a%15)*80 + 60
            ypos = int(a/15)*80 + 60
            if a == 0:
                self.nodeCircles.append(self.my_canvas.create_oval(xpos-30, ypos-30, xpos+30, ypos+30, fill="yellow"))
                self.nodeTexts.append(self.my_canvas.create_text(xpos,ypos,text="input"))
                # self.nodeCircles.append(none)
                # self.nodeTexts.append(none)
                continue
            self.nodeCircles.append(self.my_canvas.create_oval(xpos-30, ypos-30, xpos+30, ypos+30, fill=eachNodeColor[a-1]))
            self.nodeTexts.append(self.my_canvas.create_text(xpos,ypos,text=self.nodeNames[a-1]))
            
        for a in range(len(self.eqns)):
            for b in range(len(self.eqns[a])):
                # the floowing condition can be deleted for connecting self to self for self dependent cases
                if self.my_canvas.coords(self.nodeCircles[a+1])[0]+30 != self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]])[0]+30 or self.my_canvas.coords(self.nodeCircles[a+1])[1]+30 != self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]])[1]+30:
                    startingX = self.my_canvas.coords(self.nodeCircles[a+1])[0]+30
                    startingY = self.my_canvas.coords(self.nodeCircles[a+1])[1]+30
                    endingX = self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]])[0]+30
                    endingY = self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]])[1]+30
                    self.nodeConnections.append(self.my_canvas.create_line(startingX, startingY, endingX, endingY, fill="red", arrow=tk.FIRST))
                
        for a in range(len(self.notEqns)):
            for b in range(len(self.notEqns[a])):
                # the floowing condition can be deleted for connecting self to self for self dependent cases
                if self.my_canvas.coords(self.nodeCircles[a+1])[0]+30 != self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]])[0]+30 or self.my_canvas.coords(self.nodeCircles[a+1])[1]+30 != self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]])[1]+30:
                    startingX = self.my_canvas.coords(self.nodeCircles[a+1])[0]+30
                    startingY = self.my_canvas.coords(self.nodeCircles[a+1])[1]+30
                    endingX = self.my_canvas.coords(self.nodeCircles[self.notEqns[a][b]])[0]+30
                    endingY = self.my_canvas.coords(self.nodeCircles[self.notEqns[a][b]])[1]+30
                    self.nodeNotConnections.append(self.my_canvas.create_line(startingX, startingY, endingX, endingY, fill="black", arrow=tk.FIRST))
        '''
              
        for a in range(len(self.nodeNames)):
            xpos = (a%15)*80 + 60
            ypos = int(a/15)*80 + 60
            ytextpos = int(a/15)*80 + 60 -30
            
            self.nodeCircles.append(self.my_canvas.create_oval(xpos-30, ypos-30, xpos+30, ypos+30, fill=eachNodeColor[a]))
            self.nodeTexts.append(self.my_canvas.create_text(xpos,ypos,text=self.nodeNames[a]))
          
        for a in range(len(self.eqns)):
            for b in range(len(self.eqns[a])):
                # the floowing condition can be deleted for connecting self to self for self dependent cases
                # if self.my_canvas.coords(self.nodeCircles[a])[0]+30 != self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]-1])[0]+30 or self.my_canvas.coords(self.nodeCircles[a])[1]+30 != self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]-1])[1]+30:
                startingX = self.my_canvas.coords(self.nodeCircles[a])[0]+30
                startingY = self.my_canvas.coords(self.nodeCircles[a])[1]+30 + 20
                endingX = self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]-1])[0]+30
                endingY = self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]-1])[1]+30 - 20
                self.nodeConnections.append(self.my_canvas.create_line(startingX, startingY, endingX, endingY, fill="green", arrow=tk.FIRST))
             
        for a in range(len(self.notEqns)):
            for b in range(len(self.notEqns[a])):
                # the floowing condition can be deleted for connecting self to self for self dependent cases
                # if self.my_canvas.coords(self.nodeCircles[a])[0]+30 != self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]-1])[0]+30 or self.my_canvas.coords(self.nodeCircles[a])[1]+30 != self.my_canvas.coords(self.nodeCircles[self.eqns[a][b]-1])[1]+30:
                startingX = self.my_canvas.coords(self.nodeCircles[a])[0]+30
                startingY = self.my_canvas.coords(self.nodeCircles[a])[1]+30 + 20
                endingX = self.my_canvas.coords(self.nodeCircles[self.notEqns[a][b]-1])[0]+30
                endingY = self.my_canvas.coords(self.nodeCircles[self.notEqns[a][b]-1])[1]+30 - 20
                self.nodeNotConnections.append(self.my_canvas.create_line(startingX, startingY, endingX, endingY, fill="red", arrow=tk.FIRST))
         
        
        def move(e):
            #print(e.x)
            #print(e.y)
            #e.x
            #e.y
            # if e.x-10 >= self.my_canvas.coords(self.my_circle)[0] and e.y-10 >= self.my_canvas.coords(self.my_circle)[1] and e.x+10 <= self.my_canvas.coords(self.my_circle)[2] and e.y+10 <= self.my_canvas.coords(self.my_circle)[3]:
                # self.my_canvas.delete(self.my_circle)
                # self.my_canvas.delete(self.my_text)
                # self.my_canvas.delete(self.my_line)
                # self.my_line = self.my_canvas.create_line(x,y, e.x, e.y, fill="red")
                # self.my_circle = self.my_canvas.create_oval(e.x-30, e.y-30, e.x+30, e.y+30, fill="yellow")
                # self.my_text = self.my_canvas.create_text(e.x,e.y,text="mytext")
                
            if self.movingNode == 0:
                for a in range(len(self.nodeCircles)):
                    if e.x-10 >= self.my_canvas.coords(self.nodeCircles[a])[0] and e.y-10 >= self.my_canvas.coords(self.nodeCircles[a])[1] and e.x+10 <= self.my_canvas.coords(self.nodeCircles[a])[2] and e.y+10 <= self.my_canvas.coords(self.nodeCircles[a])[3]:
                        self.movingNode = self.nodeCircles[a]
                        
            if len(self.movingConnections) == 0 and len(self.movingNotConnections) == 0:
                for b in range(len(self.nodeConnections)):
                    if self.movingNode != 0 and self.my_canvas.coords(self.nodeConnections[b])[0] == self.my_canvas.coords(self.movingNode)[0]+ 30 and self.my_canvas.coords(self.nodeConnections[b])[1] == self.my_canvas.coords(self.movingNode)[1]+ 30 + 20:
                        self.movingConnections.append(self.nodeConnections[b])
                    elif self.movingNode != 0 and self.my_canvas.coords(self.nodeConnections[b])[2] == self.my_canvas.coords(self.movingNode)[0]+ 30 and self.my_canvas.coords(self.nodeConnections[b])[3] == self.my_canvas.coords(self.movingNode)[1]+ 30 - 20:
                        self.movingConnections.append(self.nodeConnections[b])
                        
                for b in range(len(self.nodeNotConnections)):
                    if self.movingNode != 0 and self.my_canvas.coords(self.nodeNotConnections[b])[0] == self.my_canvas.coords(self.movingNode)[0]+ 30 and self.my_canvas.coords(self.nodeNotConnections[b])[1] == self.my_canvas.coords(self.movingNode)[1]+ 30 + 20:
                        self.movingNotConnections.append(self.nodeNotConnections[b])
                    elif self.movingNode != 0 and self.my_canvas.coords(self.nodeNotConnections[b])[2] == self.my_canvas.coords(self.movingNode)[0]+ 30 and self.my_canvas.coords(self.nodeNotConnections[b])[3] == self.my_canvas.coords(self.movingNode)[1]+ 30 - 20:
                        self.movingNotConnections.append(self.nodeNotConnections[b])
                    
            for a in range(len(self.nodeCircles)):
                '''
                if a == 0:
                    if e.x-10 >= self.my_canvas.coords(self.nodeCircles[a])[0] and e.y-10 >= self.my_canvas.coords(self.nodeCircles[a])[1] and e.x+10 <= self.my_canvas.coords(self.nodeCircles[a])[2] and e.y+10 <= self.my_canvas.coords(self.nodeCircles[a])[3] and self.nodeCircles[a] == self.movingNode:
                        originalCircleCenterX = self.my_canvas.coords(self.nodeCircles[a])[0]+ 30
                        originalCircleCenterY = self.my_canvas.coords(self.nodeCircles[a])[1]+ 30
                        #print(len(self.nodeCircles))
                        self.my_canvas.delete(self.nodeCircles[a])
                        self.my_canvas.delete(self.nodeTexts[a])
                        #print(len(self.nodeCircles))
                        #print("")
                        self.nodeCircles[a] = self.my_canvas.create_oval(e.x-30, e.y-30, e.x+30, e.y+30, fill="yellow")
                        self.nodeTexts[a] = self.my_canvas.create_text(e.x,e.y,text="input")
                        self.movingNode = self.nodeCircles[a]
                        #print(self.my_canvas.coords(self.nodeCircles[a]))
                        
                        lineIndexesWillBeModified = []
                        for b in range(len(self.nodeConnections)):
                            if self.my_canvas.coords(self.nodeConnections[b])[0] == originalCircleCenterX and self.my_canvas.coords(self.nodeConnections[b])[1] == originalCircleCenterY:
                                #print("moving line")
                                for c in range(len(self.movingConnections)):
                                    if self.movingConnections[c] == self.nodeConnections[b]:
                                        oldIndex2 = self.my_canvas.coords(self.nodeConnections[b])[2]
                                        oldIndex3 = self.my_canvas.coords(self.nodeConnections[b])[3]
                                        self.my_canvas.delete(self.nodeConnections[b])
                                        self.nodeConnections[b] = self.my_canvas.create_line(e.x, e.y, oldIndex2, oldIndex3, fill="red", arrow=tk.FIRST)
                                        self.movingConnections[c] = self.nodeConnections[b]
                            
                            elif self.my_canvas.coords(self.nodeConnections[b])[2] == originalCircleCenterX and self.my_canvas.coords(self.nodeConnections[b])[3] == originalCircleCenterY:
                                #print("moving line")
                                for c in range(len(self.movingConnections)):
                                    if self.movingConnections[c] == self.nodeConnections[b]:
                                        oldIndex0 = self.my_canvas.coords(self.nodeConnections[b])[0]
                                        oldIndex1 = self.my_canvas.coords(self.nodeConnections[b])[1]
                                        self.my_canvas.delete(self.nodeConnections[b])
                                        self.nodeConnections[b] = self.my_canvas.create_line(oldIndex0, oldIndex1, e.x, e.y, fill="red", arrow=tk.FIRST)
                                        self.movingConnections[c] = self.nodeConnections[b]
                                
                        for b in range(len(self.nodeNotConnections)):
                            if self.my_canvas.coords(self.nodeNotConnections[b])[0] == originalCircleCenterX and self.my_canvas.coords(self.nodeNotConnections[b])[1] == originalCircleCenterY:
                                #print("moving line")
                                for c in range(len(self.movingNotConnections)):
                                    if self.movingNotConnections[c] == self.nodeNotConnections[b]:
                                        oldIndex2 = self.my_canvas.coords(self.nodeNotConnections[b])[2]
                                        oldIndex3 = self.my_canvas.coords(self.nodeNotConnections[b])[3]
                                        self.my_canvas.delete(self.nodeNotConnections[b])
                                        self.nodeNotConnections[b] = self.my_canvas.create_line(e.x, e.y, oldIndex2, oldIndex3, fill="black", arrow=tk.FIRST)
                                        self.movingNotConnections[c] = self.nodeNotConnections[b]
                                        
                            elif self.my_canvas.coords(self.nodeNotConnections[b])[2] == originalCircleCenterX and self.my_canvas.coords(self.nodeNotConnections[b])[3] == originalCircleCenterY:
                                #print("moving line")
                                for c in range(len(self.movingNotConnections)):
                                    if self.movingNotConnections[c] == self.nodeNotConnections[b]:                               
                                        oldIndex0 = self.my_canvas.coords(self.nodeNotConnections[b])[0]
                                        oldIndex1 = self.my_canvas.coords(self.nodeNotConnections[b])[1]
                                        self.my_canvas.delete(self.nodeNotConnections[b])
                                        self.nodeNotConnections[b] = self.my_canvas.create_line(oldIndex0, oldIndex1, e.x, e.y, fill="black", arrow=tk.FIRST)
                                        self.movingNotConnections[c] = self.nodeNotConnections[b]
                '''   
                if e.x-10 >= self.my_canvas.coords(self.nodeCircles[a])[0] and e.y-10 >= self.my_canvas.coords(self.nodeCircles[a])[1] and e.x+10 <= self.my_canvas.coords(self.nodeCircles[a])[2] and e.y+10 <= self.my_canvas.coords(self.nodeCircles[a])[3] and self.nodeCircles[a] == self.movingNode:
                    originalCircleCenterX = self.my_canvas.coords(self.nodeCircles[a])[0]+ 30
                    originalCircleCenterY = self.my_canvas.coords(self.nodeCircles[a])[1]+ 30
                    #print(len(self.nodeCircles))
                    self.my_canvas.delete(self.nodeCircles[a])
                    self.my_canvas.delete(self.nodeTexts[a])
                    #print(len(self.nodeCircles))
                    #print("")
                    self.nodeCircles[a] = self.my_canvas.create_oval(e.x-30, e.y-30, e.x+30, e.y+30, fill=eachNodeColor[a])
                    self.nodeTexts[a] = self.my_canvas.create_text(e.x,e.y,text=self.nodeNames[a])
                    self.movingNode = self.nodeCircles[a]
                    #print(self.my_canvas.coords(self.nodeCircles[a]))
                    
                    lineIndexesWillBeModified = []
                    for b in range(len(self.nodeConnections)):
                        if self.my_canvas.coords(self.nodeConnections[b])[0] == originalCircleCenterX and self.my_canvas.coords(self.nodeConnections[b])[1] == originalCircleCenterY + 20:
                            #print("moving line")
                            for c in range(len(self.movingConnections)):
                                if self.movingConnections[c] == self.nodeConnections[b]:
                                    oldIndex2 = self.my_canvas.coords(self.nodeConnections[b])[2]
                                    oldIndex3 = self.my_canvas.coords(self.nodeConnections[b])[3]
                                    self.my_canvas.delete(self.nodeConnections[b])
                                    self.nodeConnections[b] = self.my_canvas.create_line(e.x, e.y + 20, oldIndex2, oldIndex3, fill="green", arrow=tk.FIRST)
                                    self.movingConnections[c] = self.nodeConnections[b]
                        if self.my_canvas.coords(self.nodeConnections[b])[2] == originalCircleCenterX and self.my_canvas.coords(self.nodeConnections[b])[3] == originalCircleCenterY - 20:
                            #print("moving line")
                            for c in range(len(self.movingConnections)):
                                if self.movingConnections[c] == self.nodeConnections[b]:
                                    oldIndex0 = self.my_canvas.coords(self.nodeConnections[b])[0]
                                    oldIndex1 = self.my_canvas.coords(self.nodeConnections[b])[1]
                                    self.my_canvas.delete(self.nodeConnections[b])
                                    self.nodeConnections[b] = self.my_canvas.create_line(oldIndex0, oldIndex1, e.x, e.y - 20, fill="green", arrow=tk.FIRST)
                                    self.movingConnections[c] = self.nodeConnections[b]
                            
                    for b in range(len(self.nodeNotConnections)):
                        if self.my_canvas.coords(self.nodeNotConnections[b])[0] == originalCircleCenterX and self.my_canvas.coords(self.nodeNotConnections[b])[1] == originalCircleCenterY + 20:
                            #print("moving line")
                            for c in range(len(self.movingNotConnections)):
                                if self.movingNotConnections[c] == self.nodeNotConnections[b]:
                                    oldIndex2 = self.my_canvas.coords(self.nodeNotConnections[b])[2]
                                    oldIndex3 = self.my_canvas.coords(self.nodeNotConnections[b])[3]
                                    self.my_canvas.delete(self.nodeNotConnections[b])
                                    self.nodeNotConnections[b] = self.my_canvas.create_line(e.x, e.y + 20, oldIndex2, oldIndex3, fill="red", arrow=tk.FIRST)
                                    self.movingNotConnections[c] = self.nodeNotConnections[b]
                        if self.my_canvas.coords(self.nodeNotConnections[b])[2] == originalCircleCenterX and self.my_canvas.coords(self.nodeNotConnections[b])[3] == originalCircleCenterY - 20:
                            #print("moving line")
                            for c in range(len(self.movingNotConnections)):
                                if self.movingNotConnections[c] == self.nodeNotConnections[b]:
                                    oldIndex0 = self.my_canvas.coords(self.nodeNotConnections[b])[0]
                                    oldIndex1 = self.my_canvas.coords(self.nodeNotConnections[b])[1]
                                    self.my_canvas.delete(self.nodeNotConnections[b])
                                    self.nodeNotConnections[b] = self.my_canvas.create_line(oldIndex0, oldIndex1, e.x, e.y - 20, fill="red", arrow=tk.FIRST)
                                    self.movingNotConnections[c] = self.nodeNotConnections[b]
                
            self.my_label.config(text="Coordinates x: " + str(e.x) + " y: " + str(e.y))
            
        def release(e):
            self.movingNode = 0
            self.movingConnections = []
            self.movingNotConnections = []
            #print("released")
            
        def blink(e):
            # print("in blick function")
            # print(e.x)
            # print(e.y)
            for a in range(len(self.nodeCircles)):
                if e.x-10 >= self.my_canvas.coords(self.nodeCircles[a])[0] and e.y-10 >= self.my_canvas.coords(self.nodeCircles[a])[1] and e.x+10 <= self.my_canvas.coords(self.nodeCircles[a])[2] and e.y+10 <= self.my_canvas.coords(self.nodeCircles[a])[3]:
                    blk(a, "orange")
                    for b in range(len(self.eqns[a])): # all the input nodes
                        blk(self.eqns[a][b] - 1, "magenta")
                    for c in range(len(self.eqns)):
                        for d in range(len(self.eqns[c])):
                            if self.eqns[c][d] - 1 == a:
                                blk(c, "cyan")
                    
                    # global eachNodeColor
                    # blk(a, eachNodeColor[a])
                    # for b in range(len(self.eqns[a])): # all the input nodes
                        # blk(self.eqns[a][b] - 1, eachNodeColor[self.eqns[a][b] - 1])
                    # for c in range(len(self.eqns)):
                        # for d in range(len(self.eqns[c])):
                            # if self.eqns[c][d] - 1 == a:
                                # blk(c, eachNodeColor[c])
                                
        def blinkBack(e):
            # print("in blick function")
            # print(e.x)
            # print(e.y)
            for a in range(len(self.nodeCircles)):
                if e.x-10 >= self.my_canvas.coords(self.nodeCircles[a])[0] and e.y-10 >= self.my_canvas.coords(self.nodeCircles[a])[1] and e.x+10 <= self.my_canvas.coords(self.nodeCircles[a])[2] and e.y+10 <= self.my_canvas.coords(self.nodeCircles[a])[3]:
                    global eachNodeColor
                    blk(a, eachNodeColor[a])
                    for b in range(len(self.eqns[a])): # all the input nodes
                        blk(self.eqns[a][b] - 1, eachNodeColor[self.eqns[a][b] - 1])
                    for c in range(len(self.eqns)):
                        for d in range(len(self.eqns[c])):
                            if self.eqns[c][d] - 1 == a:
                                blk(c, eachNodeColor[c])
        
        #root.bind("<Left>", left)
        #root.bind("<Right>", right)
        #root.bind("<Up>", up)
        #root.bind("<Down>", down)
        
        def blk(a, color):
            originalCircleCenterX = self.my_canvas.coords(self.nodeCircles[a])[0]+ 30
            originalCircleCenterY = self.my_canvas.coords(self.nodeCircles[a])[1]+ 30
            self.my_canvas.delete(self.nodeCircles[a])
            self.my_canvas.delete(self.nodeTexts[a])
            self.nodeCircles[a] = self.my_canvas.create_oval(originalCircleCenterX-30, originalCircleCenterY-30, originalCircleCenterX+30, originalCircleCenterY+30, fill=color)
            self.nodeTexts[a] = self.my_canvas.create_text(originalCircleCenterX,originalCircleCenterY,text=self.nodeNames[a])
            
            for b in range(len(self.nodeConnections)):
                if self.my_canvas.coords(self.nodeConnections[b])[0] == originalCircleCenterX and self.my_canvas.coords(self.nodeConnections[b])[1] == originalCircleCenterY + 20:
                    oldIndex0 = self.my_canvas.coords(self.nodeConnections[b])[0]
                    oldIndex1 = self.my_canvas.coords(self.nodeConnections[b])[1]
                    oldIndex2 = self.my_canvas.coords(self.nodeConnections[b])[2]
                    oldIndex3 = self.my_canvas.coords(self.nodeConnections[b])[3]
                    self.my_canvas.delete(self.nodeConnections[b])
                    self.nodeConnections[b] = self.my_canvas.create_line(oldIndex0, oldIndex1, oldIndex2, oldIndex3, fill="green", arrow=tk.FIRST)

                if self.my_canvas.coords(self.nodeConnections[b])[2] == originalCircleCenterX and self.my_canvas.coords(self.nodeConnections[b])[3] == originalCircleCenterY - 20:
                    oldIndex0 = self.my_canvas.coords(self.nodeConnections[b])[0]
                    oldIndex1 = self.my_canvas.coords(self.nodeConnections[b])[1]
                    oldIndex2 = self.my_canvas.coords(self.nodeConnections[b])[2]
                    oldIndex3 = self.my_canvas.coords(self.nodeConnections[b])[3]
                    self.my_canvas.delete(self.nodeConnections[b])
                    self.nodeConnections[b] = self.my_canvas.create_line(oldIndex0, oldIndex1, oldIndex2, oldIndex3, fill="green", arrow=tk.FIRST)

                            
            for b in range(len(self.nodeNotConnections)):
                if self.my_canvas.coords(self.nodeNotConnections[b])[0] == originalCircleCenterX and self.my_canvas.coords(self.nodeNotConnections[b])[1] == originalCircleCenterY + 20:
                    oldIndex0 = self.my_canvas.coords(self.nodeNotConnections[b])[0]
                    oldIndex1 = self.my_canvas.coords(self.nodeNotConnections[b])[1]
                    oldIndex2 = self.my_canvas.coords(self.nodeNotConnections[b])[2]
                    oldIndex3 = self.my_canvas.coords(self.nodeNotConnections[b])[3]
                    self.my_canvas.delete(self.nodeNotConnections[b])
                    self.nodeNotConnections[b] = self.my_canvas.create_line(oldIndex0, oldIndex1, oldIndex2, oldIndex3, fill="red", arrow=tk.FIRST)

                if self.my_canvas.coords(self.nodeNotConnections[b])[2] == originalCircleCenterX and self.my_canvas.coords(self.nodeNotConnections[b])[3] == originalCircleCenterY - 20:
                    oldIndex0 = self.my_canvas.coords(self.nodeNotConnections[b])[0]
                    oldIndex1 = self.my_canvas.coords(self.nodeNotConnections[b])[1]
                    oldIndex2 = self.my_canvas.coords(self.nodeNotConnections[b])[2]
                    oldIndex3 = self.my_canvas.coords(self.nodeNotConnections[b])[3]
                    self.my_canvas.delete(self.nodeNotConnections[b])
                    self.nodeNotConnections[b] = self.my_canvas.create_line(oldIndex0, oldIndex1, oldIndex2, oldIndex3, fill="red", arrow=tk.FIRST)


        self.my_label = Label(self, text="")
        self.my_label.pack(pady=20)
        
        self.my_canvas.bind('<B1-Motion>', move)
        self.my_canvas.bind('<ButtonRelease-1>',release)
        self.my_canvas.bind('<Double-Button-1>', blink)
        self.my_canvas.bind('<Button-3>', blinkBack)
        
        
        
        
    
        
'''  
# for windows        
def runSimulationCpp(cpp_file, exe_file):
    os.system("echo Compiling " + cpp_file)
    os.system('g++ ' + cpp_file + ' -o ' + exe_file)
    os.system("echo Running " + exe_file)
    os.system("echo -------------------")
    os.system(exe_file)
    os.system("python data_parse.py")
'''

'''
# for linux
def runSimulationCpp(cpp_file, exe_file):
    os.system("echo Compiling " + cpp_file)
    os.system('g++ ' + cpp_file)# + ' -o ' + exe_file)
    #os.system("echo Running " + "./a.out")#exe_file)
    os.system("./a.out")#exe_file)
    #os.system("python data_parse.py")            
    #os.system("echo -------------------")
    #os.system(exe_file)
    os.system("python data_parse.py")
'''    

# for macOS
def runSimulationCpp(cpp_file, exe_file):
    os.system("echo Compiling " + cpp_file)
    os.system('g++ ' + cpp_file)# + ' -o ' + exe_file)
    #os.system("echo Running " + "./a.out")#exe_file)
    os.system("./a.out")#exe_file)
    #os.system("python data_parse.py")            
    #os.system("echo -------------------")
    #os.system(exe_file)
    os.system("python3 data_parse.py")    
    
def runParseResultAndShowGraph():
    pass
    #os.system("echo Compiling " + cpp_file)
    #os.system("python data_parse.py")
    #os.system("python plot_node_activity.py")
    #plotterPlotSpecifiedNodes()
    
def plotterPlotSpecifiedNodes():
    ## LOADING STUFF
    # file that contains all node names
    f_all_node_name = open('Node Name and their initial state.txt', 'r')

    # load the result array
    bool_net = np.load('net_after_parsing.npy')

    # file that has names of nodes to plot
    f_plot_node_name = open('specific node.txt', 'r')


    ## PROCESSING DATA
    # make a dictionary with node names
    all_nodes = []
    for line in f_all_node_name:
        for i in range(len(line)):
            if(line[i] in [' ', '\n']):
                s = line[0:i].strip()
                if(len(s)):
                    all_nodes.append(s)
                break
        
    num2name = dict([(i,all_nodes[i]) for i in range(len(all_nodes))])
    name2num = dict([(all_nodes[i],i) for i in range(len(all_nodes))])

    # read which nodes you want to plot
    plot_nodes = []
    for line in f_plot_node_name:
        s = line.strip()
        if(len(s)):
            plot_nodes.append(s)   
            
    # some tests on all_nodes and plot_nodes
    if(len(plot_nodes)==0):
        sys.exit('No node names to plot.')
        
    for n in plot_nodes:
        if(n not in all_nodes):
            sys.exit('{} not found in the set of nodes. (Check spelling and formatting.)'.format(n))
            
    # passed the tests!

    # PLOT
    t_list = range(bool_net.shape[1])   # points on time-axis
    init_cond = bool_net.shape[0]       # number of initial conditions

    plt.figure(1)
    for n in plot_nodes:
        avg_act = 100*np.sum(bool_net[:,:,name2num[n]], axis=0)/init_cond
        plt.plot(t_list, avg_act)
        
    plt.xlabel('Time')
    plt.ylabel('Activity percentage')
    plt.xticks(range(0,1+bool_net.shape[1],4))
    plt.yticks(range(0,101,20))
    plt.legend(plot_nodes)
    plt.show()
    return plt
    
        
app = Boolean_Network_App()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=1000) #in milli-second
app.mainloop()
