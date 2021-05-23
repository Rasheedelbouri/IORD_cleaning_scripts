# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 12:17:17 2019

@author: kebl4170
"""

import pandas as pd
import numpy as np

def readTable(tablename, separator):
    output = pd.read_csv('Hamza/' + tablename, sep = separator)
    
    return(output)

ED_admits = readTable('Part1_ANEAdmission.csv', '\t')
Wards = readTable('Part1_WardStay.csv', '\t')
Admissions = readTable('Part_11.csv', ',')

WardEntry = Wards[Wards['WardStartDate'].isin(ED_admits['DepartureDateTime'])]
ED_admissions = ED_admits[ED_admits['DepartureDateTime'].isin(WardEntry['WardStartDate'])]

uniqs = pd.DataFrame(WardEntry['ClusterID'].unique())


cluster_uniq_admits = ED_admissions.groupby('ClusterID')['DepartureDateTime'].apply(lambda x: list(x)).reset_index() #Grouping admission ID's according to the wards they are admitted to
cluster_uniq_admits = pd.concat([cluster_uniq_admits, cluster_uniq_admits['DepartureDateTime'].apply(pd.Series).fillna(0)], axis=1) # splitting the patient journeys into individual columns per location

cluster_uniqs = ED_admissions.groupby('ClusterID')['AttendanceID'].apply(lambda x: list(x)).reset_index() #Grouping admission ID's according to the wards they are admitted to
cluster_uniqs = pd.concat([cluster_uniqs, cluster_uniqs['AttendanceID'].apply(pd.Series).fillna(0)], axis=1) # splitting the patient journeys into individual columns per location




