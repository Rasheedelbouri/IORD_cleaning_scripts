# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 10:51:52 2019

@author: kebl4170
"""

import pandas as pd


def readTable(tablename, separator):
    output = pd.read_csv('Hamza/' + tablename, sep = separator)
    
    return(output)

tests = readTable('Part_4a.csv', ',')