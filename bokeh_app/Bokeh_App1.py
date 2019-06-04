# -*- coding: utf-8 -*-
"""
Created on Tue May  7 13:27:22 2019

@author: RubyChen
"""

import pandas as pd
import numpy as np
from pandas import Timestamp
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.io import curdoc
from bokeh.models.widgets.inputs import Select, DatePicker, TextInput
from bokeh.models.widgets.buttons import Button
from bokeh.models import LinearAxis 
from bokeh.models.ranges import DataRange1d, Range1d
from bokeh.models import HoverTool
#from bokeh.models import Plot, Title, PanTool, WheelZoomTool
from bokeh.layouts import row, column
from bokeh.models.formatters import DatetimeTickFormatter
from datetime import datetime as dt
from datetime import date

#%%  basic data setting
global df, df_category, df_market, df_target
global category_list, marketid_list, selectionid_list
df = pd.read_csv('BetfairOdds.csv')
df = df.dropna(axis=0,how='any')
df = df.dropna(axis=1,how='any')
df['marketstarttime'] = pd.to_datetime(df['marketstarttime'], format='%Y%m%d-%H:%M:%S')
df['updatedAt'] = pd.to_datetime(df['updatedAt'], format='%Y%m%d-%H:%M:%S')
df['createdAt'] = pd.to_datetime(df['createdAt'], format='%Y%m%d-%H:%M:%S')
df['marketstarttime'] = [Timestamp(i) for i in df['marketstarttime']]
df['updatedAt'] = [Timestamp(i) for i in df['updatedAt']]
df['createdAt'] = [Timestamp(i) for i in df['createdAt']]
df_target = pd.DataFrame(columns=df.columns)
df_category = df.loc[df['eventtypename']=='Cricket']

def initial_list(df):
    category_list = list(df['eventtypename'].unique())
    category_list.sort(key=str.lower)
    marketid_list = list(df['marketid'].unique())
    marketid_list.sort()
    marketid_list = [str(i) for i in marketid_list]
    selectionid_list = list(df['selectionId'].unique())
    selectionid_list.sort()
    selectionid_list = [str(i) for i in selectionid_list]
    category_list.insert(0,'--Select--')
    marketid_list.insert(0,'--Select--')
    selectionid_list.insert(0,'--Select--')
    return category_list, marketid_list, selectionid_list

#df_target=df.loc[df['selectionId']==2954263]
#df_target = df_target.reset_index(drop=True)
#StarttimeHour = df_target['marketstarttime'][0].hour-1
#Starttime = df_target['marketstarttime'][0]
#Starttime = Starttime.replace(hour=StarttimeHour)
#EndtimeHour = df_target['marketstarttime'][0].hour+3
#Endtime = df_target['marketstarttime'][0]
#Endtime = Starttime.replace(hour=EndtimeHour)
#df_target = df_target.loc[(df_target['updatedAt'] >= Starttime) & (df_target['updatedAt'] <= Endtime)]
#%% plot
# select Target data
#x = list(df_target['updatedAt'])
#L_y = list(df_target['layPrice0'])
#L_yy = list(df_target['laySize0'])
x = list(['1900-01-01 00:00:00','1900-01-01 00:00:01'])
L_y = list([1,2])
L_yy = list([1,2])
B_y = list([1,2])
B_yy = list([1,2])
TOOLS = "pan,box_zoom,reset,lasso_select,save,box_select,xzoom_in,crosshair"

data = {'x':x, 'L_y':L_y, 'L_yy':L_yy, 'B_y':B_y, 'B_yy':B_yy}
source = ColumnDataSource(data=data)

pL = figure(
    plot_width=900, 
    plot_height=450, 
    title="Lay Plot",
    tools=TOOLS,
    x_axis_type="datetime",
    x_range = DataRange1d(), 
    y_range = Range1d(1, 1.025*np.max(L_y)),
    )

pB = figure(
    plot_width=900, 
    plot_height=450, 
    title="Back Plot",
    tools=TOOLS,
    x_axis_type="datetime",
    x_range = DataRange1d(), 
    y_range = Range1d(1, 1.025*np.max(B_y)),
    )



pL.extra_y_ranges = {"volume" : DataRange1d(1, 1.025*np.max(L_yy))}
pL.add_layout(LinearAxis(y_range_name="volume"), 'right')
pL.quad(bottom=0, top='L_yy', left='x', right='x', line_width=0.025, line_color="grey",  y_range_name="volume", source=source)
pL.line(x='x', y='L_y', line_color="orange", line_width=2, source=source)
pL.xgrid.grid_line_color = None
#p.vbar(x='xR', top='L_yy', width=0.5,color="grey", y_range_name="volume",source=source)

pB.extra_y_ranges = {"volume" : DataRange1d(1, 1.025*np.max(B_yy))}
pB.add_layout(LinearAxis(y_range_name="volume"), 'right')
pB.quad(bottom=0, top='B_yy', left='x', right='x', line_width=0.025, line_color="grey",  y_range_name="volume", source=source)
pB.line(x='x', y='B_y', line_color="purple", line_width=2, source=source)
pB.xgrid.grid_line_color = None


#hover_tool
hover1 = HoverTool(
    tooltips = [
        ("updatedAt", "@x{%Y-%m-%d %H:%M:%S}"),
        ("layPrice0", "@L_y{0.00}"),
        ("laySize0", "@L_yy{0}"),
        ("backPrice0", "@B_y{0.00}"),
        ("backSize0", "@B_yy{0}"),
    ],
    formatters={
        "x": "datetime",
        "L_y": "numeral",
        "L_yy": "numeral",
        "B_y": "numeral",
        "B_yy": "numeral",
   },
           
)

