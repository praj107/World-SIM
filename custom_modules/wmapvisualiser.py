# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 17:21:26 2023

@author: nztan
"""

import numpy as np
import time
import json
import noise
from custom_modules import wmaputils as wmu
from custom_modules import wclassbasics as wcb
class MapVisualiser(wcb.Basics):
    def __init__(self, WM):
        self.WM = WM
        self.sq_size = self.WM.gAttb("sq_size")
        self.height = self.WM.gAttb("height")
        self.width = self.WM.gAttb("width")
        self.WMsettings = self.WM.gAttb("settings")
        self.WMarray = self.WM.gAttb("array")
        self.WMcanvas = self.WM.gAttb("canvas")
    def bas_map_heatmap_det(self, WM, v, args):
        #ca = WM.array.flatten()
        q1, q2, q3 = args
        tt = WM.settings["TileTypes"]
        if v < q1:
            return tt["Oceans"]
        elif v >= q1 and v < q2:
            return tt["Coasts"]
        elif v >= q2 and v < q3:
            return tt["Plains"]
        elif v >= q3:
            return tt["Mountains"]
        else:
            return "#FFFFFF"
    
    def bas_map_vis(self):
        
        ca = wmu.downsample_array(self.WMarray, factor = 16).flatten()
        tt = self.WMsettings["TileTypes"]
        a1, a2, a3 = tt["Oceans"]["allocation"],(tt["Oceans"]["allocation"]+tt["Coasts"]["allocation"]),(tt["Oceans"]["allocation"]+tt["Coasts"]["allocation"]+tt["Plains"]["allocation"])
        q1, q2, q3 = np.percentile(ca,a1), np.percentile(ca, a2), np.percentile(ca, a3)
        for x in range(self.sq_size,self.width,self.sq_size):
            for y in range(self.sq_size,self.height,self.sq_size):
                self.WMcanvas.create_rectangle(x, y, x + self.sq_size, y + self.sq_size, fill=self.bas_map_heatmap_det(self.WM,self.WMarray[x][y],(q1,q2,q3))["colour"],outline="")
        return ((q1,a1),(q2,a2),(q3,a3))