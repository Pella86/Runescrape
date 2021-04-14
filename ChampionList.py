# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 14:19:21 2021

@author: maurop
"""

import RequestsHandler

# base page of op.gg
base_url = "https://euw.op.gg"

# champions list page
champions_list_page = base_url + "/champion/statistics"

# the file where the page will be stored
cache_filename = "./cache/main_statistc_page.pickle"

# The selector in the html page of the champions list to get the div
# containing the champions names and roles
champ_selector = "body > div.l-wrap.l-wrap--champion > div.l-container > div.l-champion-index > div.l-champion-index-content > div.l-champion-index-content--main > div.champion-index__champion-list"

class Champion:
    
    def __init__(self, name, link, roles, aram_link):
        self.name = name
        self.link = link
        self.roles = roles
        self.aram_link = aram_link

    
class ChampionsList:
    
    def __init__(self):
        
        # make the request
        req = RequestsHandler.Request(champions_list_page, cache_filename)
        req.load()
        
        soup = req.get_soup()
        
        # select the div corresponding to the champions
        champs = soup.select(champ_selector)
        
        # all the first children of the selector are the champion list
        self.champions_list = champs[0].find_all("div", recursive=False)
        
        n_champions = len(self.champions_list)
        print(f"Retrived {n_champions} champions")
        
        
    def parse_champions(self):
        print("parsing champion list...")
        
        # store the parsed champions with name, link and roles
        champions_list_parsed = {}
        
        for champion in self.champions_list:
            
            # get the string of the champion name
            name = champion.find("div", {"class":"champion-index__champion-item__name"})
            name = name.getText()
            
            # get the link
            link = champion.find("a")
            
            # gets the link if it exists
            if link:
                link = base_url + link.get("href")
            else:
                link = None
                
            # get the roles
            roles_html = champion.find_all("span")
            roles = []
            for role in roles_html:
                role = role.getText()
                roles.append(role)
            
            aram_link = base_url  + "/aram/" + name + "/statistics"
            champions_list_parsed[name] = Champion(name, link, roles, aram_link)
        return champions_list_parsed
        
        