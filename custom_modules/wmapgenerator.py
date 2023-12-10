# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 15:34:47 2023

@author: nztan
"""
import noise as ns
import numpy as np
import random as rd
def gen_basic_map_layer(arr):
    print(arr.shape)
    width, height = arr.shape
    scale = 200  # Determines the "zoom" level of the noise
    octaves = 3    # Number of levels of detail
    persistence = 0.3
    lacunarity = 2.0
    offset_x = rd.uniform(0, 7000)
    offset_y = rd.uniform(0, 7000)
    for x in range(width):
        for y in range(height):
            arr[x][y] = ns.pnoise2((x + offset_x) / scale, 
                              (y + offset_y) / scale, 
                              octaves=octaves, 
                              persistence=persistence, 
                              lacunarity=lacunarity)
    return (offset_x,offset_y)