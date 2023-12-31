# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 18:33:54 2023

@author: nztan
"""

import tkinter as tk
import numpy as np
import time
import json
import noise
from custom_modules import wmapgenerator as wmp
from custom_modules import wmapvisualiser as wmv
from custom_modules import wclassbasics as wcb
class WorldMap(wcb.Basics):
    def __init__(self, master,height=1000,width=1000):
        self.master = master
        with open('simulation_settings.json','r') as f:
            self.settings = json.load(f)
        self.canvas = tk.Canvas(master, width=width, height=height)
        self.canvas.pack(side = 'left', fill="both", expand=True)
        self.width = width
        self.height = height
        self.array = np.zeros((self.width,self.height))
        self.objects = []
        self.sq_size = 4
        self.current_map_stats = None
        
        
        
        self.generate_map()
        
        
    def generate_map(self):
        self.offsets = (0,0,0)
        self.array = wmp.gen_basic_map_layer(self.array)
        #print(self.array)
        self.MPV = wmv.MapVisualiser(self)
        self.current_map_stats = self.MPV.bas_map_vis()
        print(self.current_map_stats)
        

