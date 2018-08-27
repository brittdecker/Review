# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script to plot data from COMSOL simulations. This script assumes the data is
formatted such that x number of initial conditions appear first, then the time column, 
then y number of data columns. For example:

Condition 1 | Cond X... | Time | Dataset 1 | Dataset Y... |

"""

import pandas as pd

import matplotlib.pyplot as plt

path='C:/Sandbox/testdata/pyfile.pkl'

#import the datafile, skip first 4 rows of header info
df = pd.read_csv('C:/Sandbox/testdata/data_24Aug_thermistor.csv', skiprows = 4)
#specify the columns where the initial condition names are given
subValues = {'v1': df.columns[0],
             'v2': 0,
             'v3': df.columns[1],
             'v4': 0}

#
col = list(df.columns.values)

connum=0 #number of conditions, set to 0 initially
z=0
i = 0

#find the number of conditions
while df.columns[z] != 'Time':
    connum=connum+1
    z=z+1
#assume there's always 1 condition. set cond1 to the first condition column   
cond1=df.columns[0]

#if there are 2 conditions, set the next column to cond2, time to column 3, and update the dictionary
if connum>1:
    cond2=df.columns[1]
    subPlotTitle = '{v1} = {v2}, {v3} = {v4}'
    time=df.columns[2]
    if df[cond2][0]>100:
        subValues['v4'] = df[cond2][0]-273.15
    else:
        subValues['v4'] = df[cond2][0]
    
#otherwise, there is just 1 condition, so time is column two
else:  
    time=df.columns[1]
    subPlotTitle = '{v1} = {v2}'

#group the data by the first column. Turn off sorting (sorts in ascending order)
dfg = df.groupby(df[cond1], sort=False)

#find the number of datapoints in each plot (total datapoints / number of "groups")
ndp = len(df)/len(dfg)

#figure out the number of subplot positions required
nPlots = len(dfg)
xWidth = 4
yWidth = int(nPlots/4)
if (nPlots%4) > 0:
    yWidth += 1
f, ax = plt.subplots(nrows = yWidth, ncols = xWidth)

#begin plotting
for name, group in dfg:
    print(name)
    axes = ax[int(i/4), i%4]
    for item in col[connum+1:]:    
        axes.plot(group[time], group[item])
    axes.legend(col[connum+1:])
    #make sure that the temperature is in Celcius  and update the condition values
    if name>100:  
        subValues['v2'] = df[cond1][i*ndp]-273.15
        if connum>1:
            subValues['v4'] = df[cond2][i*ndp]-273.15         
    else:
        subValues['v2'] = df[cond1][i*ndp]
        if connum>1:
            subValues['v4'] = df[cond2][i*ndp]  
    #set axis lables and title
    axes.set_title(subPlotTitle.format(**subValues)) 
    axes.set(xlabel="Time (s)", ylabel="Temperature (C)")    
    i +=1  


