# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:44:16 2019

@author: RubyChen
"""
import pandas as pd
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, output_file, output_notebook, show, ColumnDataSource
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models.widgets import PreText, Select

#%%  basic data setting
df = pd.read_csv('betlist_CHECKOUTED.csv')
df = df.loc[df['CategoryId'].isin(['Soccer','Cricket','Tennis'])]
userlist = list(pd.unique(df['Username']))
userlist.sort(key=str.lower)


#%%
df['CreatedAt'] = pd.to_datetime(df['CreatedAt'])
df['MatcheAt'] = pd.to_datetime(df['MatchedAt'])
df['SettleAt'] = pd.to_datetime(df['SettledAt'])
df['CheckoutAt'] = pd.to_datetime(df['CheckoutAt'])
df['CancelledAt'] = pd.to_datetime(df['CancelledAt'])
df = pd.DataFrame(df).reset_index(drop=True)


#%%
def nix(val, lst):
    return [x for x in lst if x != val]


#%%
def Username_ticker(df, ticker):
    df = df.loc[df['Username']==ticker]
    return df

global df_ticker1 

df_ini = Username_ticker(df, df.Username.iloc[0])

#%% set up widgets
## statement of chosen options
stats = PreText(text='', width=500)  
ticker1 = Select(title="UserID:", options=nix('--Select--',userlist))



#%% set up plots
data = {'date':df_ini.CreatedAt ,'odds':df_ini.Price}
source = ColumnDataSource(data)
tools = "pan,box_zoom,reset,lasso_select,save,box_select,xzoom_in,crosshair"

ts1 = figure(plot_width=900, plot_height=200, title="UserBet", tools=tools, x_axis_type='datetime')
ts1.circle(x='date', y='odds', line_color="orange", line_width=2, source=source)

ts1.xaxis.formatter=DatetimeTickFormatter(
    minutes = ["%Y-%m-%d %H:%M:%S"],
    hourmin = ["%Y-%m-%d %H:%M:%S"],
    hours=["%Y-%m-%d %H:%M:%S"],
    days=["%Y-%m-%d %H:%M:%S"],
    months=["%Y-%m-%d %H:%M:%S"],
    years=["%Y-%m-%d %H:%M:%S"],
)


#%%
def ticker1_change(attrname, old, new):
    update() 
    #username = str(ticker1.value)
    df_ticker1 = Username_ticker(df, username) 
    newSource = {'date':df_ticker1.CreatedAt, 'odds':df_ticker1.Price}
    source.data = newSource 

def update(selected=None):
    global username
    username= str(ticker1.value)

ticker1.on_change('value', ticker1_change)




#%% set up layout
widgets = column(ticker1)
##main_row = row(corr, widgets)
series = row(ts1)
layout = column(widgets, series)
#
#
#
#%% initialize
update()
curdoc().add_root(layout)
output_file("select.html")
show(layout)
##show(ticker1)