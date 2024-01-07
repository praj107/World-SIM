# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 15:34:47 2023

@author: nztan
"""
import noise as ns
import numpy as np
import random as rd
import math

def generate_basic_layer(arr, scale=30, octaves=3, persistence=0.3, lacunarity=2.0, R=100, r=50):
    height, width = arr.shape
    arr_layer = np.copy(arr)  # Creating a new array for the layer
    offset_x = rd.uniform(0, 7000)
    offset_y = rd.uniform(0, 7000)
    offset_z = rd.uniform(0, 7000)  # Additional offset for the 3rd dimension

    for y in range(height):
        for x in range(width):
            # Convert (x, y) to angles theta and phi
            theta = (x / width) * 2 * math.pi
            phi = (y / height) * 2 * math.pi

            # Convert angles to coordinates on the torus
            x_torus = (R + r * math.cos(phi)) * math.cos(theta)
            y_torus = (R + r * math.cos(phi)) * math.sin(theta)
            z_torus = r * math.sin(phi)

            # Sample 3D Perlin noise at torus coordinates
            arr_layer[y][x] = ns.pnoise3((x_torus + offset_x) / scale,
                                         (y_torus + offset_y) / scale,
                                         (z_torus + offset_z) / scale,
                                         octaves=octaves,
                                         persistence=persistence,
                                         lacunarity=lacunarity)
    return arr_layer

def gen_basic_map_layer(arr, scale=1000, octaves=3, persistence=0.3, lacunarity=2.0, layers=3, R=1000, r=500):
    height, width = arr.shape
    base_layer = np.copy(arr)

    # Generating the base layer
    base_layer = generate_basic_layer(base_layer, scale, octaves, persistence, lacunarity, R, r)

    # Adding extra layers
    for l in range(1, layers):
        s_offset = rd.randint(-25, 25)
        extra_layer = generate_basic_layer(arr, scale=scale+s_offset, octaves=octaves-rd.randint(1,2), persistence=persistence, lacunarity=lacunarity, R=R, r=r)
        base_layer += extra_layer  # Element-wise multiplication

    return base_layer