# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 15:33:14 2019

@author: RubyChen
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:58:15 2019

@author: RubyChen
"""
import pandas as pd
import numpy as np
from pandas import Timestamp
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, output_notebook, show, ColumnDataSource 
from bokeh.models.widgets import DatePicker
from bokeh.models.widgets.buttons import Button
from bokeh.models.ranges import FactorRange, DataRange1d
from bokeh.layouts import row, column
from datetime import datetime 
from datetime import date



#%%  basic data setting
global df, df_target, category_list, user_lis, side_list, Sector_Category_Side
df = pd.read_csv('betlist_CHECKOUTED.csv')
df = df.loc[df['MatchedAt'].notnull()]
df = df.loc[df['MatchedCredit']!=0]
df = df.loc[(df['CategoryId']=='Cricket')|(df['CategoryId']=='Tennis')|(df['CategoryId']=='Soccer')]
df.reset_index(drop=True)    
df['CreatedAt'] = pd.to_datetime(df['CreatedAt'], format='%d/%m/%Y %H:%M:%S')
df['MatchedAt'] = pd.to_datetime(df['MatchedAt'], format='%d/%m/%Y %H:%M:%S')
df['SettleAt'] = pd.to_datetime(df['SettledAt'], format='%d/%m/%Y %H:%M:%S')
df['CheckoutAt'] = pd.to_datetime(df['CheckoutAt'], format='%d/%m/%Y %H:%M:%S')
df['CancelledAt'] = pd.to_datetime(df['CancelledAt'], format='%d/%m/%Y %H:%M:%S')
df['CreatedAt'] = [Timestamp(i) for i in df['CreatedAt']]
df['MatchedAt'] = [Timestamp(i) for i in df['MatchedAt']]
df['SettledAt'] = [Timestamp(i) for i in df['SettledAt']]
df['CheckoutAt'] = [Timestamp(i) for i in df['CheckoutAt']]
df['CancelledAt'] = [Timestamp(i) for i in df['CancelledAt']]

def initial_list(df):
    user_list = list(df['Username'].unique())
    user_list.sort(key=str.lower)
    category_list = list(df['CategoryId'].unique())
    category_list.sort(key=str.lower) 
    side_list = list(df['Side'].unique())
    side_list.sort(key=str.lower)
    user_list.insert(0,'--Select--')
    return category_list, user_list, side_list

def ROI(df):
    for i in range(len(df['Side'])):
        if df['Side'].iloc[i] == 'LAY':
            df['ROI'] = df['WinlossCredit']/(df['MatchedCredit']*df['WinlossCredit'])
    else:
        df['ROI'] = df['WinlossCredit']/df['MatchedCredit']


#%% plot
ROI(df)
df_target = pd.DataFrame(columns=df.columns)
category_list, user_list, side_list = initial_list(df)    

#plot Category_Side ROI per user and Top10
x = ['a','b','c','d','e','f','g','h','i','j']
y = list(np.zeros(10))
data = {'userID':x, 'ROI_T10':y}
source = ColumnDataSource(data=data)

p_ROI = figure(
            x_range=FactorRange(*x),
            y_range=DataRange1d(),
            plot_height=300, 
            title="Total Top10 ROI ",
            toolbar_location=None, 
            tools="")

p_ROI.vbar(x='userID', top='ROI_T10', width=0.9, source=source)
p_ROI_label = p_ROI.text(x='userID', y=10, source=source, text='ROI_T10')
p_ROI.xgrid.grid_line_color = None



#%% set callback 
crnt_date=datetime.now()
today = datetime.today().date() 
global strt, end
  
# datepicker
dt_pckr_strt = DatePicker(title='Select start date', value=today, min_date=date(2017,1,1), max_date=date.today())
strt = Timestamp(dt_pckr_strt.value)
dt_pckr_end = DatePicker(title='Select end date', value=today, min_date=date(2017,1,1), max_date=date.today())
end = Timestamp(dt_pckr_end.value)

# button
button = Button(label="ClickToChange", button_type="success")


#%% set callback function
def ticker_strt_change(attrname,old,new):
    global strt
    strt = Timestamp(new)
dt_pckr_strt.on_change('value',ticker_strt_change)
    
def ticker_end_change(attrname,old,new):
    global end
    end = Timestamp(new)
dt_pckr_end.on_change('value',ticker_end_change)

def update():
    global df, df_target
    global strt, end 
    
    df_target = df.loc[(df['MatchedAt']>=strt) & (df['MatchedAt']<=end)]
    Sector_TotalROI = df_target.groupby(by=['Username'], axis=0, group_keys=False)['ROI'].sum()
    df_Top10ROI = Sector_TotalROI.sort_values(ascending=False)[0:10]
    x = list(df_Top10ROI.index)
    y = list(round(df_Top10ROI,2))
    print(strt, end)
    p_ROI.x_range.factors = x
    newSource = {'userID':x, 'ROI_T10':y}
    source.data = newSource
    
button.on_click(update)


#%% set up layout
widget1 = column(dt_pckr_strt, dt_pckr_end, button)
chart = row(widget1, p_ROI)
layout = row(chart)


#%% initial
curdoc().add_root(layout)
#output_file('MatchedCredit_Sector')
#show(layout)

