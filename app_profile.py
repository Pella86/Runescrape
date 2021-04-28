# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 11:55:56 2021

@author: maurop
"""


import cProfile
import pstats

import GUI

cProfile.run("GUI.run_app()", "profile_stats")

with open('readable_stats.txt', 'w') as stream:
    p = pstats.Stats("profile_stats", stream=stream)
    
    p.sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
    

with open("readable_stats.txt", "r") as f:
    
    lines = f.readlines()


dir_path = r'C:\Users\Media Markt\Desktop\Vita Online\LoL\runescrape' + "\\"    

filtered_stats = lines[:7]
for line in lines[7:]:
    if dir_path in line:
        filtered_stats.append(line.replace(dir_path, ""))


with open("readable_stats_filtered.txt", "w") as f:
    f.write("".join(filtered_stats))
    