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
            img_size = 25
        else:
            img_size = 50
            
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
            img = img.resize((img_size,img_size), PIL.Image.ANTIALIAS) 
            
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
        
        
        # loads the image in a tk friendly format
        stone_image = itk.PhotoImage(img)  
        
        # creates the label holding the image
        label = tkinter.Label(self.main_frame, image=stone_image)
        label.image = stone_image
        label.pack()
        
        
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
        
        
        

class RuneGroupFrame:
    ''' This class holds a rune group'''
    
    
    def __init__(self, parent_frame, rune_group, is_fragment = False):
        
        # make it bigger for the runes, and smaller for the fragments
        if is_fragment:
            height, width = 150, 125
        else:
            height, width = 300, 250
            
        self.main_frame = tkinter.Frame(parent_frame, height=height, width=width)
        self.main_frame.grid_propagate(0)
        
        # if a keystone exists, which for the fragment doesnt, create
        # a keystone frame
        if rune_group.keystone.rune_row:
        
            keystone = rune_group.keystone.get_stone()
            key_rune_frame = StoneFrame(self.main_frame, keystone)
            key_rune_frame.main_frame.grid(row = 0, column = 0)
            
        
        # for each row of stone create a frame containing the 3 stones
        for j, row in enumerate(rune_group.stone_rows):
            stonerow_frame = tkinter.Frame(self.main_frame)
            stonerow_frame.grid(row=j + 1, column=0)
            
            for i, stone in enumerate(row.get_stones()):
                stone_frame = StoneFrame(stonerow_frame, stone, is_fragment)
                stone_frame.main_frame.grid(row=0, column=i)

class RoleInfo:
    ''' Manages the role info button '''
    
    def __init__(self, parent_frame):
        self.main_frame = tkinter.Frame(parent_frame)
        
        # holds the role buttons so they can be modified
        self.roles = []
        
        # the selected variable
        self.role_var = tkinter.IntVar()
    
    
    def add_role(self, role, cb, value, col):
        # puts a new button in the selected column
        rb = tkinter.Radiobutton(self.main_frame, 
           text=role, 
           variable=self.role_var, 
           command=cb,
           value=value)
        rb.grid(row=0, column=col) 
        
        self.roles.append(rb)    
        
    def modify_role(self, idx, role):
        self.roles[idx]["text"] = role
        
    
    def add_roles(self, roles, cb):
        
        # remove the excess roles
        while len(roles) < len(self.roles):
            self.roles[-1].destroy()
            del self.roles[-1]
                
        # modify the roles, or add a new role if necessary
        for i, role in enumerate(roles):
            if len(self.roles) < i:
                self.modify_role(i, role)
            else:
                self.add_role(role, cb, i, i)
        

class RunesPreveiw:


    def __init__(self, parent_frame, cb):
        self.main_frame = tkinter.Frame(parent_frame)
        
        
        self.rune_set_idx = tkinter.IntVar()
        
        self.preview_list = []
        
        # create the 4 frames containint a radiobutton and an image
        for i in range(4):
            rb_frame = tkinter.Frame(self.main_frame)
            rb_frame.grid(row=0, column=i)

            rb = tkinter.Radiobutton(rb_frame, 
               text="", 
               variable=self.rune_set_idx, 
               command=cb,
               value=i)
            rb.grid(row=0, column=0) 
            
            label_img = tkinter.Label(rb_frame)
            label_img.grid(row=0, column=1)
            
            self.preview_list.append(label_img)
    
    def update_images(self, champion_page):
       
        for i, label in enumerate(self.preview_list):
            rune_set = champion_page.get_runes_set(i)
            
            rg1, rg2, _ = rune_set.get_groups()
            
            
            # group 1
            img_file = rg1.keystone.get_stone().img_file
            
            img = PIL.Image.open(img_file)
            
            img = img.resize((50, 50))
            
            img = img.convert("RGBA")
            
            round_pictures(img)
            
            
            # group 2
            img_file = rg2.keystone.get_stone().img_file
            
            img2 = PIL.Image.open(img_file)
            
            img2 = img2.convert("RGBA")
            
            round_pictures(img2)
            
            img2 = img2.resize((25, 25))
            
            # Paste the small rune in the big rune
            img.paste(img2, (25, 25), img2)

            # put the image on the label
            ref_img = itk.PhotoImage(img)
            
            label.image = ref_img
            
            label["image"] = ref_img        
                                                    
                                        
        
        

              
