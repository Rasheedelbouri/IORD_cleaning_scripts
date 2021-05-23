# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 13:56:35 2019

@author: kebl4170
"""

from ORCHiD_admissions_features import WardStats
from ORCHiD_events import eventStats
import pandas as pd
import numpy as np
import sys
import argparse

def readTable(tablename, separator):
    output = pd.read_csv(tablename, sep = separator)
    
    return(output)
    
class combiner():
    
    def __init__(self):
        
        self.ED_tests = readTable('ED_tests_Features.csv', ',')
        self.admissions = readTable('admission_features.csv', ',')
        self.characs = readTable('ED_characteristics.csv', ',')
        self.physicals = readTable('physicals.csv', ',')
        
    def concatenate_admits(self, drop_duplicates = True):
        
        self.ED_tests = self.ED_tests[self.ED_tests.ClusterID.isin(self.admissions.ClusterID)]
        self.admissions = self.admissions[self.admissions.ClusterID.isin(self.ED_tests.ClusterID)]
        
        self.ED_tests = self.ED_tests.sort_values('ClusterID').reset_index(drop=True)
        self.admissions = self.admissions.sort_values('ClusterID').reset_index(drop=True)
        
        if sum(self.ED_tests.ClusterID.unique() - self.admissions.ClusterID.unique()) != 0:
            sys.exit('Patient Data is not aligned')
            
        if drop_duplicates == True:
            self.ED_tests = self.ED_tests.drop_duplicates('ClusterID', keep = 'first')
            
        self.ED_tests = self.ED_tests.reset_index(drop=True)
        self.ED_tests['LOS'] = self.admissions.LOS
        self.ED_tests['initial_location'] = self.admissions.initial_location
        
        
    def concatenate_characs(self):
        self.characs = self.characs[self.characs.ClusterID.isin(self.ED_tests.ClusterID)]
        self.ED_tests = self.ED_tests[self.ED_tests.ClusterID.isin(self.characs.ClusterID)]
        
        self.characs = self.characs.sort_values('ClusterID').reset_index(drop=True)
        self.ED_tests = self.ED_tests.sort_values('ClusterID').reset_index(drop=True)
        
        if sum(self.characs.ClusterID - self.ED_tests.ClusterID) != 0:
            sys.exit('Patient data is not aligned')
        
        self.characs = self.characs.drop(['ClusterID', 'idsetuid'], axis=1)
        
        self.ED_tests = pd.concat([self.ED_tests, self.characs], axis=1)
        
    def concatenate_physicals(self):
        self.physicals = self.physicals[self.physicals.ClusterID.isin(self.ED_tests.ClusterID)]
        self.ED_tests = self.ED_tests[self.ED_tests.ClusterID.isin(self.physicals.ClusterID)]
        
        self.physicals = self.physicals.sort_values('ClusterID').reset_index(drop=True)
        self.ED_tests = self.ED_tests.sort_values('ClusterID').reset_index(drop=True)
        
        if sum(self.physicals.ClusterID - self.ED_tests.ClusterID) != 0:
            sys.exit('Patient data is not aligned')
            
        self.physicals = self.physicals.drop(['ClusterID'], axis=1)
        
        self.ED_tests = pd.concat([self.ED_tests, self.physicals], axis=1)
        
    def encode(self):
        
        alpha_uniq_trans_locs = WardStats().getUniqueWards()
        
        for i in range(0,len(self.ED_tests)):
            self.ED_tests['initial_location'][i] = alpha_uniq_trans_locs.loc[alpha_uniq_trans_locs[0] == self.ED_tests['initial_location'][i]].index[0]
            print(i)
            
        self.ED_tests['LinkedSex'] = self.ED_tests['LinkedSex'].map({'F': 1, 'M': 0})
        self.ED_tests['EthnicGroupCode'] = self.ED_tests['EthnicGroupCode'].map({'A ':0, 'B ':1, 'C ':2, 'D ':3, 
                                                                                'E ':4, 'F ':5, 'G ':6, 'H ':7,'J ':8, 
                                                                                'K ':9, 'L ':10, 'M ':11, 'N ':12, 
                                                                                'P ':13, 'R ':14, 'S ':15, 
                                                                                'Z ':16, '99':16})
       
        
        self.ED_tests['Infection Concern'][self.ED_tests['Infection Concern'].str.contains('No')] = 0
        self.ED_tests['Infection Concern'][self.ED_tests['Infection Concern'] == 'Yes'] = 1            
        
        self.ED_tests['Suspected Alert'][self.ED_tests['Suspected Alert'].isin(['S', 'SepsiS', 's'])] = 1
        self.ED_tests['Suspected Alert'][self.ED_tests['Suspected Alert'] == 'O'] = 0            
        
        self.ED_tests['Suspected sepsis'][self.ED_tests['Suspected sepsis'].isin(['Not for active treatment', 'Resolved', 'Sepsis', 'Yes'])] = 1
        self.ED_tests['Suspected sepsis'][self.ED_tests['Suspected sepsis'] == 'No'] = 0   
                                                                  
        self.ED_tests['Tracheostomy mask monitoring'][self.ED_tests['Tracheostomy mask monitoring'] == 'No'] = 0
        self.ED_tests['Tracheostomy mask monitoring'][self.ED_tests['Tracheostomy mask monitoring'] == 'Yes'] = 1
                                                                            
                                                                            
                                                                            
                                                                            
    def clean(self):
        self.ED_tests = self.ED_tests[~self.ED_tests['AVPU Scale'].isin(['In Error', 'In Progress'])]
        self.ED_tests = self.ED_tests[~self.ED_tests['Diastolic Blood Pressure'].isin(['*NOT VALUED*','Date/Time Correction',
                                                                                      'In Error', 'In Progress', 'Refused'])]
        self.ED_tests = self.ED_tests[~self.ED_tests['FiO2 concentration'].isin(['*NOT VALUED*', 'In Error', 'In Progress'])]
        self.ED_tests = self.ED_tests[~self.ED_tests['Heart Rate'].isin(['*NOT VALUED*','Date/Time Correction',
                                                                                      'In Error', 'In Progress', 'Refused'])]  
        self.ED_tests = self.ED_tests[~self.ED_tests['Infection Concern'].isin(['In Error', 'In Progress'])]
        self.ED_tests = self.ED_tests[~self.ED_tests['Oxygen L/min delivered'].isin(['In Error', 'Refused', 'Date/Time Correction'])]
        self.ED_tests = self.ED_tests[~self.ED_tests['Oxygen Saturation'].isin(['Date/Time Correction',
                                                                                      'In Error', 'In Progress', 'Refused'])] 
        self.ED_tests = self.ED_tests[~self.ED_tests['Respiratory Rate'].isin(['Date/Time Correction',
                                                                                      'In Error', 'In Progress', 'Refused'])] 
        self.ED_tests = self.ED_tests[~self.ED_tests['Systolic Blood Pressure'].isin(['*NOT VALUED*','Date/Time Correction',
                                                                                      'In Error', 'In Progress', 'Refused'])]                                                                              
        self.ED_tests = self.ED_tests[~self.ED_tests['Temperature Tympanic'].isin(['Date/Time Correction',
                                                                                      'In Error', 'In Progress', 'Refused'])]                                                                                 
        self.ED_tests = self.ED_tests[~self.ED_tests['Tracheostomy mask monitoring'].isin(['In Error'])]

        
        return(self.ED_tests)
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="specify folder to save data in")
    parser.add_argument("--stage", type = int , help = "Number of minutes to round LOS data to")
    args = parser.parse_args()    
    
    name = args.name
    stage = args.stage
    
    comb = combiner()
    print('Agent Allocated')
    print('Adding admission data')
    comb.concatenate_admits(drop_duplicates = True)
    if stage == 1:
        comb.ED_tests.to_csv(name + '.csv', sep = ',', index=False)
        sys.exit('First stage of features saved')
    print('Adding characteristics')
    comb.concatenate_characs()
    if stage ==2:
        comb.ED_tests.to_csv(name + '.csv', sep = ',', index=False)
        sys.exit('Second stage of features saved')
    print('Adding physical data')
    comb.concatenate_physicals()
    if stage ==3:
        comb.ED_tests.to_csv(name + '.csv', sep = ',', index=False)
        sys.exit('Third stage of features saved')
    print('Encoding data')
    comb.encode()
    print('cleaning up')
    features = comb.clean()
    
    print('saving to memory')
    features.to_csv('combined_features.csv', sep=',', index=False)
    
if __name__ == '__main__':
    main()
    
    
        
        