# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 13:29:01 2019

@author: kebl4170
"""

import pandas as pd

def readTable(tablename, separator, numrows = 500000):
    output = pd.read_csv('Hamza/' + tablename, sep = separator, nrows = numrows)
    
    return(output)


treatments = readTable('Part_2.csv', ',', numrows = 500000)
treatments = treatments[treatments.TreatCode.notnull()]
times = treatments.drop_duplicates(subset=['ArrivalDateTime', 'DepartureDateTime'], keep='first')
