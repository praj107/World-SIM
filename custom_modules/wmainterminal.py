# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 18:18:33 2023

@author: nztan
"""

import tkinter as tk
from custom_modules import wclassbasics as wcb
from custom_modules import wmaputils as wcu
import time
import numpy as np
class TerminalWidget(tk.Canvas,wcb.Basics):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, width=500, height=1000, bg='black', **kwargs)
        self.parent = parent
        self.text_lines = ['WorldSim Terminal V2 - Build 09 circa 19/12/23:','<<< ']
        self.line_distance = 15
        self.start_line_y = 10
        self.regions_analysis = None
        self.map_canvas = None
        self.sq_size = None
        self.WM = kwargs.get("WM")
        if self.WM:
            self.offsets = self.WM.gAttb("offsets")
        else:
            self.offsets = None
        self.init_terminal()
        
    def connect_map(self,m):
        self.cout(f"Connect Map called! {m} {self.WM}")
        if not self.WM or len(self.WM) < 1:
            self.WM = m
            self.offsets = self.WM.gAttb("offsets")
            self.map_canvas = self.WM.gAttb("canvas")
            self.sq_size = self.WM.gAttb("sq_size")
            self.cout(f'WorldMap connected successfully. Offsets {self.offsets} detected. ')
            self.redraw()

    def init_terminal(self):
        self.bind("<Key>", self.on_key_press)
        self.focus_set()

    def on_key_press(self, event):
        char = event.char
        if char == '\r':  # Enter key pressed
            self.run_command()
        elif char == '\x08':  # Backspace pressed
            if len(self.text_lines[-1]) > 4:  # Prevent removing the prompt
                self.text_lines[-1] = self.text_lines[-1][:-1]
                self.redraw()
        else:
            self.text_lines[-1] += char
            self.redraw()

    def run_command(self):
        # Extract the command without the prompt
        command = self.text_lines[-1][4:]
        if command:
            if command.lower() in ["cls","clear","clean"]:
                self.text_lines = ['WorldSim Terminal V2 - Build 09 circa 19/12/23:','<<< ']
                self.redraw()
                return
            elif command.lower() in ["refresh map","regen"] and self.WM:
                self.WM.canvas.delete('all')
                before = time.time()
                self.WM.generate_map()
                after = time.time()
                self.cout(f"Map Regenerated Successfully! ({round(after-before,4)} s)")
                self.redraw()
                return
            elif command.lower() in ['analyse map','analysis']:
                self.map_analysis()
                return
            elif command.lower().startswith("highlight region"):
                try:
                    region_number = int(command.lower().split()[-1])
                except Exception as e:
                    self.cout("Invalid command attribute! Error: {e}.")
                self.highlight_region(int(region_number))
            elif command.lower() in ['highlight all regions','highlight region all']:
                if self.regions_analysis:
                    for v in set(self.regions_analysis.keys()):
                        self.highlight_region(v)
            else:
                self.cout(f"Invalid command! Recieved ({command}), WM exists? {(self.WM != None)}")
                #self.text_lines.append(f"Invalid command! Recieved ({command}), WM exists? {(self.WM != None)}")
                self.redraw()
        # Process the command here (placeholder)
        self.text_lines.append('>>> ')
        self.redraw()
    
    def highlight_region(self, region):
        if not self.regions_analysis:
            self.cout("No region analysis stored! Use 'analyse' command first.")
            return
        elif not self.regions_analysis.get(region):
            self.cout(f"Invalid Region {region}! Choose a valid region from the following: {set(self.regions_analysis.keys())}.")
            return
        else:
            points = self.regions_analysis.get(region)
            print(f"POINT EXAMPLE: {points[0]}")
            #points = [(x[0]*(self.sq_size-2),x[1]*(self.sq_size-2)) for x in points]
            min_y = min(point[0] for point in points)
            min_x = min(point[1] for point in points)
            max_y = max(point[0] for point in points)
            max_x = max(point[1] for point in points)
            self.cout(f"Region coordset: x0 = {min_x}, y0 = {min_y},x1 = {max_x}, y1 = {max_y}.s")
            highlight_bbox = self.map_canvas.create_rectangle(min_x,min_y,max_x,max_y,outline='red',width=10)
            for p in points:
                y0, x0 = p
                self.map_canvas.create_rectangle(x0,y0,x0+4,y0+4, fill='red',width=0)
            # self.map_canvas.tag_configure("transparent", alpha=0.8)
            # self.map_canvas.itemconfig(highlight_bbox, tags=("transparent",))
            return
    def map_analysis(self):
        raw_arr = self.WM.gAttb("array")
        arr = wcu.downsample_array(raw_arr)
        cms = self.WM.gAttb("current_map_stats")
        self.cout(f'Current Maps Stats: {str(cms)}.')
        q1, a1, q2, a2, q3, a3 = cms[0][0],cms[0][1],cms[1][0],cms[1][1],cms[2][0],cms[2][1]
        self.cout(f'Ocean vs Land boundary: {q1} <=> {q2}.')
        
        # Feature Analysis (islands, continents, etc)
        # 1 - Find all elements that are not Deep Ocean:
        total_elements = 1e6
        no_ocean = wcu.numpy_array_filter(arr,lower=q2,upper=1e9)
        radii = 10

        self.cout(no_ocean.shape)
        self.rg = wcu.identify_land_features(no_ocean)
        summary = []
        regions_to_points = {}
        for val in set(self.rg.keys()):
            number = self.rg.get(val)
            summary.append((val,len(number)))
            regions_to_points[val] = number
        summary = sorted(summary,key=lambda x:x[1], reverse=True)
        self.regions_analysis = regions_to_points
        self.cout(summary)

        
    def redraw(self):
        self.delete("all")
        current_y = self.start_line_y
        for line in self.text_lines:
            self.create_text(10, current_y, anchor='nw', text=line, fill='green')
            current_y += self.line_distance
    def process_string_for_cout(self, s, max_length=75):
        segments = []
        while s:
            segment = s[:max_length]
            segments.append(segment)
            s = s[max_length:]  # Update 's' instead of 'input_string'
        return segments
    def cout(self, msg, ml=76):
        try:
            msg = str(msg)
        except Exception as e:
            self.cout(str(e))
            return
        if len(msg.split("\n")) > 1:
            lines = msg.split("\n")
            for line in lines:
                if lines.index(line) == 0:
                    if len(line) > ml:
                        strings = self.process_string_for_cout(line, max_length=ml)
                        for s in strings:
                            if not strings.index(s):
                                self.text_lines.append(">>> " + s)
                            else:
                                self.text_lines.append("         " + s)
                    else:
                        self.text_lines.append(">>> " + line)
                else:
                    if len(line) > ml:
                        strings = self.process_string_for_cout(line, max_length=ml)
                        for s in strings:
                            self.text_lines.append("         " + s)
                    else:
                        self.text_lines.append("         " + line)
            self.text_lines.append('<<< ')
        else:
            if len(msg) > ml:
                strings = self.process_string_for_cout(msg, max_length=ml)
                for s in strings:
                    if not strings.index(s):
                        self.text_lines.append(">>> " + s)
                    else:
                        self.text_lines.append("         " + s)
            else:
                self.text_lines.append(">>> " + msg)  
            self.text_lines.append('<<< ')
    
        self.redraw()
