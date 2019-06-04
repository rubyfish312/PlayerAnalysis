# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:44:16 2019

@author: RubyChen
"""
import pandas as pd
import numpy as np
from pandas import Timestamp
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, ColumnDataSource
from bokeh.io import curdoc
from bokeh.io import output_file, show
from bokeh.layouts import row, column
from bokeh.models import HoverTool
from bokeh.models.widgets.inputs import DatePicker, MultiSelect, TextInput
from bokeh.models.widgets.sliders import Slider 
from bokeh.models.widgets.buttons import Button
from bokeh.models.ranges import DataRange1d, Range1d
from datetime import datetime as dt
from datetime import date
#import julian

#%%  basic data setting
global df, df_target, user_list
global x, y, source
df = pd.read_csv('betlist_CHECKOUTED.csv')
df = df.loc[df['MatchedAt'].notnull()]
df = df.loc[df['CategoryId'].isin(['Soccer','Cricket','Tennis'])]
df['CreatedAt'] = pd.to_datetime(df['CreatedAt'], format='%d/%m/%Y %H:%M:%S')
df['MatchedAt'] = pd.to_datetime(df['MatchedAt'], format='%d/%m/%Y %H:%M:%S')
df['SettledAt'] = pd.to_datetime(df['SettledAt'], format='%d/%m/%Y %H:%M:%S')
df['CheckoutAt'] = pd.to_datetime(df['CheckoutAt'], format='%d/%m/%Y %H:%M:%S')
df['CancelledAt'] = pd.to_datetime(df['CancelledAt'], format='%d/%m/%Y %H:%M:%S')
df['CreatedAt'] = [Timestamp(i) for i in df['CreatedAt']]
df['MatchedAt'] = [Timestamp(i) for i in df['MatchedAt']]
df['SettledAt'] = [Timestamp(i) for i in df['SettledAt']]
df['CheckoutAt'] = [Timestamp(i) for i in df['CheckoutAt']]
df['CancelledAt'] = [Timestamp(i) for i in df['CancelledAt']]
df_target = pd.DataFrame(columns=df.columns)
user_list = list(df['Username'].unique())
user_list.sort(key=str.lower)

def initial_list(df):
    category_list = list(df['CategoryId'].unique())
    category_list.sort(key=str.lower)
    user_list = list(df['Username'].unique())
    user_list.sort(key=str.lower)
    category_list.insert(0,'--ResetAll--')
    return category_list


#%% set up plots
def initial_figure():
    global x, y, source, df, df_target 
    x = list(['1900-01-01 00:00:00','1900-01-01 00:00:01'])
    y = list([0,0])
    colors = ['red', 'red']
    data = {'MatchedAt':x, 'MatchedCredit':y, 'colors':colors}
    source = ColumnDataSource(data)

initial_figure()          
TOOLS = "pan,box_zoom,reset,lasso_select,save,box_select,zoom_in,zoom_out,crosshair"
p = figure(plot_width=900, 
           plot_height=450,
           tools=TOOLS,
           x_axis_type="datetime",
           x_range = DataRange1d(), 
           y_range = DataRange1d(),#Range1d(1, 1.025*np.max(df['MatchedCredit'])),
          )

p.scatter(x='MatchedAt', y='MatchedCredit', 
          fill_color='colors', fill_alpha=0.6,
          line_color=None,
          source=source
          )

hover1 = HoverTool(
    tooltips = [
        ("MatchedAt", "@x{%Y-%m-%d %H:%M:%S}"),
        ("MatchedCredit", "@y{0.00}"),
        #("laySize0", "@L_yy{0}"),
        #("backPrice0", "@B_y{0.00}"),
        #("backSize0", "@B_yy{0}"),
    ],
    formatters={
        "x": "datetime",
        "y": "numeral",
        #"L_yy": "numeral",
        #"B_y": "numeral",
        #"B_yy": "numeral",
   },
           
)

p.add_tools(hover1)

p.xaxis.formatter=DatetimeTickFormatter(
    minutes = ["%Y-%m-%d %H:%M:%S"],
    hourmin = ["%Y-%m-%d %H:%M:%S"],
    hours=["%Y-%m-%d %H:%M:%S"],
    days=["%Y-%m-%d %H:%M:%S"],
    months=["%Y-%m-%d %H:%M:%S"],
    years=["%Y-%m-%d %H:%M:%S"],
)


#%% set callback
category_list = initial_list(df)
crnt_date=dt.now()
today = dt.today().date()
global category, strt, end, c, username

# select categoryID
ticker_category = MultiSelect(title='Category', value=[''], options=category_list)
category = ticker_category.value

# datepicker
dt_pckr_strt = DatePicker(title='Select start date', value=today, min_date=date(2017,1,1), max_date=date.today())
strt = Timestamp(dt_pckr_strt.value)
dt_pckr_end = DatePicker(title='Select end date', value=today, min_date=date(2017,1,1), max_date=date.today())
end = Timestamp(dt_pckr_end.value)

# credit slider
slider_crdtthrld = Slider(title="MatchedCredit", value=0.0, start=0, end=2000000, step=100)
c = slider_crdtthrld.value

# select userID
text_input_user = TextInput(value='', title='User:')
username = text_input_user.value 
# button
button = Button(label="ClickToChange", button_type="success")
#%% set callback function
def ticker_category_change(attrname, old, new):
    global df, df_target, user_list
    global category, strt, end, c, username
    if ticker_category.value == new:
        category = new
    else:
        category = old
ticker_category.on_change('value', ticker_category_change)
    
def ticker_strt_change(attrname,old,new):
    global df, df_target, user_list
    global category, strt, end, c, username
    ticker_category.on_change('value', ticker_category_change)
    strt = Timestamp(new)
dt_pckr_strt.on_change('value',ticker_strt_change)
    
def ticker_end_change(attrname,old,new):
    global df, df_target, user_list
    global category, strt, end, c, username
    dt_pckr_strt.on_change('value',ticker_strt_change)
    end = Timestamp(new)
dt_pckr_end.on_change('value',ticker_end_change)
    
def slider_credit_change(attrname, old, new):
    global df, df_target, user_list
    global category, strt, end, c, username    
    if slider_crdtthrld.value == new:
        c = new
    else:
        c = old
    #df_target = df_target.loc[df_target['MatchedCredit']>=c]
slider_crdtthrld.on_change('value', slider_credit_change)
   
def text_input_user_change(attrname, old, new):
    global df, df_target, user_list
    global category, strt, end, c, username
    df_target = df[df['CategoryId'].isin(category)]
    df_target = df_target.loc[df_target['MatchedCredit']>=c]
    if text_input_user.value == new:
        username = new
    else:
        username = old
    if username not in user_list:
        df_target = df_target
    if username in user_list:
        df_target = df_target.loc[df_target['Username']==username]        
text_input_user.on_change('value', text_input_user_change)
   
def update():
    global df, df_target
    global category, strt, end, c, username
    if '--ResetAll--' in category:
        df_target = df
    else:
        df_target = df[df['CategoryId'].isin(category)]
    df_target = df_target.loc[(df_target['MatchedAt']>=strt)]
    df_target = df_target.loc[(df_target['MatchedAt']<=end)]
    df_target = df_target.loc[df_target['MatchedCredit']>=c]
    if username not in user_list:
        df_target = df_target
    if username in user_list:
        df_target = df_target.loc[df_target['Username']==username]
    df_target.reset_index(drop=True)
    x = list(df_target['MatchedAt'])
    y = list(df_target['MatchedCredit'])
    #print(df_target)
    colormap = {'Cricket': 'red', 'Soccer': 'blue', 'Tennis': 'green'}
    colors = [colormap[i] for i in df_target['CategoryId']]
    newSource = {'MatchedAt':x, 'MatchedCredit':y, 'colors':colors}
    source.data = newSource
        
button.on_click(update)


#%% set up layout
widgets = column(ticker_category, dt_pckr_strt, dt_pckr_end, slider_crdtthrld, text_input_user, button)
main_row = row(widgets, p)
layout = row(main_row)


#%% initialize
curdoc().add_root(layout)
output_file("select.html")
show(layout)
#show(p)