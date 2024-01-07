# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 18:33:23 2023

@author: nztan
"""

# Foriegn Modules.
import tkinter as tk
import json
import random
import datetime
import time

# Custom Modules.
from tkinter import ttk
from custom_modules import wmapcanvas as wmc
from custom_modules import wmainterminal as wmt
from custom_modules import wclassbasics as wcb

# Main Class
class MySQLAccessGUI(wcb.Basics):
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("World Simulator V1")
        self.master.geometry("1500x1000")
        
        # Frames
        self.LFrame = tk.Frame(self.master, bg="white", width=500, height=1000)
        self.RFrame = tk.Frame(self.master, bg="white", width=1000, height=1000)
        self.LFrame.pack(side=tk.LEFT)
        self.LFrame.pack_propagate(0)
        self.RFrame.pack(side=tk.RIGHT)
        self.RFrame.pack_propagate(0)

        self.console = wmt.TerminalWidget(self.LFrame)
        self.console.pack(side=tk.TOP, fill=tk.BOTH)
        
        # World Sim Canvas
        self.map = wmc.WorldMap(self.RFrame)
        self.console.connect_map(self.map)
        self.master.mainloop()
        
        # Console:
        
MySQLAccessGUI()