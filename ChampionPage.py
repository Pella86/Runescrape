# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 10:58:43 2021

@author: maurop
"""

import os
import pathlib
import ChampionList
import RequestsHandler


# Class that stores the rune stone
class Stone:
    
    def __init__(self, img_file, active):
        
        self.img_file = img_file
        
        self.active = active
        
        
    def __str__(self):
        
        return self.img_file + ", " + str(self.active) 


# Class that represent a rune row
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
            
            # prepare the filename
            img_filename = "./images/" + img_name
                            
            if pathlib.Path(img_filename).is_file():
                # the file was already downloaded
                pass
            else:
                img_name_no_ext, ext = os.path.splitext(img_name)
                
                # request the image
                img_req = RequestsHandler.Request(img_link, f"./cache/{img_name_no_ext}.pickle")
                img_req.load()
                
    
                
                # save the image
                img_req.save_image(img_filename)
            
            if link.find("e_grayscale&v=1") != -1:
                active = False
            else:
                active = True
                
            stone = Stone(img_filename, active)
            stones.append(stone)
            
        return stones    

# class that represent the rune symbol of the key stone        
class KeyStoneRow(StoneRow):
    
    def __init__(self, rune_row):
        super().__init__(rune_row)
        
    def get_stone(self):
        return self.get_stones()[0]
        
# class that represent a single rune group (e.g. precision) 
class RuneGroup:
    
    def __init__(self, keystone, in_stone_rows):
        self.keystone = KeyStoneRow(keystone)
        
        # the 3 rows
        self.stone_rows = []
        
        for row in in_stone_rows:
            self.stone_rows.append(StoneRow(row))


# Class that represent the 3 runes groups (e.g. precision, domination, 3 dots)
class RunesSet:
    
    def __init__(self, rune_table):
        # gets the tables containg the runes
        self.rune_table = rune_table
        
        #self.rune_groups = self.table.find_all("tr", recursive = False)

    def get_runes(self):
        # gets the runes rows
        runes =  self.rune_table.find_all("div", {"class" : "perk-page__row"})
        runes += self.rune_table.find_all("div", {"class" : "fragment__row"})
        return runes
    
    def get_groups(self):
        stones = self.get_runes()
        
        rg1 = RuneGroup(stones[0], stones[1:5])
        rg2 = RuneGroup(stones[5], stones[6:9])
        rg3 = RuneGroup(None, stones[9:12])
        return [rg1, rg2, rg3]    


class ChampionPage:
    
    def __init__(self, champion, role, is_aram):
        
        self.champion = champion
        self.role = role
        
        if is_aram:
            url = champion.aram_link
            filename = f"./cache/{champion.name}_aram_stats.pickle"
        else:
            # get the champion page
            url = champion.link + "/" + role
            filename = f"./cache/{champion.name}_{role}_stats.pickle"
        
        req = RequestsHandler.Request(url, filename)
        req.load()

        soup = req.get_soup()
        
        # get the runes table
        class_tag = "champion-overview__table champion-overview__table--rune tabItems"
        table = soup.find("table", {"class":class_tag})    
        
        
        
        # find all tbody which contain the runes
        tbodies = table.find_all("tbody", recursive=False)
        

        self.runes_sets = []
        
        # skip the first table that isnt about the runes
        for tbody in tbodies[1:]:
            rune_sets = tbody.find_all("tr", recursive=False)
            
            for rune_set in rune_sets:
                runes_set = RunesSet(rune_set)
                self.runes_sets.append(runes_set)


    def get_runes_set(self, idx):
        return self.runes_sets[idx]



if __name__ == "__main__":
    cl = ChampionList.ChampionsList()
    
    champions_list = cl.parse_champions()
    
    champion = champions_list["Aatrox"]
    
    
    
    cp = ChampionPage(champion, champion.roles[0], True)
    
    
    rune_set = cp.get_runes_set(1)
    
    print(rune_set)
    
    rg1, rg2, rg3 = rune_set.get_groups()
    
    print(rg1.keystone.get_stone())


# #cp = ChampionPage(champions_list[0], champions_list[0].roles[0])


# for champion in champions_list:
#     if champion.name == "Maokai":
#         cp = ChampionPage(champion, champion.roles[0])     


# =============================================================================
# old Champion page body                
# =============================================================================

        # runes_sets = tbodies[0]
        # runes_set_1 = tbodies[2]
        # runes_set_2 = tbodies[2]
        
        
        # # from the rune set extract the runes:
        # runes_specs = runes_set_1.find_all("tr", recursive=False)
        
        # #print(len(runes_specs))
        
        # runes_specs_1 = runes_specs[0]
        # runes_specs_2 = runes_specs[1]
        
        # # find the keystones
        
        # keystones = runes_specs_1.find_all("div", {"class" : "perk-page__row"})
        
        
        
        # #print(len(keystones))        
        
        # print("--- First runes ---")
        

        # self.rune_list_1 = RuneGroup(keystones[0], keystones[1:5])
        
        
        # print(self.rune_list_1.keystone.get_stone())    
        # for row in self.rune_list_1.stone_rows:
        #     print("-----")
        #     stones = row.get_stones()
            
        #     for stone in stones:
        #         print(stone)
                
                
        # self.rune_list_2 = RuneGroup(keystones[4], keystones[5:9])
        
        
        # print(self.rune_list_2.keystone.get_stone())    
        # for row in self.rune_list_2.stone_rows:
        #     print("-----")
        #     stones = row.get_stones()
            
        #     for stone in stones:
        #         print(stone)
                
        
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

# =============================================================================
# old parsing funcitons            
# =============================================================================
        
    # def save_image_tag(self, stone):
    #     link = stone.find("img").get("src")
    #     pos = link.find("?")
        
    #     # prepare image link
    #     img_link = "https:" + link[:pos]
        
    #     # prepare image name
    #     image_name_start = img_link.rfind("/") + 1
    #     img_name = img_link[image_name_start:]
        
    #     img_name_no_ext, ext = os.path.splitext(img_name)
        
    #     img_req = RequestsHandler.Request(img_link, f"./cache/{img_name_no_ext}.pickle")
    #     img_req.load()
        
    #     img_filename = "./images/" + img_name
        
    #     img_req.save_image(img_filename)  
        
    #     return img_filename
    
    # def parse_key_rune(self, keystone):
    #     key_rune_link = keystone.find("img").get("src")
        
    #     pos = key_rune_link.find("?")
        
    #     # prepare image link
    #     img_link = "https:" + key_rune_link[:pos]
        
    #     # prepare image name
    #     image_name_start = img_link.rfind("/") + 1
    #     img_name = img_link[image_name_start:]
        
    #     img_name_no_ext, ext = os.path.splitext(img_name)
        
    #     img_req = RequestsHandler.Request(img_link, f"./cache/{img_name_no_ext}.pickle")
    #     img_req.load()
        
    #     img_req.save_image("./images/" + img_name)
               
    #     # get the code
    #     ext_pos = key_rune_link.find(".png")
        
    #     code = ""
    #     pos = ext_pos - 1
    #     while key_rune_link[pos] != "/" or pos == 0:
    #         code = key_rune_link[pos] + code
    #         pos -= 1
            
    #     #print(code)
            
    #     stone = Stone()
        
    #     stone.img_file = "./images/" + img_name
        
    #     return stone
        
    
    # def parse_stone(self, keystone):
    #     # if is the key stone the tag is this
    #     active_stone_tag = "perk-page__item perk-page__item--keystone perk-page__item--active"
    #     stone_page = keystone.find("div", {"class": active_stone_tag })      
        
    #     # else is this one
    #     if stone_page is None:
    #         active_stone_tag = "perk-page__item perk-page__item--active"
    #         stone_page = keystone.find("div", {"class": active_stone_tag }) 
            
    #     if stone_page:
        
    #         img_tag = stone_page.find("img")
    #         image_link = img_tag.get("src")
    #         image_name = img_tag.get("alt")
            
    #         print(image_name)
    #     else:
    #         print("No runes in this row")
        
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
            




