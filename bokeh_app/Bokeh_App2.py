# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:44:16 2019

@author: RubyChen
"""
import pandas as pd
import numpy as np
import time
from pandas import Timestamp
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, ColumnDataSource
from bokeh.io import curdoc
from bokeh.io import output_file, show
from bokeh.layouts import row, column
from bokeh.models import HoverTool
from bokeh.models.widgets.inputs import DatePicker, MultiSelect, Select
from bokeh.models.widgets.sliders import Slider 
from bokeh.models.widgets.buttons import Button
from bokeh.models.ranges import DataRange1d
from datetime import datetime
from datetime import date
#from bokeh.models.tools import HoverTool


#%%  basic data setting
global df, df_target, category_list, user_list
#global x, y, source
df = pd.read_csv('betlist_CHECKOUTED_Vt111.csv')
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
#df = df[(df.MatchedAt.notnull())]
#xt = [datetime.strftime(i, "%Y-%m-%d %H:%M:%S") for i in df['MatchedAt']]
#time_tuple = [time.strptime(i, '%Y-%m-%d %H:%M:%S') for i in xt]
#time_epoch = [int(time.mktime(i)) for i in time_tuple]
#time_gct = [time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(i)) for i in time_epoch]
df_target = pd.DataFrame(columns=df.columns)

def initial_list(df):
    category_list = list(df['CategoryId'].unique())
    category_list.sort(key=str.lower)
    user_list = list(df['Username'].unique())
    user_list.sort(key=str.lower)
    user_list.insert(0,'--Select--')
    user_list.insert(1,'--All--')
    category_list.insert(0,'--ResetAll--')
    return category_list, user_list


#%% set up plots
#def initial_figure():
#global x, y, source, df, df_target 
x = list(['1900-01-01 00:00:00','1900-01-01 00:00:01'])
y = list([0,0])
colors = ['red', 'red']
time_gct = list(['1900-01-01 00:00:00','1900-01-01 00:00:01'])
side = list(['LAY','BACK'])
price = list([1.00,1.00])
data = {'MatchedAt':x, 'MatchedCredit':y, 'colors':colors, 'gct':time_gct, 'side':side, 'price':price}
source = ColumnDataSource(data)

#initial_figure()          
TOOLS = "pan,box_zoom,reset,lasso_select,save,box_select,zoom_in,zoom_out,crosshair"
p = figure(plot_width=900, 
           plot_height=450,
           tools=TOOLS,
           x_axis_type="datetime",
           x_range = DataRange1d(), 
           y_range = DataRange1d(),
          )

p.scatter(x='MatchedAt', y='MatchedCredit', 
          fill_color='colors', 
          fill_alpha=0.6,
          line_color=None,
          source=source
          )

hover1 = HoverTool(
    tooltips = [
        ("MatchedAt", "@gct"),
        ("MatchedCredit", "$y{0}"),
        ("Side", "@side"),
        ("price", "@price{0.00}")
    ],
    formatters={
        "MatchedAt": "datetime",
        "MatchedCredit": "numeral",
        "Side": "printf",
        "price":"numeral"
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
category_list, user_list = initial_list(df)
crnt_date=datetime.now()
today = datetime.today().date()
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
slider_crdtthrld = Slider(title="MatchedCredit", value=0.0, start=0, end=1.02*np.max(df['MatchedCredit']), step=100)
c = slider_crdtthrld.value

# userlist
ticker_user = Select(title="UserID:", value='--Select--', options=user_list)

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
    strt = Timestamp(new)
dt_pckr_strt.on_change('value',ticker_strt_change)
    
def ticker_end_change(attrname,old,new):
    global df, df_target, user_list
    global category, strt, end, c, username
    end = Timestamp(new)
dt_pckr_end.on_change('value',ticker_end_change)
    
def slider_credit_change(attrname, old, new):
    global df, df_target, user_list
    global category, strt, end, c, username    
    if slider_crdtthrld.value == new:
        c = new
    else:
        c = old
slider_crdtthrld.on_change('value', slider_credit_change)
   
def ticker_user_change(attrname, old, new):
    global df, df_target, user_list
    global category, strt, end, c, username
    if ticker_user.value == new:
        username = new
    else:
        username = old
ticker_user.on_change('value', ticker_user_change)
   
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
    if username == '--All--':
        df_target = df_target
    else:    
        df_target = df_target.loc[df_target['Username']==username]       
    df_target.reset_index(drop=True)
    x = list(df_target['MatchedAt'])
    xt = [datetime.strftime(i, "%Y-%m-%d %H:%M:%S") for i in df_target['MatchedAt']]
    time_tuple = [time.strptime(i, '%Y-%m-%d %H:%M:%S') for i in xt]
    time_epoch = [int(time.mktime(i)) for i in time_tuple]
    time_gct = [time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(i)) for i in time_epoch]
    y = list(df_target['MatchedCredit'])
    side = list(df_target['Side'])
    price = list(df_target['Price'])
    colormap = {'Cricket': 'red', 'Soccer': 'blue', 'Tennis': 'green'}
    colors = [colormap[i] for i in df_target['CategoryId']]
    newSource = {'MatchedAt':x, 'MatchedCredit':y, 'colors':colors, 'gct':time_gct, 'side':side, 'price':price}
    source.data = newSource
button.on_click(update)


#%% set up layout
widgets = column(ticker_category, dt_pckr_strt, dt_pckr_end, slider_crdtthrld, ticker_user, button)
main_row = row(widgets, p)
layout = row(main_row)


#%% initialize
curdoc().add_root(layout)
output_file("select.html")
show(layout)
#show(p)