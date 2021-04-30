# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 14:53:20 2021

@author: maurop
"""
import PIL
from PIL import ImageTk as itk

import tkinter
import pathlib


def round_pictures(img):
    # make the outer ring transparent
    pixdata = img.load()
    
    # every pixel outside the radius are now transparent
    width, height = img.size
    for x in range(width):
        for y in range(height):
            radius = width / 2
            if (x - radius)**2 + (y - radius)**2 > radius**2:
                pixdata[x, y] = (255, 255, 255, 0)


class StoneFrame:
    '''Frame that holds a single stone of a rune group'''
    
    def __init__(self, parent_frame, stone, is_fragment = False):
        
        self.main_frame = tkinter.Frame(parent_frame)
        
        # if is the fragment make them smaller
        if is_fragment:
            self.img_size = 25
        else:
            self.img_size = 50
        
        # loads the image in a tk friendly format
        stone_image = self.prepare_photo_image(stone)
        
        # creates the label holding the image
        self.label = tkinter.Label(self.main_frame, image=stone_image)
        self.label.image = stone_image
        self.label.pack()
        
        
    def prepare_photo_image(self, stone):
        ''' Prepares the pictures in a tk friendly format'''
        
         # composes the filename if the image is active or not
        img_file_mod = stone.img_file.replace(".png", "")
        if stone.active:
            img_file_mod = img_file_mod + "_modified_active.png"
        else:
            img_file_mod = img_file_mod + "_modified_inactive.png"
            
        # if the picture was already modified it loads it from the ./image 
        # folder
        if pathlib.Path(img_file_mod).is_file():
            img = PIL.Image.open(img_file_mod)
        else:
            
            img = PIL.Image.open(stone.img_file)
            
            # resize the image
            img = img.resize((self.img_size,self.img_size), PIL.Image.ANTIALIAS) 
            
            # if the stone is inactive it makes it gray
            if not stone.active:
                # Converts to gray the image
                img = img.convert("LA")
                
                # Converts the black and white image to RGBA again to modify 
                # the alpha channel
                img = img.convert("RGBA")
                
                round_pictures(img)
  
            
            # save the image for later
            img.save(img_file_mod)
            
        return itk.PhotoImage(img)  
    
    def update_image(self, stone):
        img = self.prepare_photo_image(stone)       
        
        self.label["image"] = img
        self.label.image = img


class RuneGroupFrame:
    ''' This class holds a rune group'''
    
    
    def __init__(self, parent_frame, rune_group, is_fragment = False):
        
        self.is_framgent = is_fragment
        
        # make it bigger for the runes, and smaller for the fragments
        if self.is_framgent:
            height, width = 150, 125
        else:
            height, width = 300, 250
            
        self.main_frame = tkinter.Frame(parent_frame, height=height, width=width)
        self.main_frame.grid_propagate(0)
        
        # if a keystone exists, which for the fragment doesnt, create
        # a keystone frame
        if rune_group.keystone.rune_row:
        
            keystone = rune_group.keystone.get_stone()
            self.key_rune_frame = StoneFrame(self.main_frame, keystone)
            self.key_rune_frame.main_frame.grid(row = 0, column = 0)
            
        
        # for each row of stone create a frame containing the 3 pr more stones
        self.stones_rows = []
        self.stones_frames = []
        for j, row in enumerate(rune_group.stone_rows):
            stonerow_frame = tkinter.Frame(self.main_frame)
            stonerow_frame.grid(row=j + 1, column=0)
            
            self.stones_frames.append(stonerow_frame)
            
            stones_row = []
            
            for i, stone in enumerate(row.get_stones()):
                stone_frame = StoneFrame(stonerow_frame, stone, self.is_framgent)
                stone_frame.main_frame.grid(row=0, column=i)
                
                stones_row.append(stone_frame)
                
            self.stones_rows.append(stones_row)
    
    def update_images(self, rune_group):
        
        if rune_group.keystone.rune_row:
            keystone = rune_group.keystone.get_stone()
            self.key_rune_frame.update_image(keystone)
            
        for i, current_row, input_row in zip(range(len(self.stones_rows)), self.stones_rows, rune_group.stone_rows):
            
            input_row = input_row.get_stones()

            # remove excess stones
            while len(current_row) > len(input_row):
                current_row[-1].main_frame.destroy()
                del current_row[-1]
            
      
            # update the stones
            for current_stone, input_stone in zip(current_row, input_row):
                current_stone.update_image(input_stone)
            
            # add stones if there are more
            idx = len(current_row)
            while len(input_row) > len(current_row):
                stone = input_row[idx]
                idx += 1
                
                frame = self.stones_frames[i]
                new_stone_frame = StoneFrame(frame, stone, self.is_framgent)
                new_stone_frame.main_frame.grid(row=0, column=idx)
                current_row.append(new_stone_frame)

class RuneSetFrame:

    def __init__(self, parent_frame, rune_set):
        self.main_frame = tkinter.Frame(parent_frame)
        
        rg1, rg2, rg3 = rune_set.get_groups()
        
        self.rg1_frame = RuneGroupFrame(self.main_frame, rg1)
        self.rg1_frame.main_frame.grid(row=0, column=0)

        self.rg2_frame = RuneGroupFrame(self.main_frame, rg2)
        self.rg2_frame.main_frame.grid(row=0, column=1)       
        
        self.rg3_frame = RuneGroupFrame(self.main_frame, rg3, is_fragment=True)
        self.rg3_frame.main_frame.grid(row=1, column=0, columnspan=2) 
    
    
    def update_images(self, rune_set):
        rg1, rg2, rg3 = rune_set.get_groups()
        
        self.rg1_frame.update_images(rg1)
        self.rg2_frame.update_images(rg2)
        self.rg3_frame.update_images(rg3)    
        