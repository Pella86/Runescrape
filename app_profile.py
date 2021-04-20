# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 11:55:56 2021

@author: maurop
"""


import cProfile
import GUI

pstat = cProfile.run(GUI.run_app())


pstat.print_stats()