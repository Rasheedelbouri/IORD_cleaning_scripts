# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 11:17:39 2019

@author: kebl4170
"""

import pandas as pd
import numpy as np

def readTable(tablename, separator, numrows):
    output = pd.read_csv('Hamza/' + tablename, sep = separator, nrows = numrows)
    
    return(output)
    

class getEpisodes():
    
    def __init__(self, numrows = 1000000):

        self.episodes = readTable('Part_11.csv', ',', numrows)


    def getReducedEpisodes(self):
        
        episodes = self.episodes.drop_duplicates(subset=['ClusterID', 'EpisodeID'], keep = 'first')

        return(episodes)


    def getSubject2Episode(self, reduced = True):
    
        if reduced != True:
            subject_to_episode =  self.episodes.groupby('ClusterID')['EpisodeID'].apply(lambda x: list(x)).reset_index() 
            subject_to_episode = pd.concat([subject_to_episode, subject_to_episode['EpisodeID'].apply(pd.Series).fillna(0)], axis=1)
            
        else:
            episodes = self.getReducedEpisodes()
            subject_to_episode =  episodes.groupby('ClusterID')['EpisodeID'].apply(lambda x: list(x)).reset_index() 
            subject_to_episode = pd.concat([subject_to_episode, subject_to_episode['EpisodeID'].apply(pd.Series).fillna(0)], axis=1)
        
        return(subject_to_episode)
        
        
    def getDiagList(self):
        episodes = self.getReducedEpisodes()
        diagnosis_list = pd.DataFrame(episodes.DiagCode.unique()).sort_values(0).reset_index(drop=True)
        diagnosis_list['counts'] = diagnosis_list[0].map(episodes.DiagCode.value_counts())
        
        return(diagnosis_list)
        
    def getWardVisits(self):
        from first_orchid_script import WardStats
        alpha_uniq_trans_locs = WardStats().getUniqueWards()
        episode_ward_list = pd.DataFrame(self.getReducedEpisodes().FirstWard).reset_index(drop=True)
        adapted = self.getReducedEpisodes()[['FirstWard', 'LastWard']].reset_index(drop=True)
        adapted.columns=[0,1]
        adapted = adapted[adapted[0].notnull()]
        adapted = adapted[adapted[1].notnull()]
        adapted = adapted[adapted[0] != 'null ward name']
        adapted = adapted[adapted[1] != 'null ward name']
        adapted = adapted.reset_index(drop=True)
        tm = self.Get_Transition_Matrix(alpha_uniq_trans_locs, adapted)
        
        return(tm, alpha_uniq_trans_locs)
        
        
    def Get_Transition_Matrix(self, alpha_uniq_trans_locs, ward_codedf): # Function takes in the uniq locations and ward code dataframe
        Transition_Matrix = np.zeros((len(alpha_uniq_trans_locs) ,len(alpha_uniq_trans_locs))) # initialise the transition matrix
        for i in range(0,len(ward_codedf)): # loop through every individual patients journey            
                    
                    Transition_coord1 = alpha_uniq_trans_locs.loc[alpha_uniq_trans_locs[0] == ward_codedf[i:i+1][0][i]].index[0]   # Finding the index in the catalogue of unique locations
                    Transition_coord2 = alpha_uniq_trans_locs.loc[alpha_uniq_trans_locs[0] == ward_codedf[i:i+1][1][i]].index[0] # Finding the index in the catalogue of unique locations
        
                    Transition_Matrix[Transition_coord1 , Transition_coord2] = Transition_Matrix[Transition_coord1, Transition_coord2] + 1 #updating the location in the matrix by adding 1
    
                    print(i)
        return Transition_Matrix   #output the final transition matrix

ge = getEpisodes()
dl = ge.getDiagList()
    