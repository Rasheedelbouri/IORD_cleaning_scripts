# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 10:14:01 2019

@author: kebl4170
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse

def readTable(tablename, separator):
    output = pd.read_csv('Hamza/' + tablename, sep = separator)
    
    return(output)


class WardStats():
    
    def __init__(self):
        self.Admissions = readTable('Part1_2.csv', ',')
        self.ED_admissions = readTable('Part1_ANEAdmission.csv', '\t')
        self.Wards_df = readTable('Part1_WardStay.csv', '\t')

    def getUniqueWards(self):
        unique_wards = pd.DataFrame(self.Wards_df['WardName'].unique()).sort_values(0).reset_index(drop=True)
        unique_wards['counts'] = unique_wards[0].map(self.Wards_df['WardName'].value_counts())
        
        return(unique_wards)
    
    def getEmergencyWards(self):
        ed_id = pd.DataFrame(self.ED_admissions['ClusterID'].unique())
        emerg_wards = self.Wards_df[self.Wards_df['ClusterID'].isin(ed_id[0])]
        emerg_uniques = pd.DataFrame(emerg_wards.WardName.unique()).sort_values(0).reset_index(drop=True) ### not quite true
        emerg_uniques['counts'] = emerg_uniques[0].map(emerg_wards['WardName'].value_counts())
    
        return(emerg_wards, emerg_uniques)
        
        
    def getSubjectWardHistory(self):
        emerg_wards, emerg_uniques = self.getEmergencyWards()
        ward_journey = emerg_wards.groupby('ClusterID')['WardName'].apply(lambda x: list(x)).reset_index() 
        ward_journey = pd.concat([ward_journey, ward_journey['WardName'].apply(pd.Series).fillna(0)], axis=1)

        return(ward_journey)
        
    def getWardHistoryDistribution(self):
        from matplotlib.patches import Polygon
        ward_journey = self.getSubjectWardHistory()
        counter = np.zeros(np.shape(ward_journey)[1])
        for i in range(0,len(ward_journey)):
            counter[len(ward_journey.WardName[i])] += 1
            print(i)
        fig, ax = plt.subplots()
        plt.plot(counter)
        plt.xlabel('Number of Wards Admitted to in Patient\'s history')
        plt.ylabel('Number of Patients Admitted')
        ix = np.linspace(10, 200)
        iy = counter[10:200]
        verts = [(10, 0), *zip(ix, iy), (200, 0)]
        poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
        ax.add_patch(poly)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.set_xticks((10, 200))
        ax.set_xticklabels(('$10$', '$200$'))
        ax.set_yticks([])
        plt.text(0.5 * (10 + 200), 20000, r"Only 10% of patients use 10 or more wards in their whole history",
                 horizontalalignment='center', fontsize=8)
        
    def getED_LOS(self, mins = 10, plot = False):
        from Allmyfunctions import round_timedelta
        self.ED_admissions.ArrivalDateTime = self.ED_admissions.ArrivalDateTime.apply(pd.to_datetime, errors = 'coerce')
        self.ED_admissions.DepartureDateTime = self.ED_admissions.DepartureDateTime.apply(pd.to_datetime, errors = 'coerce')
        filteredDF = self.ED_admissions[self.ED_admissions.DepartureDateTime.notnull()]
        filteredDF['LOS'] = filteredDF.DepartureDateTime - filteredDF.ArrivalDateTime
        filteredDF = filteredDF.reset_index(drop=True)
        filteredDF['LOS'] = round_timedelta(filteredDF['LOS'], 60*mins)
        filteredDF['LOS'] = filteredDF['LOS']/3600
        
        if plot == True:
            unique_times = pd.DataFrame(filteredDF['LOS'].unique()).sort_values(0).reset_index(drop=True)
            unique_times['counts'] = unique_times[0].map(filteredDF['LOS'].value_counts())
            import matplotlib.pyplot as plt
            plt.plot(unique_times[0][0:70], unique_times['counts'][0:70])
            plt.xlabel('LOS (Hours)')
            plt.ylabel('Number of Patients Experiencing ED LOS')
        
        return(filteredDF)
                
        

class generateAdmissions(WardStats):
    
    def __init__(self, WardStats):
        self.Wards_df = WardStats.Wards_df
        self.Admissions = WardStats.Admissions
        
    def getSubjectTimeBlock(self, mins = 10, plot = False):
        filtered_admissions = self.Admissions[self.Admissions.DepartureDateTime.notnull()]
        from Allmyfunctions import round_timedelta
        filtered_admissions.ArrivalDateTime = filtered_admissions.ArrivalDateTime.apply(pd.to_datetime, errors = 'coerce')
        filtered_admissions.DepartureDateTime = filtered_admissions.DepartureDateTime.apply(pd.to_datetime, errors = 'coerce')
        filtered_admissions['LOS'] = filtered_admissions.DepartureDateTime - filtered_admissions.ArrivalDateTime
        filtered_admissions = filtered_admissions.reset_index(drop=True)
        filtered_admissions['LOS'] = round_timedelta(filtered_admissions['LOS'], 60*mins)
        filtered_admissions['LOS'] = filtered_admissions['LOS']/3600
        filtered_admissions = filtered_admissions[filtered_admissions['LOS'] >= 0]
        
        if plot == True:
            unique_times = pd.DataFrame(filtered_admissions['LOS'].unique()).sort_values(0).reset_index(drop=True)
            unique_times['counts'] = unique_times[0].map(filtered_admissions['LOS'].value_counts())
            import matplotlib.pyplot as plt
            plt.plot(unique_times[0][0:70], unique_times['counts'][0:70])
            plt.xlabel('LOS (Hours)')
            plt.ylabel('Number of Patients Experiencing ED LOS')
        
        return(filtered_admissions)





def main(mins, plot):
    
    tableAgent = WardStats()
    admission_agent = generateAdmissions(tableAgent)
    print('Agents assigned')
    
    emerg_wards, emerg_uniques = tableAgent.getEmergencyWards()
    ward_journey = tableAgent.getSubjectWardHistory()
    print('ward history extracted')

    admits = admission_agent.getSubjectTimeBlock(mins=10, plot = False)
    print('admissions obtained')

    ward_journey = ward_journey[ward_journey.ClusterID.isin(admits.ClusterID)].sort_values('ClusterID').reset_index(drop=True)
    admits = admits[admits.ClusterID.isin(ward_journey.ClusterID)].sort_values('ClusterID').reset_index(drop=True)
    
    if sum(ward_journey.ClusterID.unique() - admits.ClusterID.unique())!=0:
        sys.exit('Tables are not aligned')
    
    admits = admits.drop_duplicates('ClusterID', keep='first').reset_index(drop=True)
    admits['initial_location'] = ward_journey[0]
    admits = admits[admits.columns[~admits.columns.str.contains('DateTime')]]
    admits = admits.reset_index(drop=True)
    print('comparison complete, saving features')
    #tableAgent.getWardHistoryDistribution()
    #filteredDF = tableAgent.getED_LOS(plot=plot)
    
    return(admits)
    


if __name__ == '__main__':
     parser = argparse.ArgumentParser()
     parser.add_argument("name", help="specify folder to save data in")
     parser.add_argument("--mins", type = int , help = "Number of minutes to round LOS data to")
     parser.add_argument('--plot', type = bool , help = 'Choose to plot distribution of LOS or not')
     args = parser.parse_args()
 
     name = args.name
     mins = args.mins
     plot = args.plot
     admits = main(mins, plot)
     
     admits.to_csv(name + '.csv', sep = ',', index=False)
