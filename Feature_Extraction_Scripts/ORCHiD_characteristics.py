# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 16:06:49 2019

@author: kebl4170
"""

import pandas as pd
import argparse

def readTable(tablename, separator):
    output = pd.read_csv('Hamza/' + tablename, sep = separator)
    
    return(output)
    
class characteristics():
    
    def __init__(self):
        
        self.character = readTable('Part10_13_AnE.csv', ',')
        
        
    def getUniques(self):
        chars = pd.DataFrame(self.character.ClusterID.unique())
        self.character = self.character.drop_duplicates('ClusterID', keep = 'first')
        
        return(self.character)
        
def main(name):
    
    ch = characteristics()
    character = ch.getUniques()
    
    character.to_csv(name + '.csv', sep = ',', index = False)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="specify folder to save data in")
    args = parser.parse_args()
    name = args.filename
    main(name)
    
        
        