# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 18:38:46 2021

@author: maurop
"""

# =============================================================================
# TO DO list
# =============================================================================
# - button for upload
#   - show the differences?
# - scrape abilities
# - scrape win rates
# - insert message when there is a not found champion
# - log shit
# - last used champions?
# - sizes?


import os
            
import tkinter
import PIL
from PIL import ImageTk as itk
from PIL import ImageOps as ImOps

import ChampionList
import RequestsHandler

cl = ChampionList.ChampionsList()

champions_list = cl.parse_champions()


class Stone:
    
    def __init__(self, img_file, active):
        
        self.img_file = img_file
        
        self.active = active
        
        
    def __str__(self):
        
        return self.img_file + ", " + str(self.active) 

class RunesSet:
    
    def __init__(self, table_tag):
        # gets the tables containg the runes
        self.table = table_tag
    
    def get_runes(self):
        # gets the runes rows
        return self.table.find_all("tr", recursive = False)
    


class StoneRow:

    def __init__(self, rune_row):
        self.rune_row = rune_row


    def get_stones(self):
        # get the link of the image
        rune_links_tag = self.rune_row.find_all("img")
        
        stones = []
        for link_tag in rune_links_tag:
            link = link_tag.get("src")
        
            # find the image link end
            pos = link.find("?")
            
            # prepare image link
            img_link = "https:" + link[:pos]
            
            # prepare image name
            image_name_start = img_link.rfind("/") + 1
            img_name = img_link[image_name_start:]
            
            img_name_no_ext, ext = os.path.splitext(img_name)
            
            # request the image
            img_req = RequestsHandler.Request(img_link, f"./cache/{img_name_no_ext}.pickle")
            img_req.load()
            
            # prepare the filename
            img_filename = "./images/" + img_name
            
            # save the image
            img_req.save_image(img_filename)
            
            if link.find("e_grayscale&v=1") != -1:
                active = False
            else:
                active = True
                
            stone = Stone(img_filename, active)
            stones.append(stone)
            
        return stones    
        
class KeyStoneRow(StoneRow):
    
    def __init__(self, rune_row):
        super().__init__(rune_row)
        
    def get_stone(self):
        return self.get_stones()[0]
        
 
class RuneGroup:
    
    def __init__(self, keystone, in_stone_rows):
        self.keystone = KeyStoneRow(keystone)
        
        # the 3 rows
        self.stone_rows = []
        
        for row in in_stone_rows:
            self.stone_rows.append(StoneRow(row))
    


class ChampionPage:
    
    def __init__(self, champion, role):
        
        # get the chamopion page
        url = champion.link + "/" + role
        filename =  "./cache/" + champion.name + "_stats.pickle"
        req = RequestsHandler.Request(url, filename)
        req.load()

        soup = req.get_soup()
        
        # get the runes table
        class_tag = "champion-overview__table champion-overview__table--rune tabItems"
        table = soup.find("table", {"class":class_tag})    
        
        # find all tbody which contain the runes
        
        tbodies = table.find_all("tbody", recursive=False)
        #print(len(tbodies))
        
        runes_sets = tbodies[0]
        runes_set_1 = tbodies[2]
        runes_set_2 = tbodies[2]
        
        
        # from the rune set extract the runes:
        runes_specs = runes_set_1.find_all("tr", recursive=False)
        
        #print(len(runes_specs))
        
        runes_specs_1 = runes_specs[0]
        runes_specs_2 = runes_specs[1]
        
        # find the keystones
        
        keystones = runes_specs_1.find_all("div", {"class" : "perk-page__row"})
        
        
        
        #print(len(keystones))        
        
        print("--- First runes ---")
        

        self.rune_list_1 = RuneGroup(keystones[0], keystones[1:5])
        
        
        print(self.rune_list_1.keystone.get_stone())    
        for row in self.rune_list_1.stone_rows:
            print("-----")
            stones = row.get_stones()
            
            for stone in stones:
                print(stone)
                
                
        self.rune_list_2 = RuneGroup(keystones[4], keystones[5:9])
        
        
        print(self.rune_list_2.keystone.get_stone())    
        for row in self.rune_list_2.stone_rows:
            print("-----")
            stones = row.get_stones()
            
            for stone in stones:
                print(stone)
                
        
        # self.keystone = self.parse_key_rune(keystones[0])
        
        # row = keystones[1]
        
        # stones = row.find_all("div", recursive=False)
        # print(len(stones))
        
        # self.stones = []
        
        # for stone in stones:
        
        #     stone_img = Stone()
        #     stone_img.img_file = self.save_image_tag(stone)
        #     print()
            
        #     self.stones.append(stone_img)
            
        # row2 = keystones[2]
        # stones2 = row2.find_all("div", recursive=False)
        
        
        # self.stones2 = []
        
        # for stone in stones2:
        
        #     stone_img = Stone()
        #     stone_img.img_file = self.save_image_tag(stone)
        #     print()
            
        #     self.stones2.append(stone_img)       
            
            
        
        
        # for i in range(1, 5):
        #     self.parse_stone(keystones[i])
            
        # print("--- Second Runes ---")

        # self.parse_key_rune(keystones[5])
        
        # for i in range(6, 9):
        #     self.parse_stone(keystones[i])       
            
    def save_image_tag(self, stone):
        link = stone.find("img").get("src")
        pos = link.find("?")
        
        # prepare image link
        img_link = "https:" + link[:pos]
        
        # prepare image name
        image_name_start = img_link.rfind("/") + 1
        img_name = img_link[image_name_start:]
        
        img_name_no_ext, ext = os.path.splitext(img_name)
        
        img_req = RequestsHandler.Request(img_link, f"./cache/{img_name_no_ext}.pickle")
        img_req.load()
        
        img_filename = "./images/" + img_name
        
        img_req.save_image(img_filename)  
        
        return img_filename
    
    def parse_key_rune(self, keystone):
        key_rune_link = keystone.find("img").get("src")
        
        pos = key_rune_link.find("?")
        
        # prepare image link
        img_link = "https:" + key_rune_link[:pos]
        
        # prepare image name
        image_name_start = img_link.rfind("/") + 1
        img_name = img_link[image_name_start:]
        
        img_name_no_ext, ext = os.path.splitext(img_name)
        
        img_req = RequestsHandler.Request(img_link, f"./cache/{img_name_no_ext}.pickle")
        img_req.load()
        
        img_req.save_image("./images/" + img_name)
               
        # get the code
        ext_pos = key_rune_link.find(".png")
        
        code = ""
        pos = ext_pos - 1
        while key_rune_link[pos] != "/" or pos == 0:
            code = key_rune_link[pos] + code
            pos -= 1
            
        #print(code)
            
        stone = Stone()
        
        stone.img_file = "./images/" + img_name
        
        return stone
        
    
    def parse_stone(self, keystone):
        # if is the key stone the tag is this
        active_stone_tag = "perk-page__item perk-page__item--keystone perk-page__item--active"
        stone_page = keystone.find("div", {"class": active_stone_tag })      
        
        # else is this one
        if stone_page is None:
            active_stone_tag = "perk-page__item perk-page__item--active"
            stone_page = keystone.find("div", {"class": active_stone_tag }) 
            
        if stone_page:
        
            img_tag = stone_page.find("img")
            image_link = img_tag.get("src")
            image_name = img_tag.get("alt")
            
            print(image_name)
        else:
            print("No runes in this row")
        
        # for i in range(1, 5):
        #     active_stone_tag = "perk-page__item perk-page__item--keystone perk-page__item--active"
            
        #     stone_page = keystones[i].find("div",{ "class" : active_stone_tag })
            
        #     img_tag = stone_page.find("img")
        #     image_link = img_tag.find("src")
        #     image_name = img_tag.find("alt")
            
        #     print(image_name)
        
        
        

        
        # keystone = table.find_all("div", {"class": "perk-page__item perk-page__item--active"})
        # for key in keystone:
        
        #     img = key.find("img")
            
        #     print(img.get("alt"))    
            



#cp = ChampionPage(champions_list[0], champions_list[0].roles[0])


for champion in champions_list:
    if champion.name == "Maokai":
        cp = ChampionPage(champion, champion.roles[0]) 



# =============================================================================
# GUI
# =============================================================================

import matplotlib.pyplot as plt

root = tkinter.Tk()


main_frame = tkinter.Frame(root)
main_frame.pack()


keyrune_frame = tkinter.Frame(main_frame)
keyrune_frame.grid(row=0,column=0)

keyrunestone_frame = tkinter.Frame(keyrune_frame)
keyrunestone_frame.grid(row=0, column=0)


keyrune_image = tkinter.PhotoImage(file=cp.rune_list_1.keystone.get_stone().img_file)


keyrune_label = tkinter.Label(keyrunestone_frame, image=keyrune_image)
keyrune_label.pack()





for j, row in enumerate(cp.rune_list_1.stone_rows):
    stonerow_frame = tkinter.Frame(keyrune_frame)
    stonerow_frame.grid(row=j + 1, column=0)
    
    for i, stone in enumerate(row.get_stones()):
        print(i)
        print(stone.img_file)
    
        stone_frame = tkinter.Frame(stonerow_frame)
        stone_frame.grid(row=0, column=i)
        
        img = PIL.Image.open(stone.img_file)
        
        img = img.resize((50,50), PIL.Image.ANTIALIAS)
        
        print(stone.active)
        if not stone.active:
            #img = ImOps.grayscale(img)
            img = img.convert("LA")
            
            
    
        stone_image = itk.PhotoImage(img)
    
    
        stone_label = tkinter.Label(stone_frame, image=stone_image)
        stone_label.image = stone_image
        stone_label.pack()
        
        root.update()


root.mainloop()


# =============================================================================
# #previosu
# =============================================================================

# print()
# print(champions_list[0].name)
# print(champions_list[0].roles[0])

# cp = ChampionPage(champions_list[0], champions_list[0].roles[0])


# for champion in champions_list:
    
#     if champion.name == "Maokai":
#         print()
#         print(champion.name)
#         print(champion.roles[1])
#         cp = ChampionPage(champion, champion.roles[1]) 


# import RequestsHandler


# base_url = "https://euw.op.gg"

# req = RequestsHandler.Request("https://euw.op.gg/champion/statistics", "./cache/main_statistc_page.pickle")

# req.load()

# soup = req.get_soup()


# champ_selector = "body > div.l-wrap.l-wrap--champion > div.l-container > div.l-champion-index > div.l-champion-index-content > div.l-champion-index-content--main > div.champion-index__champion-list"


# champs = soup.select(champ_selector)

# print(len(champs))


# div = champs[0].find_all("div", recursive=False)


# champ_idx = 0
# print(div[champ_idx].prettify())

# name = div[champ_idx].find("div", {"class":"champion-index__champion-item__name"})


# print(name.getText())

# link = div[champ_idx].find("a")

# print(link.get("href"))

# roles = div[champ_idx].find_all("span")

# print(roles[0].getText())

# for stat in div:
#     name = stat.find("div", {"class":"champion-index__champion-item__name"}).getText()
    
#     link = stat.find("a")
        
#     print(name)
#     if link == None:
#         print("No stats")
#     else:
#         print(link.get("href"))
#     print()


# lets take a rune page


# req = RequestsHandler.Request(base_url + link.get("href") + "/" + roles[0].getText(), "./cache/" + name.getText() + "_stats.pickle")


# req.load()
# print(req.url)
# print(req.response.status_code)

# soup = req.get_soup()

# class_tag = "champion-overview__table champion-overview__table--rune tabItems"
# table = soup.find("table", {"class":class_tag})    

# print(table.getText())


# keystone = table.find_all("div", {"class": "perk-page__item perk-page__item--active"})

# print(len(keystone))

# print()
# print("----------------------------")

# print(name.getText())
# print(roles[0].getText())

# print("-----runes-----")

# for key in keystone:

#     img = key.find("img")
    
#     print(img.get("alt"))

