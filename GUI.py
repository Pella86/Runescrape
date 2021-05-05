# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 17:01:54 2021

@author: maurop
"""

import PIL
from PIL import ImageTk as itk
import tkinter
import pathlib
import datetime

import ChampionList
import ChampionPage
import ChampionNameBox
import RunesDisplay

def strfy_day_difference(n_days):
    
    if n_days == 0:
        return "Today"
    elif n_days == 1:
        return "Yesterday"
    elif n_days <= 7:
        return f"{n_days} days ago"
    elif n_days <= 14:
        return "Last week"
    elif n_days <= 30:
        n_weeks = int(n_days / 7)
        return f"{n_weeks} weeks ago"
    elif n_days <= 60:
        return "Last month"
    elif n_days <= 360:
        n_month = int(n_days / 30)
        return f"{n_month} month ago"
    else:
        return "More than a year ago"
    

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
        while len(roles) <= len(self.roles):
            self.roles[-1].destroy()
            del self.roles[-1]
                
        # modify the roles, or add a new role if necessary
        for i, role in enumerate(roles):
            if len(self.roles) < i:
                self.modify_role(i, role)
            else:
                self.add_role(role, cb, i, i)
        

class RunesPreveiw:
    ''' Displays the 4 different rune sets '''

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
            
            RunesDisplay.round_pictures(img)
            
            
            # group 2
            img_file = rg2.keystone.get_stone().img_file
            
            img2 = PIL.Image.open(img_file)
            
            img2 = img2.convert("RGBA")
            
            RunesDisplay.round_pictures(img2)
            
            img2 = img2.resize((25, 25))
            
            # Paste the small rune in the big rune
            img.paste(img2, (25, 25), img2)

            # put the image on the label
            ref_img = itk.PhotoImage(img)
            
            label.image = ref_img
            
            label["image"] = ref_img        


class InfoDisplay:
    ''''The frame containint all the infos'''
    
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
               command=cb_preview,
               value=val)
            rb.grid(row=row, column=col)     
            
        create_game_mode_button("RIFT", 0, 0, 0)
        create_game_mode_button("ARAM", 0, 1, 1)
        
        # The roles frame
        self.roles_info = RoleInfo(self.main_frame)
        self.roles_info.main_frame.grid(row=1, column=0)
        
        # The runes set frame
        self.rune_preview = RunesPreveiw(self.main_frame, cb_preview)
        self.rune_preview.main_frame.grid(row=2, column=0) 
        
    
        
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
        
        
        self.name_list_box = ChampionNameBox.ChampionNameBox(champion_info_frame, self.champ_selection)
        self.name_list_box.update_names(self.champions_list.keys())
        
        
        button_update = tkinter.Button(champion_info_frame, text="Update", command=lambda : self.update_champion())
        button_update.pack()
        
        self.update_time_str = tkinter.StringVar()
        self.update_time_str.set("")
        
        
        label_update = tkinter.Label(champion_info_frame, textvariable=self.update_time_str)
        label_update.pack()
        
        # runes page shown
        self.runes_info_frame = tkinter.Frame(self.main_frame)
        self.runes_info_frame.grid(row=0, column=1)
        
        
        # info display
        self.info_display = InfoDisplay(self.runes_info_frame, lambda : self.roles_button())
        self.info_display.main_frame.grid(row=0, column=0)
        
        
        # frame containing the stones
        self.rune_set_frame = None


        # default champion
        champion = self.champions_list["Aatrox"]
        
        self.show_options(champion)

    
    def show_options(self, champion): 
        
        # assign the selected champion as the current champion for the 
        # runes options and indexes
        self.current_champion = champion
        
        # add the possible roles the champion has
        self.info_display.roles_info.add_roles(champion.roles, lambda : self.roles_button())
        
        # display if was chosen aram or rift
        role_idx = self.info_display.roles_info.role_var.get()
        aram_var = self.info_display.aram_var.get()
            
        cp = ChampionPage.ChampionPage(champion, champion.roles[role_idx], aram_var)  
        
        
        # get the creation time of the file
        file = pathlib.Path(cp.get_filename())
        creation_time = file.stat().st_mtime
        mtime = datetime.datetime.fromtimestamp(creation_time)
        
        now = datetime.datetime.now()
        delta = now - mtime
        days = delta.days
        
        stime = strfy_day_difference(days)
        
        #stime = mtime.strftime("%d %B %Y")
        
        self.update_time_str.set(stime)
        
        # display the rune sets
        self.info_display.rune_preview.update_images(cp)
        
        # show the runes
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
            
            self.info_display.roles_info.role_var.set(0)
            
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

        idx = self.info_display.rune_preview.rune_set_idx.get()
        
        rune_set = champion_page.get_runes_set(idx)
        
        if self.rune_set_frame is None:
            self.rune_set_frame = RunesDisplay.RuneSetFrame(self.runes_info_frame, rune_set)
            self.rune_set_frame.main_frame.grid(row = 2, column=0)
        else:
            self.rune_set_frame.update_images(rune_set)    
    
    def update_champion(self):
        champion = self.current_champion
        
        role_idx = self.info_display.roles_info.role_var.get()
        aram_var = self.info_display.aram_var.get()
        
        cp = ChampionPage.ChampionPage(champion, champion.roles[role_idx], aram_var)
        cp.download()
        
        self.show_options(champion)
        
        
        
        

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
    run_app()
    
    #test_info()
    
    
        
        
