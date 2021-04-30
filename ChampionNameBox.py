# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 14:49:43 2021

@author: maurop
"""

import tkinter


class ChampionNameBox:
    ''' Class that holds the list of champion names'''
    
    
    def __init__(self, parent_frame, lb_callback):
        # lb_callback is the function that reacts when is a name is pressed
        self.name_list_box = tkinter.Listbox(parent_frame)
        self.name_list_box.pack()
        
        self.name_list_box.bind("<<ListboxSelect>>", lambda e : lb_callback(e))   
        
        # stores the list in the box
        self.name_idx = []
        
    def update_names(self, selection_list):
        names_to_remove = []
        
        # removes the names that arent in the selection list
        for name in self.name_idx:
            if name not in selection_list:
                names_to_remove.append(name)
       
        for name in names_to_remove:
            self.remove_name(name)
        
        # adds the missing names
        for name in selection_list:
            if name not in self.name_idx:
                self.add_name(name)

    def add_name(self, name):
        # appends at the end of the list box the name
        idx = len(self.name_idx)
        self.name_list_box.insert(idx, name)
        
        self.name_idx.append(name)
    
    def remove_name(self, name):
        idx = self.name_idx.index(name)
        
        del self.name_idx[idx]
        
        self.name_list_box.delete(idx)
        
        

    