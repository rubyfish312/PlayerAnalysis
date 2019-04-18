# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:26:38 2019

@author: RubyChen
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from datetime import datetime
from decimal import *





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
# risk count > r_criteria
r_criteria = 275
ROI_effective=(ROI_effective.loc[ROI_effective[('Risk','count')] > r_criteria]
                            .reset_index()
                            .drop(columns=('index'))
              )

#%% calculate ROI
ROI_effective['ROI'] = ROI_effective[('WinlossCredit','sum')].mul(1/ROI_effective[('Risk','sum')])


#%% write to csvFile
ROI_effective.to_csv('C:/Users/rubychen/Documents/dumps/Daily_WatchingList/Player_Performance_'+datetime.now().strftime("%Y%m%d")+'.csv', index=False)


#%% plot a visualized chart
#pie chart
fig1, ax1 = plt.subplots(figsize=(9, 6), subplot_kw=dict(aspect="equal"))
recipe = ROI_effective
piechartdata = ROI_effective['Risk','sum']
ingredients = ROI_effective['Username']

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n${:d}".format(pct, absolute)

wedges, texts, autotexts = ax1.pie(piechartdata, autopct=lambda pct: func(pct, piechartdata),
                                  textprops=dict(color="w"))
ax1.legend(wedges, ingredients,
          title="Ingredients",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")
ax1.set_title("Bet Credit Amount")
plt.show()


#donut chart
fig2, ax2 = plt.subplots(figsize=(9, 6), subplot_kw=dict(aspect="equal"))
donutchartdata = ROI_effective['ROI']
donutchartdata = donutchartdata.tolist()

wedges, texts = ax2.pie(piechartdata, wedgeprops=dict(width=0.5), startangle=-40)
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax2.annotate(Decimal(donutchartdata[i]).quantize(Decimal('0.000')), xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)
#
ax2.set_title("Player ROI")
#
plt.show()