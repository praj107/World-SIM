# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 18:18:33 2023

@author: nztan
"""

import tkinter as tk
from custom_modules import wclassbasics as wcb
import time
class TerminalWidget(tk.Canvas,wcb.Basics):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, width=500, height=1000, bg='black', **kwargs)
        self.parent = parent
        self.text_lines = ['WorldSim Terminal V1 - Build 01 circa 9/12/23:','<<< ']
        self.line_distance = 15
        self.start_line_y = 10
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
                self.text_lines = ['<<< ']
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
                arr = self.WM.gAttb("array")
                cms = self.WM.gAttb("current_map_stats")
                self.cout(f'Current Maps Stats: {str(cms)}.')
                q1, a1, q2, a2, q3, a3 = cms[0][0],cms[0][1],cms[1][0],cms[1][1],cms[2][0],cms[2][1]
                self.cout(f'Ocean vs Land boundary: {q1} <=> {q2}.')
                return
            else:
                self.cout(f"Invalid command! Recieved ({command}), WM exists? {(self.WM != None)}")
                #self.text_lines.append(f"Invalid command! Recieved ({command}), WM exists? {(self.WM != None)}")
                self.redraw()
        # Process the command here (placeholder)
        self.text_lines.append('>>> ')
        self.redraw()

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
