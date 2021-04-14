# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 17:01:54 2021

@author: maurop
"""

import PIL
from PIL import ImageTk as itk
import tkinter

import pathlib

import ChampionList
import ChampionPage


class StoneFrame:
    '''Frame that olds a single stone of a rune group'''
    
    def __init__(self, parent_frame, stone, is_fragment = False):
        
        self.main_frame = tkinter.Frame(parent_frame)
        
        # if is the fragment make them smaller
        if is_fragment:
            img_size = 25
        else:
            img_size = 50
            
        # composes the filename if the image is active or not
        img_file_mod = stone.img_file.replace(".png", "")
        if stone.active:
            img_file_mod = img_file_mod + "_modified_active.png"
        else:
            img_file_mod = img_file_mod + "_modified_inactive.png"
            
        
        if pathlib.Path(img_file_mod):
            img = PIL.Image.open(img_file_mod)
        else:
            
            # resize the image
            img = img.resize((img_size,img_size), PIL.Image.ANTIALIAS) 
            
            if not stone.active:
                # Converts to gray the image
                img = img.convert("LA")
                
                # Converts the black and white image to RGBA again to modify the
                # alpha channel
                img = img.convert("RGBA")
                
                # make the outer ring transparent
                pixdata = img.load()
    
                width, height = img.size
                for x in range(width):
                    for y in range(height):
                        radius = img_size / 2
                        if (x - radius)**2 + (y - radius)**2 > radius**2:
                            pixdata[x, y] = (255, 255, 255, 0)
            
            img.save(img_file_mod)
            
        
        
        # prepare the images for the active and inactive stone
        if stone.active:
            img_file_mod = stone.img_file.replace(".png", "")
            img_file_mod = img_file_mod + "_modified_active.png" 
            
            # check if the image was already 
            if not pathlib.Path(img_file_mod).is_file():
                
                img = PIL.Image.open(stone.img_file)
        
                # make the image 50x50 size
                img = img.resize((img_size,img_size), PIL.Image.ANTIALIAS) 
                
                img.save(img_file_mod)

            else:
                 img =  PIL.Image.open(img_file_mod)      
            
        else:
            img_file_mod = stone.img_file.replace(".png", "")
            img_file_mod = img_file_mod + "_modified_inactive.png"             
            
            if not pathlib.Path(img_file_mod).is_file():
                
                img = PIL.Image.open(stone.img_file)
        
                # make the image 50x50 size
                img = img.resize((img_size,img_size), PIL.Image.ANTIALIAS) 
                
                # Converts to gray the image
                img = img.convert("LA")
                
                # Converts the black and white image to RGBA again to modify the
                # alpha channel
                img = img.convert("RGBA")
                
                # make the outer ring transparent
                pixdata = img.load()
    
                width, height = img.size
                for x in range(width):
                    for y in range(height):
                        radius = img_size / 2
                        if (x - radius)**2 + (y - radius)**2 > radius**2:
                            pixdata[x, y] = (255, 255, 255, 0)
                            
                            
                img.save(img_file_mod)
            
            else:
                 img =  PIL.Image.open(img_file_mod)             
        

        stone_image = itk.PhotoImage(img)  
        
        label = tkinter.Label(self.main_frame, image=stone_image)
        label.image = stone_image
        label.pack()
        

class RuneGroupFrame:
    
    
    def __init__(self, parent_frame, rune_group, is_fragment = False):
        
        if is_fragment:
            height, width = 150, 125
        else:
            height, width = 300, 250
            
        self.main_frame = tkinter.Frame(parent_frame, height=height, width=width)
        self.main_frame.grid_propagate(0)
    
        if rune_group.keystone.rune_row:
        
            keystone = rune_group.keystone.get_stone()
            key_rune_frame = StoneFrame(self.main_frame, keystone)
            key_rune_frame.main_frame.grid(row = 0, column = 0)
            
        
        
        for j, row in enumerate(rune_group.stone_rows):
            stonerow_frame = tkinter.Frame(self.main_frame)
            stonerow_frame.grid(row=j + 1, column=0)
            
            for i, stone in enumerate(row.get_stones()):
            
                stone_frame = StoneFrame(stonerow_frame, stone, is_fragment)
                stone_frame.main_frame.grid(row=0, column=i)
        
        
        


class App:
    
    
    def __init__(self, root, champions_list):
        
        self.champions_list = champions_list
        
        self.main_frame = tkinter.Frame(root)
        self.main_frame.pack()
        
        
        # champion info, add a search box, connected to a list box that gets 
        # filtered as soon as people type
        # and the first selected will be shown
        
        champion_info_frame = tkinter.Frame(self.main_frame)
        champion_info_frame.grid(row=0, column=0)
        
        # Entry
        
        self.input_trace = tkinter.StringVar()
        self.input_trace.trace_add("write", lambda var_name, idk, mode : self.update_runes_trace(var_name, idk, mode))

        self.name_entry = tkinter.Entry(champion_info_frame, textvariable=self.input_trace)
        self.name_entry.pack()
        
        button = tkinter.Button(champion_info_frame, text="Search", command=lambda : self.update_runes())
        button.pack()
        
        # this will be a search box
        # name_label = tkinter.Label(champion_info_frame, text=champion_page.champion.name)
        # name_label.pack()
        
        # role_label = tkinter.Label(champion_info_frame, text=champion_page.role)
        # role_label.pack()
        
        self.name_list_box = tkinter.Listbox(champion_info_frame)
        self.name_list_box.pack()
        
        self.name_list_box.bind("<<ListboxSelect>>", lambda e : self.champ_selection(e))
        
        for i, name in enumerate(self.champions_list):
            self.name_list_box.insert(i, name)
            
        self.name_list_box.selection_set(0)

            
        
        # runes page shown
        self.runes_info_frame = tkinter.Frame(self.main_frame)
        self.runes_info_frame.grid(row=0, column=1)
        
        # aram or rift
        game_mode_frame = tkinter.Frame(self.runes_info_frame)
        game_mode_frame.grid(row=0, column=0)

        self.aram_var = tkinter.IntVar()
        
        rb = tkinter.Radiobutton(game_mode_frame, 
           text="RIFT", 
           variable=self.aram_var, 
           command=lambda : self.roles_button(),
           value=0)
        rb.grid(row=0, column=0)

        rb = tkinter.Radiobutton(game_mode_frame, 
           text="ARAM", 
           variable=self.aram_var, 
           command=lambda : self.roles_button(),
           value=1)
        rb.grid(row=0, column=1)
        
        
        # lane information
        self.position_frame = tkinter.Frame(self.runes_info_frame)
        self.position_frame.grid(row=1, column=0)
        
        self.role_idx = tkinter.IntVar()
        
        
        # frame containing the stones
        self.rune_set_frame = tkinter.Frame(self.runes_info_frame)
        self.rune_set_frame.grid(row = 2, column=0)

        # default champion
        champion = self.champions_list["Aatrox"]
        
        self.show_options(champion)
        
        self.current_champion = champion
        
        
        # cp = ChampionPage.ChampionPage(champion, champion.roles[0])        
        
        # self.show_runes(cp)
        
    
    def show_options(self, champion): 
        
        self.position_frame.destroy()

        self.position_frame = tkinter.Frame(self.runes_info_frame)
        self.position_frame.grid(row=1, column=0)
        
        

        # roles        
        for i, role in enumerate(champion.roles):
            rb = tkinter.Radiobutton(self.position_frame, 
               text=role, 
               variable=self.role_idx, 
               command=lambda : self.roles_button(),
               value=i)
            rb.grid(row=0, column=i)
            
            
        print("role selected:", champion.roles[self.role_idx.get()])
        
        cp = ChampionPage.ChampionPage(champion, champion.roles[self.role_idx.get()], self.aram_var.get())  
        
        
        self.show_runes(cp)
      
        
    
    def roles_button(self):
        
        self.show_options(self.current_champion)
        
        
        
        
    def champ_selection(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            name = event.widget.get(index)
            
            
            self.show_runes_name(name)
            
            
        
    def show_runes_name(self, name):
        
        if name in self.champions_list:
            champion = self.champions_list[name]
            
            self.current_champion  = champion
            
            self.role_idx.set(0)
            
            self.show_options(champion)
            
            # cp = ChampionPage.ChampionPage(champion, champion.roles[0])
            
            # self.show_runes(cp)        
    
    def update_runes_trace(self, var_name, idk, mode):
        user_input = self.input_trace.get()
        selection_list = self.match_champion(user_input)
        
        # empty the list
        self.name_list_box.delete(0, tkinter.END)
        
        for i, name in enumerate(selection_list):
            self.name_list_box.insert(i, name)
            
        if selection_list:
            self.name_list_box.selection_set(0)
            self.show_runes_name(selection_list[0])    
    
    def match_champion(self, user_input):
        selection_list =[]
        
        for champion_name in self.champions_list:
            if user_input.lower() in champion_name.lower():
                selection_list.append(champion_name)  
        
        return selection_list

        
    def update_runes(self):
        user_input = self.name_entry.get()
        
        selection_list = self.match_champion(user_input)
        
        # empty the list
        self.name_list_box.delete(0, tkinter.END)
        
        for i, name in enumerate(selection_list):
            self.name_list_box.insert(i, name)
            
        if selection_list:
            self.name_list_box.selection_set(0)
            self.show_runes_name(selection_list[0])

        
    def show_runes(self, champion_page):
        self.rune_set_frame.destroy()
        
        self.rune_set_frame = tkinter.Frame(self.runes_info_frame)
        self.rune_set_frame.grid(row = 2, column=0)
        
        
        rune_set = champion_page.get_runes_set(0)
        print("rune set available:", len(champion_page.runes_sets))

        rg1, rg2, rg3 = rune_set.get_groups()
        
        rg_frame = RuneGroupFrame(self.rune_set_frame, rg1)
        rg_frame.main_frame.grid(row=0, column=0)

        rg_frame = RuneGroupFrame(self.rune_set_frame, rg2)
        rg_frame.main_frame.grid(row=0, column=1)       
        
        rg_frame = RuneGroupFrame(self.rune_set_frame, rg3, is_fragment=True)
        rg_frame.main_frame.grid(row=0, column=2)              
        
        
        
        
        
root = tkinter.Tk()

cl = ChampionList.ChampionsList()

champions_list = cl.parse_champions()

# champion = champions_list["Sivir"]

# cp = ChampionPage.ChampionPage(champion, champion.roles[0])

# for champion in champions_list:
    
#     if champion.name == "Sivir":
#         cp = ChampionPage.ChampionPage(champion, champion.roles[0])
        
#cp = ChampionPage.ChampionPage(champions_list[0], champions_list[0].roles[0])




App(root, champions_list)

root.mainloop()
        
        
        


# main_frame = tkinter.Frame(root)
# main_frame.pack()


# keyrune_frame = tkinter.Frame(main_frame)
# keyrune_frame.grid(row=0,column=0)

# keyrunestone_frame = tkinter.Frame(keyrune_frame)
# keyrunestone_frame.grid(row=0, column=0)


# keyrune_image = tkinter.PhotoImage(file=cp.rune_list_1.keystone.get_stone().img_file)


# keyrune_label = tkinter.Label(keyrunestone_frame, image=keyrune_image)
# keyrune_label.pack()





# for j, row in enumerate(cp.rune_list_1.stone_rows):
#     stonerow_frame = tkinter.Frame(keyrune_frame)
#     stonerow_frame.grid(row=j + 1, column=0)
    
#     for i, stone in enumerate(row.get_stones()):
#         print(i)
#         print(stone.img_file)
    
#         stone_frame = tkinter.Frame(stonerow_frame)
#         stone_frame.grid(row=0, column=i)
        
#         img = PIL.Image.open(stone.img_file)
        
#         img = img.resize((50,50), PIL.Image.ANTIALIAS)
        
#         print(stone.active)
#         if not stone.active:
#             #img = ImOps.grayscale(img)
#             img = img.convert("LA")
            
            
    
#         stone_image = itk.PhotoImage(img)
    
    
#         stone_label = tkinter.Label(stone_frame, image=stone_image)
#         stone_label.image = stone_image
#         stone_label.pack()
        
#         root.update()


# root.mainloop()
