# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 18:40:11 2023

@author: nztan
"""

class Basics:
    def __init__(self):
        self.bs_present = True
        
    def gAttb(self, attr_name, default=None):
        return getattr(self, attr_name, default)