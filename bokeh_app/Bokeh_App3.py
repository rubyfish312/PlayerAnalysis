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
from bokeh.models.widgets import Select, DatePicker
from bokeh.models.widgets.buttons import Button
from bokeh.models.ranges import FactorRange, DataRange1d
from bokeh.layouts import row, column
from datetime import datetime 
from datetime import date
from bokeh.transform import factor_cmap


#%%  basic data setting
global df, df_target, category_list, user_lis, side_list, Sector_Category_Side
df = pd.read_csv('betlist_CHECKOUTED_Vt111.csv')
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
x = [(cid, side) for cid in category_list for side in side_list]
Sector_Category_Side = df_target.groupby(by=['CategoryId','Side'], axis=0, group_keys=False)['ROI'].sum()
Sector_Category_Side = pd.DataFrame(Sector_Category_Side)
y = list([0,0,0,0,0,0])
data = {'Category_Side' : x, 'ROI' : y}
palette = ["#94dfff", "#f9c8d3"]
source = ColumnDataSource(data=data)

p_ROI = figure(title="ROI by Category_Side",
               plot_height=300,
               plot_width=900,
               toolbar_location=None, 
               tools="",
               x_range=FactorRange(*x),
               y_range=DataRange1d(),
               )

p_ROI.vbar(x='Category_Side', top='ROI', width=0.9, line_color="white",
       fill_color=factor_cmap('Category_Side', palette=palette, factors=side_list, start=1, end=2), source=source)

p_ROI_label = p_ROI.text(x='Category_Side', y=0, source=source, text='ROI')
p_ROI.x_range.range_padding = 0.1
p_ROI.xaxis.major_label_orientation = 1
p_ROI.xgrid.grid_line_color = None


#%% set callback 
crnt_date=datetime.now()
today = datetime.today().date() 
global strt, end, username
  
# userlist
ticker_user = Select(title="UserID:", value='--Select--', options=user_list)

# datepicker
dt_pckr_strt = DatePicker(title='Select start date', value=today, min_date=date(2017,1,1), max_date=date.today())
strt = Timestamp(dt_pckr_strt.value)
dt_pckr_end = DatePicker(title='Select end date', value=today, min_date=date(2017,1,1), max_date=date.today())
end = Timestamp(dt_pckr_end.value)

# show Top5 winner
#stats = PreText(text='', width=500)

# button
button = Button(label="ClickToChange", button_type="success")


#%% set callback function
def ticker_user_change(attrname, old, new):
    global username
    if ticker_user.value == new:
        username = new
    else:
        username = old
ticker_user.on_change('value', ticker_user_change)

def ticker_strt_change(attrname,old,new):
    global strt
    strt = Timestamp(new)
dt_pckr_strt.on_change('value',ticker_strt_change)
    
def ticker_end_change(attrname,old,new):
    global end
    end = Timestamp(new)
dt_pckr_end.on_change('value',ticker_end_change)

#stats = PreText(text='', width=500)

def update():
    global df, df_target, Sector_Category_Side
    global strt, end, username
    if username == '--Select--':
        df_target = df
    else:    
        df_target = df.loc[df['Username']==username]
    df_target = df_target.loc[(df_target['MatchedAt']>=strt)]
    df_target = df_target.loc[(df_target['MatchedAt']<=end)]    
    Sector_Category_Side = df_target.groupby(by=['CategoryId','Side'], axis=0, group_keys=False)['ROI'].sum()
    Sector_Category_Side = pd.DataFrame(Sector_Category_Side)
    x = [(cid, side) for cid in category_list for side in side_list]
    y = list(round(Sector_Category_Side.ROI, 3))
    newSource = {'Category_Side' : x, 'ROI' : y}
    source.data = newSource
    
    
    
    
button.on_click(update)


#%% set up layout
widget1 = column(ticker_user, dt_pckr_strt, dt_pckr_end, button)
#chart = row(widget1, p_ROI_CS, p_ROI_T10)
chart = row(widget1, p_ROI)
#series = row(p)
layout = row(chart)


#%% initial
curdoc().add_root(layout)
#output_file('MatchedCredit_Sector')
#show(layout)

