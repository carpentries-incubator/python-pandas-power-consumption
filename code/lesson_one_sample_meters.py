# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 11:40:30 2023

@author: jwheel01
"""

#%% import libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import glob

#%% define functions

def subsample_year(start_year, end_year, data):
    try:
        data.set_index(pd.to_datetime(data["INTERVAL_TIME"]), inplace=True)
        data.sort_index(inplace=True)
        in_sample = start_year in data.index and end_year in data.index
        return in_sample
    except:
        return


#%% get a list of data files

file_list = glob.glob('./LADPU/*.csv')

#%% remove files that don't include complete date range
# earliest start date 2013-05-06 (use 2014-01-01)
# latest end date 2020-01-01 (use 2019-12-31)

# store file names in set
years_sample = set()

# define years to include
# all items in the sample will have some data for all years included
start_year = "2014-01-01"
end_year = "2019-12-31"

counter = 1
for f in file_list:
    print(counter, f)
    data = pd.read_csv(f)
    if subsample_year(start_year, end_year, data):
        years_sample.add(f)
    counter += 1
    print(len(years_sample))

#%% save year_sample to file

with open('year_sample.txt', 'w') as o:
    for f in years_sample:
        o.write(str(f) + '\n')
        
#%% random select 10 files

# convert to df
df = pd.DataFrame(years_sample)
meters_sample = df.sample(10)

#%% save to file

meters_sample.to_csv("meter_sample_10_lesson_1.csv", index=False)



