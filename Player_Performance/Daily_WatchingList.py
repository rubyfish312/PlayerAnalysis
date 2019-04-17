# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:26:38 2019

@author: RubyChen
"""


import pandas as pd
import numpy as np
from pandas import DataFrame
from datetime import datetime





#%% read .csv 
data = pd.read_csv('betlist_CHECKOUTED.csv')
df = DataFrame(data) 
LastRow = df.shape[0]


#%% calcultate risk
df['Risk'] = np.where(df['Side']=='BACK', df['MatchedCredit'], df['MatchedCredit'].mul(df['Price']-1)) 


#%% permutated player by A-Z
df = df.iloc[df.Username.str.lower().argsort()]
df = df.reset_index(drop=True)
df_ROI = df[['Username','WinlossCredit','Risk']]


#%% filter : pickup 
ROI_effective = (df_ROI.groupby("Username")
                       .agg(['sum','count'])
                       .reset_index()
                       .drop(columns=('WinlossCredit','count'))
                )  
# risk count >2
ROI_effective=ROI_effective.loc[ROI_effective[('Risk','count')] > 2]


#%% calculate ROI
ROI_effective['ROI'] = ROI_effective[('WinlossCredit','sum')].mul(1/ROI_effective[('Risk','sum')])


#%% write to csvFile
ROI_effective.to_csv('C:/Users/rubychen/Documents/dumps/Daily_WatchingList/Player_Performance_'+datetime.now().strftime("%Y%m%d")+'.csv', index=False)


 