pL.add_tools(hover1)
pB.add_tools(hover1)

pL.xaxis.formatter=DatetimeTickFormatter(
    minutes = ["%Y-%m-%d %H:%M:%S"],
    hourmin = ["%Y-%m-%d %H:%M:%S"],
    hours=["%Y-%m-%d %H:%M:%S"],
    days=["%Y-%m-%d %H:%M:%S"],
    months=["%Y-%m-%d %H:%M:%S"],
    years=["%Y-%m-%d %H:%M:%S"],
)
            
pB.xaxis.formatter=DatetimeTickFormatter(
    minutes = ["%Y-%m-%d %H:%M:%S"],
    hourmin = ["%Y-%m-%d %H:%M:%S"],
    hours=["%Y-%m-%d %H:%M:%S"],
    days=["%Y-%m-%d %H:%M:%S"],
    months=["%Y-%m-%d %H:%M:%S"],
    years=["%Y-%m-%d %H:%M:%S"],
)


#%% setting callback
# category picker
def nix(val, lst):
    return [x for x in lst if x!=val]

category_list, marketid_list, selectionid_list = initial_list(df)
# select categoryId
ticker_category = Select(title='Category', options=category_list)

def ticker_category_change(attrname, old, new):
    global df, df_category, ticker_market
    category = str(ticker_category.value)
    if category == '--Select--':
        category_list, marketid_list, selectionid_list = initial_list(df)
        ticker_market.options = marketid_list
        ticker_selection.options = selectionid_list
    else:
        df_category = df.loc[df['eventtypename']==category]
        marketid_list = list(df_category['marketid'].unique())
        marketid_list.sort()
        marketid_list = [str(i) for i in marketid_list]
        marketid_list.insert(0,'--Select--')
        ticker_market.options = marketid_list
           
ticker_category.on_change('value', ticker_category_change)

# select marketId
ticker_market = Select(title='Market', options=marketid_list)

def ticker_market_change(attrname, old, new):
    global df, df_category, df_market, ticker_selection
    market = ticker_market.value
    if market == '--Select--':
        category_list, marketid_list, selectionid_list = initial_list(df)
        ticker_selection.options = selectionid_list
    else:
        market = float(market)
        df_market = df_category.loc[df_category['marketid']==market]
        selectionid_list = list(df_market['selectionId'].unique())
        selectionid_list.sort()
        selectionid_list = [str(i) for i in selectionid_list]
        selectionid_list.insert(0,'--Select--')
        ticker_selection.options = selectionid_list
    
ticker_market.on_change('value', ticker_market_change)

# select selectionId
ticker_selection = Select(title='Selection', options=selectionid_list)

def ticker_selection_change(attrname, old, new):
    global df_target, df_market, ticker_selection, selection
    selection = ticker_selection.value
    if selection == '--Select--':
        selectionid_list = list(df_market['selectionId'].unique())
        selectionid_list.sort()
        selectionid_list = [str(i) for i in selectionid_list]
        selectionid_list.insert(0,'--Select--')
        ticker_selection.options = selectionid_list
    else:
        selection = int(selection)
        df_target = df_market.loc[df_market['selectionId']==selection]
        df_target.reset_index(drop=True, inplace=True)
    
ticker_selection.on_change('value', ticker_selection_change)

# datepicker
crnt_date=dt.now()
today = dt.today().date()
 
text_input_strtt = TextInput(value='yyyy-mm-dd hh:mm:ss', title="Start Datetime:")
text_input_endt = TextInput(value='yyyy-mm-dd hh:mm:ss', title="End Datetime:")

# button
button_plot = Button(label="ClickToPlot", button_type="success")

def update():
    global df_target, ticker_selection, selection
    df_target = df_market.loc[df_market['selectionId']==selection]
    df_target.reset_index(drop=True, inplace=True)
    strtt = pd.to_datetime(text_input_strtt.value, format='%Y%m%d %H:%M:%S')
    strtt = Timestamp(strtt)
    endt = pd.to_datetime(text_input_endt.value, format='%Y%m%d %H:%M:%S')
    endt = Timestamp(endt)
    #endt = text_input_endt_change(attr,old,new)
    #print(strtt, endt)   
    df_target = df_target.loc[(df_target['updatedAt'] >= strtt) & (df_target['updatedAt'] <= endt)] 
    #print(strtt, endt)
    x = list(df_target['updatedAt'])
    L_y = list(df_target['layPrice0'])
    L_yy = list(df_target['laySize0'])
    B_y = list(df_target['backPrice0'])
    B_yy = list(df_target['backSize0'])
    newSource = {'x':x, 'L_y':L_y, 'L_yy':L_yy, 'B_y':B_y, 'B_yy':B_yy}
    pL.y_range.reset_end=1.025*np.max(L_y)
    pB.y_range.reset_end=1.025*np.max(B_y)
    source.data = newSource
    
    
button_plot.on_click(update)       


#%% set up layout
widget1 = column(ticker_category, ticker_market, ticker_selection,  
                 #dt_pckr_strt, 
                 text_input_strtt, 
                 #dt_pckr_end, 
                 text_input_endt, 
                 button_plot
                 )
chart = column(pL, pB)
series = row(widget1, chart)
layout = row(series)
#%%
curdoc().add_root(layout)
output_file("Stake.html")
show(layout)
