# -*- coding: utf-8 -*-
"""
Created on Tue May  7 13:27:22 2019

@author: RubyChen
"""

import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import LinearAxis, Range1d
from bokeh.models import HoverTool
from bokeh.models.formatters import DatetimeTickFormatter

#%%  basic data setting
df = pd.read_csv('1.157356325.csv')
df['marketstarttime'] = pd.to_datetime(df['marketstarttime'], format='%Y%m%d-%H:%M:%S')
StarttimeHour = df['marketstarttime'][0].hour-1
Starttime = df['marketstarttime'][0]
Starttime = Starttime.replace(hour=StarttimeHour)
EndtimeHour = df['marketstarttime'][0].hour+3
Endtime = df['marketstarttime'][0]
Endtime = Starttime.replace(hour=EndtimeHour)
df['updatedAt'] = pd.to_datetime(df['updatedAt'], format='%Y%m%d-%H:%M:%S')
df['createdAt'] = pd.to_datetime(df['createdAt'], format='%Y%m%d-%H:%M:%S')
df['marketstarttime'] = [i.strftime('%Y-%m-%d %H:%M:%S') for i in df['marketstarttime']]
df['updatedAt'] = [i.strftime('%Y-%m-%d %H:%M:%S') for i in df['updatedAt']]
df['createdAt'] = [i.strftime('%Y-%m-%d %H:%M:%S') for i in df['createdAt']]
Starttime = Starttime.strftime('%Y-%m-%d %H:%M:%S')
Endtime = Endtime.strftime('%Y-%m-%d %H:%M:%S')

#%% select Target data
Target = df.loc[(df['selectionId'] == 2954260) & (df['updatedAt'] >= Starttime) & (df['updatedAt'] <= Endtime)]
x = pd.to_datetime(Target['updatedAt'])
y = Target['layPrice0']
yy = Target['laySize0']

#%%
TOOLS = "pan,box_zoom,reset,lasso_select,save,box_select,xzoom_in,crosshair"

#hover_tool

# create a new plot (with a title) using figure
source_data = {'x':x, 'yy':yy, 'y':y}
source = ColumnDataSource(source_data)

                  


p = figure(
    plot_width=1500, 
    plot_height=500, 
    title="My Line Plot",
    tools=TOOLS,
    x_axis_type="datetime",
    y_range=(0,y.max()+1)
    )

line = p.line(x='x', y='y', line_color="orange", line_width=2, source=source)
p.extra_y_ranges = {"volume": Range1d(start=0, end=1.5*np.max(yy))}
p.vbar(x='x', top='yy', width=0.5,color="grey", y_range_name="volume",source=source)
p.add_layout(LinearAxis(y_range_name="volume"), 'right')




hover1 = HoverTool(
    tooltips = [
        ("updatedAt", "@x{%Y-%m-%d %H:%M:%S}"),
        ("layPrice0", "@y{0.00}"),
        ("laySize0", "@yy{0}"),
    ],
    formatters={
        "x": "datetime",
        "y": "numeral",
        "yy": "numeral",       
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

output_file("legend.html", title="legend.py example")

show(p)  # open a browser
