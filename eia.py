#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 15:33:25 2018

@author: jimgrund
"""

import os
### Provide the path here
os.chdir('/Users/jimgrund/Documents/GWU/machine learning/final-project/data') 

### Basic Packages
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import scipy.stats as stats
import matplotlib.dates as mdates


# Table_1_04_a is net_generation by coal 
# Table_1_14_A is net_generation by wind
# Table_1_09_A is net_generation by nuclear


#states = {'State': pd.Series(['Connecticut','Maine','Massachusetts','New Hampshire','Rhode Island','Vermont','New Jersey','New York','Pennsylvania','Illinois','Indiana','Michigan','Ohio','Wisconsin','Iowa','Kansas','Minnesota','Missouri','Nebraska','North Dakota','South Dakota','Delaware','District of Columbia','Florida','Georgia','Maryland','North Carolina','South Carolina','Virginia','West Virginia','Alabama','Kentucky','Mississippi','Tennessee','Arkansas','Louisiana','Oklahoma','Texas','Arizona','Colorado','Idaho','Montana','Nevada','New Mexico','Utah','Wyoming','California','Oregon','Washington','Alaska','Hawaii'])}
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

states_series = pd.Series(['Connecticut','Maine','Massachusetts','New Hampshire','Rhode Island','Vermont','New Jersey','New York','Pennsylvania','Illinois','Indiana','Michigan','Ohio','Wisconsin','Iowa','Kansas','Minnesota','Missouri','Nebraska','North Dakota','South Dakota','Delaware','District of Columbia','Florida','Georgia','Maryland','North Carolina','South Carolina','Virginia','West Virginia','Alabama','Kentucky','Mississippi','Tennessee','Arkansas','Louisiana','Oklahoma','Texas','Arizona','Colorado','Idaho','Montana','Nevada','New Mexico','Utah','Wyoming','California','Oregon','Washington','Alaska','Hawaii'])

#states_df = pd.DataFrame(states)

wind_generation_df       = pd.DataFrame()
nuclear_generation_df    = pd.DataFrame()
ng_generation_df         = pd.DataFrame()
petcoke_generation_df    = pd.DataFrame()
biomass_generation_df    = pd.DataFrame()
renewables_generation_df = pd.DataFrame()


def zero_out_undef(dataframe):
    dataframe = (dataframe
                      .drop('NetGen_cur', axis=1)
                      .join(dataframe['NetGen_cur'].apply(pd.to_numeric, errors='coerce')))
    dataframe = dataframe.fillna(0)
    return(dataframe)


def generate_wind_dataframe(wind_generation_df,file,month,year):
    temp_wind_generation_df = pd.read_excel(file, header=None, index_col=False, names=['State','NetGen_cur','NetGen_prior','perc_change','a','b','c','d','e','f','g','h'])
    temp_wind_generation_df = temp_wind_generation_df.drop(['NetGen_prior','perc_change','a','b','c','d','e','f','g','h'], axis=1)
    temp_wind_generation_df['month'] = month
    temp_wind_generation_df['year']  = year
        
    temp_wind_generation_df = temp_wind_generation_df[temp_wind_generation_df['State'].isin(states_series)]
        
    wind_generation_df = wind_generation_df.append(temp_wind_generation_df,ignore_index=True)

    return(wind_generation_df)

def generate_nuclear_dataframe(dataframe, file, month, year):
    temp_dataframe = pd.read_excel(file, header=None, index_col=False, names=['State','NetGen_cur','NetGen_prior','perc_change','a','b','c','d','e','f','g','h'])
    temp_dataframe = temp_dataframe.drop(['NetGen_prior','perc_change','a','b','c','d','e','f','g','h'], axis=1)
    temp_dataframe['month'] = month
    temp_dataframe['year']  = year
        
    temp_dataframe = temp_dataframe[temp_dataframe['State'].isin(states_series)]
        
    dataframe = dataframe.append(temp_dataframe,ignore_index=True)

    return(dataframe)
    
    
def generate_ng_dataframe(dataframe, file, month, year):
    temp_dataframe = pd.read_excel(file, header=None, index_col=False, names=['State','NetGen_cur','NetGen_prior','perc_change','a','b','c','d','e','f','g','h'])
    temp_dataframe = temp_dataframe.drop(['NetGen_prior','perc_change','a','b','c','d','e','f','g','h'], axis=1)
    temp_dataframe['month'] = month
    temp_dataframe['year']  = year
        
    temp_dataframe = temp_dataframe[temp_dataframe['State'].isin(states_series)]
        
    dataframe = dataframe.append(temp_dataframe,ignore_index=True)

    return(dataframe)

def generate_dataframe(dataframe, file, month, year):
    temp_dataframe = pd.read_excel(file, header=None, index_col=False, names=['State','NetGen_cur','NetGen_prior','perc_change','a','b','c','d','e','f','g','h'])
    temp_dataframe = temp_dataframe.drop(['NetGen_prior','perc_change','a','b','c','d','e','f','g','h'], axis=1)
    #temp_dataframe['month'] = month
    #temp_dataframe['year']  = year
    temp_dataframe['date']  = month + ' 1, ' + str(year)
        
    temp_dataframe = temp_dataframe[temp_dataframe['State'].isin(states_series)]
        
    dataframe = dataframe.append(temp_dataframe,ignore_index=True)

    return(dataframe)


def plotStates(dataframe,max_y):
    # begin the plot
    fig = plt.figure(figsize=(20,20))
    xrow = 1
    yrow = 1
    plotnum = 0

    for state in states_series:
        #print("State: " + state)

        dfquery = "State == '" +state + "'"
        #print(dfquery)
        df = dataframe.query(dfquery).groupby(['date'], as_index=False)['NetGen_cur'].mean()
        x1 = df['date']
        y1 = df['NetGen_cur']

        df
        #print(x1)
        #print(y1)
        
        if ( xrow >= 3 ):
            xrow = 1
            yrow +=1
        plotnum +=1

        fig.add_subplot(9,6,plotnum)

        # Plot actual data
        plt.plot_date(x=x1, y=y1, fmt='o-')

#        x2 = mdates.date2num(x1)
#
#        z=np.polyfit(x2,y1,1)
#        p=np.poly1d(z)

#        plt.plot(x1,p(x2),'r--') #add trendline to plot


        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                    wspace=0.35)
        axes = plt.gca()

        axes.set_ylim([0,max_y])

        plt.title(state + ' Generated')
        plt.ylabel('Generated Power')
        plt.xlabel('Date')

        xrow +=1


    fig = plt.gcf()
    plt.show()
    

for year in range(2011, 2017):
    for month in months:
        print("month-year: %s%d" % (month,year))
        #if year < 2013:
        #    filebase = 'epmxlfile'
        #    coal_filename = filebase + '1_4.xls'
        #else:
        if year < 2013:
            continue
        
        
        filebase = 'Table_'
        coal_filename       = filebase + '1_04_A.xls'
        petcoke_filename    = filebase + '1_06_A.xlsx'
        ng_filename         = filebase + '1_07_A.xlsx'
        wind_filename       = filebase + '1_14_A.xlsx'
        nuclear_filename    = filebase + '1_09_A.xlsx'
        biomass_filename    = filebase + '1_15_A.xlsx'
        renewables_filename = filebase + '1_11_A.xlsx'

        dirname  = ''
        dirname  += month
        dirname  += str(year)

        
        print(dirname+'/'+wind_filename)
        wind_generation_df       = generate_dataframe(wind_generation_df, dirname+'/'+wind_filename, month, year)
        
        nuclear_generation_df    = generate_dataframe(nuclear_generation_df, dirname+'/'+nuclear_filename, month, year)
        
        ng_generation_df         = generate_dataframe(ng_generation_df, dirname+'/'+ng_filename, month, year)
        
        petcoke_generation_df    = generate_dataframe(petcoke_generation_df, dirname+'/'+petcoke_filename, month, year)
        
        biomass_generation_df    = generate_dataframe(biomass_generation_df, dirname+'/'+biomass_filename, month, year)

        renewables_generation_df = generate_dataframe(renewables_generation_df, dirname+'/'+renewables_filename, month, year)
        
        del filebase,dirname,wind_filename,coal_filename,nuclear_filename,ng_filename,petcoke_filename,biomass_filename,renewables_filename
        
    
del month,months,year
    
#wind_generation_df = (wind_generation_df
#                      .drop('NetGen_cur', axis=1)
#                      .join(wind_generation_df['NetGen_cur'].apply(pd.to_numeric, errors='coerce')))
#wind_generation_df = wind_generation_df.fillna(0)

wind_generation_df        = zero_out_undef(wind_generation_df)
nuclear_generation_df     = zero_out_undef(nuclear_generation_df)
ng_generation_df          = zero_out_undef(ng_generation_df)
petcoke_generation_df     = zero_out_undef(petcoke_generation_df)
biomass_generation_df     = zero_out_undef(biomass_generation_df)
renewables_generation_df  = zero_out_undef(renewables_generation_df)



print("Renewables")
plotStates(renewables_generation_df,renewables_generation_df['NetGen_cur'].max())

print("Nuclear")
plotStates(nuclear_generation_df,nuclear_generation_df['NetGen_cur'].max())

print("PetCoke")
plotStates(petcoke_generation_df,petcoke_generation_df['NetGen_cur'].max())
