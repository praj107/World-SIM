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


def bas_map_heatmap_det(WM, v, args):
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

def bas_map_vis(WM):
    
    ca = wmu.downsample_array(WM.array).flatten()
    tt = WM.settings["TileTypes"]
    a1, a2, a3 = tt["Oceans"]["allocation"],(tt["Oceans"]["allocation"]+tt["Coasts"]["allocation"]),(tt["Oceans"]["allocation"]+tt["Coasts"]["allocation"]+tt["Plains"]["allocation"])
    q1, q2, q3 = np.percentile(ca,a1), np.percentile(ca, a2), np.percentile(ca, a3)
    for x in range(WM.sq_size,WM.width,WM.sq_size):
        for y in range(WM.sq_size,WM.height,WM.sq_size):
            WM.canvas.create_rectangle(x, y, x + WM.sq_size, y + WM.sq_size, fill=bas_map_heatmap_det(WM,WM.array[x][y],(q1,q2,q3))["colour"],outline="")
    return ((q1,a1),(q2,a2),(q3,a3))