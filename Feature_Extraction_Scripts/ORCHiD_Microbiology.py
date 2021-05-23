# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 11:01:14 2019

@author: kebl4170
"""

import pandas as pd

def readTable(tablename, separator):
    output = pd.read_csv('Hamza/' + tablename, sep = separator)
    
    return(output)

class getMicroStats():
    
    def __init__(self):

        self.Microbiology = readTable('Part_5.csv', ',')

    def getTestRounds(self):
        subjects = pd.DataFrame(self.Microbiology.ClusterID.unique()).sort_values(0).reset_index(drop=True)
        Micro = self.Microbiology.drop_duplicates(subset=['ClusterID', 'CollectionDateTime'], keep='first')
        
        test_times =  Micro.groupby('ClusterID')['CollectionDateTime'].apply(lambda x: list(x)).reset_index() 
        test_times = pd.concat([test_times, test_times['CollectionDateTime'].apply(pd.Series).fillna(0)], axis=1)
        
        return(subjects, test_times)