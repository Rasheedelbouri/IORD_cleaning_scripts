# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 14:30:12 2019

@author: kebl4170
"""

import pandas as pd
import numpy as np

def readTable(tablename, separator):
    output = pd.read_csv('Hamza/' + tablename, sep = separator)
    
    return(output)


class DiagnosisStats():
    
    def __init__(self):
        self.Diagnoses = readTable('Part1_2.csv', ',')
        self.ED_admissions = readTable('Part1_ANEAdmission.csv', '\t')
        
    def getDiagnoses(self, plot = False):
        
        investigations = ['X-Ray', 'ECG', 'Haem', 'Cross-Match-Blood',
                          'Biochem', 'Urinalysis', 'Bacteriology',
                          'Ultrasound', 'MRI', 'CT', 'Clotting Study', 'Immunology',
                          'Cardiac Enzymes', 'Blood Gas', 'Toxicology', 'Blood Culture', 
                          'Serology', 'Pregnancy Test', 'Orthoptic Tests','None', 'Other']        
        
        mutuals = self.Diagnoses[self.Diagnoses.AttendanceID.isin(self.ED_admissions.AttendanceID)]
        uniq_invests = pd.DataFrame(mutuals.PrimaryInvestCode.unique()).sort_values(0).reset_index(drop=True)
        uniq_invests['counts'] = uniq_invests[0].map(mutuals.PrimaryInvestCode.value_counts())
        
        if plot == True:
            import matplotlib.pyplot as plt
            plt.bar(investigations[1:-5], uniq_invests['counts'])
        
        return(mutuals, investigations, uniq_invests)
        
        
    def separateAttendances(self):
        mutuals = self.getDiagnoses()
        uniq_attends = pd.DataFrame(mutuals.ClusterID.unique()).sort_values(0).reset_index(drop=True)
        uniq_attends['counts'] = uniq_attends[0].map(mutuals.ClusterID.value_counts())
        subject_admissions = mutuals.groupby('ClusterID')['AttendanceID'].apply(lambda x: list(x)).reset_index() 
        subject_admissions = pd.concat([subject_admissions, subject_admissions['AttendanceID'].apply(pd.Series).fillna(0)], axis=1)
    
        
        return(subject_admissions)
        
        
    def subjectDiagnoses(self):
         mutuals = self.getDiagnoses()
         mutuals = mutuals[mutuals.PrimaryDiagCodeFull.notnull()]
         subject_diagnoses = mutuals.groupby('ClusterID')['PrimaryDiagCodeFull'].apply(lambda x: list(x)).reset_index() 
         subject_diagnoses = pd.concat([subject_diagnoses, subject_diagnoses['PrimaryDiagCodeFull'].apply(pd.Series).fillna(0)], axis=1)
         
         return(subject_diagnoses)
         
    def getEDFeatures(self):
        mutuals, investigations, uniq_invests = self.getDiagnoses()
        #admiss_investigations = mutuals.groupby('AttendanceID')['PrimaryInvestCode'].apply(lambda x: list(x)).reset_index() 
        #admiss_investigations = pd.concat([admiss_investigations, admiss_investigations['PrimaryInvestCode'].apply(pd.Series).fillna(0)], axis=1)
        admiss_investigations = mutuals
        admiss_investigations['PrimaryInvestCode'] = admiss_investigations['PrimaryInvestCode'].astype(int)
        
        #mutuals = mutuals.sort_values('AttendanceID').reset_index(drop=True)
        admiss_investigations = admiss_investigations.sort_values('AttendanceID').reset_index(drop=True)
       

        
        ED_investigations = pd.DataFrame(np.zeros([len(admiss_investigations),len(uniq_invests)]))
        ED_investigations.columns = uniq_invests[0]
        for i in range(0, len(ED_investigations)):
            ED_investigations[admiss_investigations['PrimaryInvestCode'][i]][i] = 1
            print(i)
    
        ED_investigations.columns = investigations

    
        ED_investigations.insert(loc =0, column = 'AttendanceID', value = admiss_investigations['AttendanceID'])
        ED_investigations.insert(loc =0, column = 'ClusterID', value = admiss_investigations['ClusterID'])
        ED_investigations['PrimaryDiagCodeFull'] = admiss_investigations['PrimaryDiagCodeFull']
        ED_investigations['PrimaryTreatCodeFull'] = admiss_investigations['PrimaryTreatCodeFull']
        ED_investigations['SiteCode'] = admiss_investigations['SiteCode']
        ED_investigations['ArrivalDateTime'] = admiss_investigations['ArrivalDateTime']
        ED_investigations['DepartureDateTime'] = admiss_investigations['DepartureDateTime']

        
        return(ED_investigations)
            
            
            
            
class getPrimaryTreatmentStats(DiagnosisStats):
    

    def __init__(self, DiagnosisStats):
        self.Diagnoses = DiagnosisStats.Diagnoses
        self.ED_Admissions = DiagnosisStats.ED_admissions
    
    def getTreatments(self):
        mutuals = self.getDiagnoses()
        mutual_primary_treatments = pd.DataFrame(mutuals.PrimaryTreatCodeFull.unique()).sort_values(0).reset_index(drop=True)
        mutual_primary_treatments['counts'] = mutual_primary_treatments[0].map(mutuals.PrimaryTreatCodeFull.value_counts())
        
        return(mutual_primary_treatments)
        
         