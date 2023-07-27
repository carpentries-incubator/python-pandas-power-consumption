# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 13:27:05 2023

@author: jwheel01
"""

#%% import libaries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% define functions

def read_index(file):
    df = pd.read_csv(file, parse_dates=True,
                     infer_datetime_format=True,
                     index_col="INTERVAL_TIME")
    df.sort_index(inplace=True)
    return df


def date_subset(start_date, end_date, data):
    subset_data = data.loc[start_date: end_date].copy()
    return subset_data


def check_null(data):
    return data.isnull().values.any()


def check_duplicates(data):
    return data.index.duplicated().any()


def quick_plot(data, f):
    fig, ax = plt.subplots()
    ax.plot(data["INTERVAL_READ"])
    ax.set_xlabel('Time')
    ax.set_ylabel('Energy consumption')

    fig.autofmt_xdate()
    plt.title(f)
    plt.tight_layout()
    plt.show()
    return


def deduplicate_index(data):
    # on inspection of some duplicate "INTERVAL_TIME" values
    # closest way to approximate the daily total (within one decimal point)
    # was to sum the values of the duplicated rows
    sum_duplicates = data.groupby(data.index).agg({"METER_FID": 'first',
                                                   "START_READ": 'first',
                                                   "END_READ": 'first',
                                                   "INTERVAL_READ": sum})
    return sum_duplicates


def agg_plot(data, f):
    subset_cols = data.drop(columns=['METER_FID', 'START_READ', 'END_READ'])
    week_resample = subset_cols.resample('W')
    week_totals = week_resample.aggregate([np.sum])
    month_resample = subset_cols.resample('M')
    month_totals = month_resample.aggregate([np.sum])
    
    fig, ax = plt.subplots()
    
    ax.plot(week_totals, label='Weekly')
    ax.plot(month_totals, label='Monthly')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Electricity consumption')
     
    ax.legend(loc=2)
    
    plt.title('Power consumption: ' + str(f))
    plt.tight_layout()
    plt.show()
    
    return

#%% inspect data per file

# get random subset of 10 files
year_sample = pd.read_csv('year_sample.txt')
flist = year_sample.sample(10)

# see if we can randomly get 10 files with no zero values
no_null = set()
no_dupes = set()
few_zeros = set()
#%% read and plot data for each file

counter = 1
for i, r in year_sample.iterrows():
    data = read_index(r['filepath'])
    # on inspection much of the missing data appears to be before 2017
    # three years of data is sufficient for lesson 1 objectives
    data = date_subset("2017-01-01", "2019-12-31", data)
    #has_null = check_null(data)
    has_dupes = check_duplicates(data)
    if has_dupes:
        data = deduplicate_index(data)
    has_null = check_null(data)
    has_dupes = check_duplicates(data)
    if not has_null:
        no_null.add(r['filepath'])
        if not has_dupes:
            no_dupes.add(r['filepath'])
            # there is only one meter which has no zero values
            # since we are unsure if readings == 0 are valid or not
            # we will leave them in place but limit sample to meters
            # that have a fraction of INTERVAL_READ == 0
            # on average 15 readings == 0.01% of a meter's readings
            # over 3 years
            if len(data[data['INTERVAL_READ'] == 0]) < 10:
                few_zeros.add(r['filepath'])
    print(counter, r['filepath'], len(no_null), len(no_dupes), len(few_zeros))
    counter += 1           
    

#%% from the set of few_zeros select 10 at random

subset_datasets = pd.DataFrame(few_zeros)
subset_datasets.rename(columns={0: 'filepath'}, inplace=True)


#%% inspect the 10 files and plot

for i, r in subset_datasets.iterrows():
    data = read_index(r['filepath'])
    # on inspection much of the missing data appears to be before 2017
    # three years of data is sufficient for lesson 1 objectives
    data = date_subset("2017-01-01", "2019-12-31", data)
    #has_null = check_null(data)
    has_dupes = check_duplicates(data)
    if has_dupes:
        data = deduplicate_index(data)
    has_null = check_null(data)
    has_dupes = check_duplicates(data)
    print(r['filepath'], 'has null values:', has_null)
    print(r['filepath'], 'has duplicate data:', has_dupes, "\n")  
    print(data[data["INTERVAL_READ"] == 0].info())         
    quick_plot(data, r['filepath'])
    agg_plot(data, r['filepath'])
    
#%% inspect a further subset based on plots

final_subset = [285, 10063, 44440, 4348, 45013, 
                32366, 24197, 18918, 35034, 42755, 
                25188, 29752, 20967, 12289, 8078]

for i in final_subset:
    fpath = './LADPU\\' + str(i) + '.csv'
    data = read_index(fpath)
    # on inspection much of the missing data appears to be before 2017
    # three years of data is sufficient for lesson 1 objectives
    data = date_subset("2017-01-01", "2019-12-31", data)
    #has_null = check_null(data)
    has_dupes = check_duplicates(data)
    if has_dupes:
        data = deduplicate_index(data)
    has_null = check_null(data)
    has_dupes = check_duplicates(data)
    print(fpath, 'has null values:', has_null)
    print(fpath, 'has duplicate data:', has_dupes, "\n")  
    print(data[data["INTERVAL_READ"] == 0].info())         
    quick_plot(data, fpath)
    agg_plot(data, fpath)
    
#%% save subsets to file

f_counter= 1
for i in final_subset:
    fpath = './LADPU\\' + str(i) + '.csv'
    data = read_index(fpath)
    # on inspection much of the missing data appears to be before 2017
    # three years of data is sufficient for lesson 1 objectives
    data = date_subset("2017-01-01", "2019-12-31", data)
    #has_null = check_null(data)
    has_dupes = check_duplicates(data)
    if has_dupes:
        data = deduplicate_index(data)
    has_null = check_null(data)
    has_dupes = check_duplicates(data)
    print(fpath, 'has null values:', has_null)
    print(fpath, 'has duplicate data:', has_dupes, "\n")  
    out_path = './LADPU_meter_data_subset/ladpu_smart_meter_data_' + str(f_counter) + '.csv'
    data.to_csv(out_path, index=False)
    f_counter += 1
    
