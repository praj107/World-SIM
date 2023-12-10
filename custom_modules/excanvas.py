# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 02:25:16 2023

@author: nztan
"""

# Filename: scrollable_canvas.py
import tkinter as tk

class ScrollableCanvas:
    def __init__(self, master,width=600):
        self.master = master
        self.canvas = tk.Canvas(master, width=width)
        self.canvas.pack(side = 'left', fill="both", expand=True)
        self.width = width
        # list to keep track of rectangles
        self.rectangles = []

        # Adding a scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configuring the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

    def add_rectangle(self, text, rect_color="blue", text_color="white", font=("Arial", 14), xy=[600,18]):
        if self.rectangles:
            # Get the position of the last rectangle
            _, _, _, last_y2 = self.canvas.coords(self.rectangles[-1][0])
            y1 = last_y2
        else:
            # This is the first rectangle
            y1 = 0

        x1 = 0
        y2 = y1 + xy[1]
        x2 = x1 + max(xy[0],self.width)

        rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=rect_color,outline=rect_color)
        text_id = self.canvas.create_text(0, (y1+y2)/2, text=text, fill=text_color, font=font,anchor=tk.W)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.rectangles.append((rect_id, text_id))

    def modify_rectangle(self, index, rect_color=None, text_color=None):
        if 0 <= index < len(self.rectangles):
            rect_id, text_id = self.rectangles[index]
            if rect_color:
                self.canvas.itemconfig(rect_id, fill=rect_color)
            if text_color:
                self.canvas.itemconfig(text_id, fill=text_color)

    def delete_rectangle(self, index,all_elements=False):
        if all_elements:
            self.canvas.delete("all")
            self.rectangles.clear()
            return True
        if 0 <= index < len(self.rectangles):
            rect_id, text_id = self.rectangles.pop(index)
            self.canvas.delete(rect_id)
            self.canvas.delete(text_id)
            # Update the positions of the following rectangles
            for i in range(index, len(self.rectangles)):
                rect_id, text_id = self.rectangles[i]
                x1, y1, x2, y2 = self.canvas.coords(rect_id)
                new_y1 = y1 - 110
                new_y2 = y2 - 110
                self.canvas.coords(rect_id, x1, new_y1, x2, new_y2)
                self.canvas.coords(text_id, (x1+x2)/2, (new_y1+new_y2)/2)
