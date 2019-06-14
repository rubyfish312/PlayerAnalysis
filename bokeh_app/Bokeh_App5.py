# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:46:07 2019

@author: RubyChen
"""

import pandas as pd
import numpy as np
import time
from pandas import Timestamp
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.io import curdoc
from bokeh.palettes import Viridis10
from bokeh.plotting import figure, output_file, output_notebook, show, ColumnDataSource 
from bokeh.models import HoverTool
from bokeh.models.widgets import DatePicker, CheckboxGroup
from bokeh.models.widgets.buttons import Button
from bokeh.models.ranges import DataRange1d
from bokeh.layouts import row, column
from datetime import datetime 
from datetime import date



#%%  basic data setting
global df, df_target, df_Top10ROI
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
df['MatchedDate'] = [i.date() for i in df['MatchedAt']]

def ROI(df):
    for i in range(len(df['Side'])):
        if df['Side'].iloc[i] == 'LAY':
            df['ROI'] = df['WinlossCredit']/(df['MatchedCredit']*df['WinlossCredit'])
    else:
        df['ROI'] = df['WinlossCredit']/df['MatchedCredit']

ROI(df)
df_target = pd.DataFrame(columns=df.columns)
Sector_TotalROI = df_target.groupby(by=['Username'], axis=0, group_keys=False)['ROI'].sum()
df_Top10ROI = Sector_TotalROI.sort_values(ascending=False)[0:10]


#%% set up plots
x = list(['1900-01-01','1900-01-02'])
time_gct = list(['1900-01-01','1900-01-02'])
y0, y1, y2, y3, y4, y5, y6, y7, y8, y9 = list([0,1]), list([0,1]), list([0,1]), list([0,1]), list([0,1]), \
                                         list([0,1]), list([0,1]), list([0,1]), list([0,1]), list([0,1])
data = {'x':x, 'L0':y0, 'L1':y1, 'L2':y2,
               'L3':y3, 'L4':y4, 'L5':y5,
               'L6':y6, 'L7':y7, 'L8':y8,
               'L9':y9,
        'gct':time_gct
        }
source = ColumnDataSource(data=data)

#initial_figure()          
TOOLS = "pan,box_zoom,reset,lasso_select,save,box_select,zoom_in,zoom_out,crosshair"
p = figure(plot_width=900, 
           plot_height=450,
           tools=TOOLS,
           x_axis_type="datetime",
           x_range = DataRange1d(), 
           y_range = DataRange1d(),
          )
props = dict(line_width=4, line_alpha=0.7)
L0 = p.line(x='x', y='L0', legend = '1', color=Viridis10[0], source=source, **props)
L1 = p.line(x='x', y='L1', legend = '2', color=Viridis10[1], source=source, **props)
L2 = p.line(x='x', y='L2', legend = '3', color=Viridis10[2], source=source, **props)
L3 = p.line(x='x', y='L3', legend = '4', color=Viridis10[3], source=source, **props)
L4 = p.line(x='x', y='L4', legend = '5', color=Viridis10[4], source=source, **props)
L5 = p.line(x='x', y='L5', legend = '6', color=Viridis10[5], source=source, **props)
L6 = p.line(x='x', y='L6', legend = '7', color=Viridis10[6], source=source, **props)
L7 = p.line(x='x', y='L7', legend = '8', color=Viridis10[7], source=source, **props)
L8 = p.line(x='x', y='L8', legend = '9', color=Viridis10[8], source=source, **props)
L9 = p.line(x='x', y='L9', legend = '10', color=Viridis10[9], source=source, **props)

hover1 = HoverTool(
    tooltips = [
        ("Date", "@gct"),
    ],
    formatters={
        "Date": "datetime",
        "ROI": "numeral",
   },        
)

p.add_tools(hover1)

p.xaxis.formatter=DatetimeTickFormatter(   
    days=["%Y-%m-%d"],
    months=["%Y-%m-%d"],
    years=["%Y-%m-%d"],
)


#%% set callback 
crnt_date=datetime.now()
today = datetime.today().date() 
  
# datepicker
global strt, end
dt_pckr_strt = DatePicker(title='Select start date', value=today, min_date=date(2017,1,1), max_date=date.today())
strt = Timestamp(dt_pckr_strt.value)
dt_pckr_end = DatePicker(title='Select end date', value=today, min_date=date(2017,1,1), max_date=date.today())
end = Timestamp(dt_pckr_end.value)

# cehckbox
active_list = [i for i in range(10)]
T10_list = list(df_Top10ROI.index)
checkbox_group = CheckboxGroup(labels=T10_list, active=active_list)

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

def checkbox_group_change(attrname,old,new):
    L0.visible = 0 in checkbox_group.active
    L1.visible = 1 in checkbox_group.active
    L2.visible = 2 in checkbox_group.active
    L3.visible = 3 in checkbox_group.active
    L4.visible = 4 in checkbox_group.active
    L5.visible = 5 in checkbox_group.active
    L6.visible = 6 in checkbox_group.active
    L7.visible = 7 in checkbox_group.active
    L8.visible = 8 in checkbox_group.active
    L9.visible = 9 in checkbox_group.active
        
checkbox_group.on_change('active', checkbox_group_change)    

def update_df_plot():
    global df, df_target, df_Top10ROI, df_plot
    global strt, end 
    
    df_target = df.loc[(df['MatchedAt']>=strt) & (df['MatchedAt']<=end)]
    Sector_TotalROI = df_target.groupby(by=['Username'], axis=0, group_keys=False)['ROI'].sum()
    df_Top10ROI = Sector_TotalROI.sort_values(ascending=False)[0:10]
    T10_list = list(df_Top10ROI.index)
    checkbox_group.labels = T10_list
    delta = end-strt
    dti = pd.date_range(strt, periods=delta.days+1, freq='D')
    df_plot = pd.DataFrame(columns=T10_list, index=dti.date)
    df_target = df_target.loc[df_target['Username'].isin(T10_list)]
    Sector_UserDailyROI = df_target.groupby(by=['Username', 'MatchedDate'], axis=0, group_keys=False)['ROI'].sum()
    df_target = Sector_UserDailyROI.unstack(level=0)
    df_plot.update(df_target)
    df_plot=df_plot.fillna(0)
    df_plot = df_plot.cumsum(axis = 0)
    x = list(df_plot.index)
    xt = [datetime.strftime(i, "%Y-%m-%d") for i in df_plot.index]
    time_tuple = [time.strptime(i, '%Y-%m-%d') for i in xt]
    time_epoch = [int(time.mktime(i))+86400 for i in time_tuple]
    time_gct = [time.strftime("%Y-%m-%d", time.gmtime(i)) for i in time_epoch]
    y0 = list(df_plot.iloc[:,0])
    y1 = list(df_plot.iloc[:,1])
    y2 = list(df_plot.iloc[:,2])
    y3 = list(df_plot.iloc[:,3])
    y4 = list(df_plot.iloc[:,4])
    y5 = list(df_plot.iloc[:,5])
    y6 = list(df_plot.iloc[:,6])
    y7 = list(df_plot.iloc[:,7])
    y8 = list(df_plot.iloc[:,8])
    y9 = list(df_plot.iloc[:,9])
    p.x_range = DataRange1d(df_plot.index)
    newSource = {'x':x, 'L0':y0, 'L1':y1, 'L2':y2,
                'L3':y3, 'L4':y4, 'L5':y5,
                'L6':y6, 'L7':y7, 'L8':y8,
                'L9':y9,
                'gct':time_gct
                 }
    source.data = newSource
    
button.on_click(update_df_plot)

  
#%% set up layout
widget1 = column(dt_pckr_strt, dt_pckr_end, checkbox_group, button)
chart = row(widget1, p)
#series = row(p)
layout = row(chart)
#%%
curdoc().add_root(layout)
#output_file("Stake.html")
#show(layout)
