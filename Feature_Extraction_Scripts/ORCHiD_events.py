# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 10:35:09 2019

@author: kebl4170
"""

import pandas as pd 
import numpy as np
import argparse

def readTable(tablename, separator):
    output = pd.read_csv('Hamza/' + tablename, sep = separator)
    
    return(output)


class eventStats():
    
    def __init__(self, plot = False, inpat = True):
        
        if inpat == False:
            self.events = readTable('Part_3a.csv', ',')
        else:
            self.events = readTable('Part_3a_Inpat.csv', ',')
            self.events.columns=['ArrivalDateTime', 'ClusterID', 'EventMilleniumCode', 'EventStartDateTime', 
                                 'EventEndDateTime', 'DisplayValue', 'EventTag']
        self.plot = plot

    def getEvents(self):
        event_list = pd.DataFrame(self.events.DisplayValue.unique()).sort_values(0).reset_index(drop=True)
        event_list['counts'] = event_list[0].map(self.events.DisplayValue.value_counts())
        
        if self.plot == True:
            import matplotlib.pyplot as plt
            plt.bar(event_list[0], event_list['counts'])
        
        return(event_list)
        
def main(events, event_list):
    events = events.drop_duplicates(['ClusterID', 'DisplayValue'], keep='first')        
    uniqs = pd.DataFrame(events.ClusterID.unique()).sort_values(0).reset_index(drop=True)
    new_test = pd.DataFrame(np.zeros((len(uniqs), len(event_list))))
    new_timesin = pd.DataFrame(np.zeros((len(uniqs), len(event_list))))
    new_timesout = pd.DataFrame(np.zeros((len(uniqs), len(event_list))))

    new_test.columns = event_list[0]
    new_timesin.columns = event_list[0] 
    new_timesout.columns = event_list[0] 

    for i in range(0, len(uniqs)):
        test = events[events.ClusterID == uniqs[0][i]].reset_index(drop=True)
        new_test.set_value(i, list(test.DisplayValue), list(test.EventTag))
        new_timesin.set_value(i, list(test.DisplayValue), list(test.EventStartDateTime))
        new_timesout.set_value(i, list(test.DisplayValue), list(test.EventEndDateTime))


        print(i)
    
    new_test.insert(loc =0, column = 'ClusterID', value = uniqs[0])
    new_timesin.insert(loc =0, column = 'ClusterID', value = uniqs[0])
    new_timesout.insert(loc =0, column = 'ClusterID', value = uniqs[0])
    
    return(new_test, new_timesin, new_timesout)


es = eventStats(inpat = True)
events = es.events
event_list = es.getEvents()

main(events, event_list)


    
    
if __name__ == '__main__':        

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="specify folder to save data in")
    args = parser.parse_args()
    name = args.filename    

    es = eventStats(inpat = True)
    events = es.events
    event_list = es.getEvents()
    physicals, physicalsDTin, physicalsDTout = main(events, event_list)
    
    physicals.to_csv(name + '.csv', sep = ',', index=False)
    physicalsDTin.to_csv(name + 'DTin.csv', sep = ',', index=False)
    physicalsDTout.to_csv(name + 'DTout.csv', sep = ',', index=False)
