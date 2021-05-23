# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 17:14:13 2019

@author: kebl4170
"""

from ORCHiD_DiagnosisStats import DiagnosisStats
import argparse

class Features():
    
    def __init__(self):
        self.ds = DiagnosisStats()
        
        
    def getInvestigations(self):
        
        ED_investigations = self.ds.getEDFeatures()
        
        return(ED_investigations)


def main(name):
    f = Features()
    ED_feats = f.getInvestigations()
    
    ED_feats.to_csv(name + '.csv', sep = ',', index=False)

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="specify folder to save data in")
    args = parser.parse_args()
    name = args.filename
    main(name)