class InfoDisplay:
    
    def __init__(self, parent_frame, cb_preview):
        
        self.main_frame = tkinter.Frame(parent_frame)
        
        # Game mode radio buttons
        game_mode_frame = tkinter.Frame(self.main_frame)
        game_mode_frame.grid(row=0, column=0)

        self.aram_var = tkinter.IntVar()
        
        def create_game_mode_button(text, row, col, val):
            rb = tkinter.Radiobutton(game_mode_frame, 
               text=text, 
               variable=self.aram_var, 
               command=lambda : self.roles_button(),
               value=val)
            rb.grid(row=row, column=col)     
            
        create_game_mode_button("RIFT", 0, 0, 0)
        create_game_mode_button("ARAM", 0, 1, 1)
        
        # The roles frame
        self.roles_info = RoleInfo(self.main_frame)
        self.roles_info.main_frame.grid(row=1, column=0)
        
        #The runes set frame
        
        self.rune_preview = RunesPreveiw(self.main_frame, cb_preview)
    
        
        
    

class App:
    ''' Main App '''
    
    def __init__(self, root, champions_list):
        
        # the list of all champions containing links
        self.champions_list = champions_list
        
        self.main_frame = tkinter.Frame(root)
        self.main_frame.pack()
        
        
        # champion info, a search box, connected to a list box that gets 
        # filtered as soon as people type
        # and the first selected will be shown
        
        champion_info_frame = tkinter.Frame(self.main_frame)
        champion_info_frame.grid(row=0, column=0)
        
        # Entry box for user input
        
        # string var that keeps track of user input
        lb = tkinter.Label(champion_info_frame, text="Enter champion name")
        lb.pack()       
        
        self.input_trace = tkinter.StringVar()
        self.input_trace.trace_add("write", lambda var_name, idk, mode : self.update_runes_trace(var_name, idk, mode))

        self.name_entry = tkinter.Entry(champion_info_frame, textvariable=self.input_trace)
        self.name_entry.pack()
        
        # This will hold the list of champions
        lb = tkinter.Label(champion_info_frame, text="Champions List")
        lb.pack()
        
        
        self.name_list_box = ChampionNameBox(champion_info_frame, self.champ_selection)
        self.name_list_box.update_names(self.champions_list.keys())

        # runes page shown
        self.runes_info_frame = tkinter.Frame(self.main_frame)
        self.runes_info_frame.grid(row=0, column=1)
        
        
        # info display
        self.info_display = InfoDisplay(self.main_frame, lambda : self.roles_button())
        
        
        
        # # aram or rift
        # game_mode_frame = tkinter.Frame(self.runes_info_frame)
        # game_mode_frame.grid(row=0, column=0)

        # self.aram_var = tkinter.IntVar()
        
        # rb = tkinter.Radiobutton(game_mode_frame, 
        #    text="RIFT", 
        #    variable=self.aram_var, 
        #    command=lambda : self.roles_button(),
        #    value=0)
        # rb.grid(row=0, column=0)

        # rb = tkinter.Radiobutton(game_mode_frame, 
        #    text="ARAM", 
        #    variable=self.aram_var, 
        #    command=lambda : self.roles_button(),
        #    value=1)
        # rb.grid(row=0, column=1)
        
        
        # # lane information
        # self.position_frame = tkinter.Frame(self.runes_info_frame)
        # self.position_frame.grid(row=1, column=0)
        
        # self.role_idx = tkinter.IntVar()

        # self.rune_set_idx = tkinter.IntVar()
        # self.rune_set_idx.set(0) 
        
        # rune_set_index_frame = tkinter.Frame(self.runes_info_frame)
        # rune_set_index_frame.grid(row=2, column=0)
        
        
        
        # self.label_img_list = []
        
        # for i in range(4):
        #     rb_frame = tkinter.Frame(rune_set_index_frame)
        #     rb_frame.grid(row=0, column=i)

        #     rb = tkinter.Radiobutton(rb_frame, 
        #        text=str(i), 
        #        variable=self.rune_set_idx, 
        #        command=lambda : self.roles_button(),
        #        value=i)
        #     rb.grid(row=0, column=0) 
            
        #     label_img = tkinter.Label(rb_frame)
        #     label_img.grid(row=0, column=1)
            
        #     self.label_img_list.append(label_img)
            
         

        
        # # frame containing the stones
        # self.rune_set_frame = tkinter.Frame(self.runes_info_frame)
        # self.rune_set_frame.grid(row = 2, column=0)
        

        
    

        # default champion
        champion = self.champions_list["Aatrox"]
        
        self.show_options(champion)

        
    def update_list_box(self, champion_list):
        pass
        
    
    def show_options(self, champion): 
        
        # self.position_frame.destroy()

        # self.position_frame = tkinter.Frame(self.runes_info_frame)
        # self.position_frame.grid(row=1, column=0)
        
        self.current_champion = champion
        
        self.info_display.roles_info.add_roles(champion.roles, lambda : self.roles_button())
  

        # roles        
        for i, role in enumerate(champion.roles):
            rb = tkinter.Radiobutton(self.position_frame, 
               text=role, 
               variable=self.role_idx, 
               command=lambda : self.roles_button(),
               value=i)
            rb.grid(row=0, column=i)
            
        cp = ChampionPage.ChampionPage(champion, champion.roles[self.role_idx.get()], self.aram_var.get())  
        
        for i, label in enumerate(self.label_img_list):
            rune_set = cp.get_runes_set(i)
            
            rg1, rg2, _ = rune_set.get_groups()
            
            
            # group 1
            img_file = rg1.keystone.get_stone().img_file
            
            img = PIL.Image.open(img_file)
            
            img = img.resize((50, 50))
            
            img = img.convert("RGBA")
            
            round_pictures(img)
            
            
            # group 2
            img_file = rg2.keystone.get_stone().img_file
            
            img2 = PIL.Image.open(img_file)
            
            img2 = img2.convert("RGBA")
            
            round_pictures(img2)
            
            img2 = img2.resize((25, 25))
            
            # img2, img1
            img.paste(img2, (25, 25), img2)

            
            ref_img = itk.PhotoImage(img)
            
            label.image = ref_img
            
            label["image"] = ref_img
            
        
        
        self.show_runes(cp)
      
        
    
    def roles_button(self):
        # triggered by fiddling with Aram/rift or position
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
               
    
    def update_runes_trace(self, var_name, idk, mode):
        user_input = self.input_trace.get()
        selection_list = self.match_champion(user_input)
        
        self.name_list_box.update_names(selection_list)
        
        if selection_list:
            if len(user_input) >= 2:
                champion = self.champions_list[selection_list[0]]
                
                self.show_options(champion)
    
    def match_champion(self, user_input):
        # function that filters the list
        selection_list =[]
        
        for champion_name in self.champions_list:
            if user_input.lower() in champion_name.lower():
                selection_list.append(champion_name)  
        
        return selection_list

        
    def show_runes(self, champion_page):
        self.rune_set_frame.destroy()
        
        self.rune_set_frame = tkinter.Frame(self.runes_info_frame)
        self.rune_set_frame.grid(row = 3, column=0)
        
        idx = self.rune_set_idx.get()
        
        
        rune_set = champion_page.get_runes_set(idx)

        rg1, rg2, rg3 = rune_set.get_groups()
        
        rg_frame = RuneGroupFrame(self.rune_set_frame, rg1)
        rg_frame.main_frame.grid(row=0, column=0)

        rg_frame = RuneGroupFrame(self.rune_set_frame, rg2)
        rg_frame.main_frame.grid(row=0, column=1)       
        
        rg_frame = RuneGroupFrame(self.rune_set_frame, rg3, is_fragment=True)
        rg_frame.main_frame.grid(row=1, column=0, columnspan=2)              
        
        

def run_app():
    root = tkinter.Tk()
    
    cl = ChampionList.ChampionsList()
    
    champions_list = cl.parse_champions()
    
    App(root, champions_list)
    
    root.mainloop()
    

def test_callback():
    print("Test callback")
    
    
def test_info():
    root = tkinter.Tk()
    ri = RoleInfo(root)
    ri.main_frame.pack()
    
    roles = ["Top", "Middle", "Support"]
    
    ri.add_roles(roles, test_callback)

    roles = ["Bottom", "Jungle"]
    
    ri.add_roles(roles, test_callback)
    
    roles = ["Bottom", "Middle", "Support"]
    
    ri.add_roles(roles, test_callback)
    
    root.mainloop()

if __name__ == "__main__":
    # run_app()
    
    test_info()
    
    
    # root = tkinter.Tk()
    # ri = RoleInfo(root)
    # ri.main_frame.pack()
    
    # roles = ["Top", "Middle", "Support"]
    
    # ri.add_roles(roles, test_callback)

    # roles = ["Bottom", "Jungle"]
    
    # ri.add_roles(roles, test_callback)
    
    # roles = ["Bottom", "Middle", "Support"]
    
    # ri.add_roles(roles, test_callback)
    
    # root.mainloop()
        
        
