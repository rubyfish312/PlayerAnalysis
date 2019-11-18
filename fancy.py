#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 09:22:47 2019

@author: nickren
"""


import pandas as pd
import numpy as np

#%%
#輸入treeline
df_tree = pd.read_excel('treeline20191112.xls', names = ['username', 'treeline', 'currency', 'exchangerate'])
#輸入betlist
df_Aug_betlist = pd.read_csv('AugDataClean.csv')
df_Sep_betlist = pd.read_csv('SepDataClean.csv')
df_Oct_betlist = pd.read_csv('BFordersOct.csv')

#%%
#treeline整理
##分割treeline
df_tree['sa'] = [x.split('-')[0] for x in df_tree['treeline']]
df_tree['a'] = [x.split('-')[1] for x in df_tree['treeline']]
df_tree['s'] = [x.split('-')[2] for x in df_tree['treeline']]
df_tree['m'] = [x.split('-')[3] for x in df_tree['treeline']]
##username調整
df_tree['username'] = [x.lower() for x in (df_tree['username'])] 
df_tree['username'].replace(to_replace=pd.Timestamp('2019-01-01 00:00:00'), value='janu1', inplace=True)
df_tree['username'].replace(to_replace=43466, value='janu1', inplace=True)
df_tree['username'].replace(to_replace='1-jan', value='janu1', inplace=True)
df_tree['username'].replace(to_replace=43467, value='janu2', inplace=True)
df_tree['username'].replace(to_replace='2-jan', value='janu2', inplace=True)
df_tree['username'].replace(to_replace=43556, value='apr01', inplace=True)
df_tree['username'].replace(to_replace='1-apr', value='apr01', inplace=True)
##移除重複username
df_tree.index = df_tree.username
df_tree.drop_duplicates(subset=['username'], keep='first', inplace=True)

#%%
#betlist整理
##8月
###調整欄標題
col_nameA = df_Aug_betlist.columns.tolist()
col_nameA = [x.lower() for x in col_nameA] #轉小寫
col_nameA = [x.replace(' ', '') for x in col_nameA] #去空白
df_Aug_betlist.columns = col_nameA #更新欄位名稱
###username調整
df_Aug_betlist['username'] = [x.lower() for x in (df_Aug_betlist['username'])] #username轉小寫
df_Aug_betlist['username'].replace(to_replace=pd.Timestamp('2019-01-01 00:00:00'), value='janu1', inplace=True)
df_Aug_betlist['username'].replace(to_replace=43466, value='janu1', inplace=True)
df_Aug_betlist['username'].replace(to_replace='1-jan', value='janu1', inplace=True)
df_Aug_betlist['username'].replace(to_replace=43467, value='janu2', inplace=True)
df_Aug_betlist['username'].replace(to_replace='2-jan', value='janu2', inplace=True)
df_Aug_betlist['username'].replace(to_replace=43556, value='apr01', inplace=True)
df_Aug_betlist['username'].replace(to_replace='1-apr', value='apr01', inplace=True)

##9月
###調整欄標題
col_nameS = df_Sep_betlist.columns.tolist()
col_nameS = [x.lower() for x in col_nameS] #轉小寫
col_nameS = [x.replace(' ', '') for x in col_nameS] #去空白
df_Sep_betlist.columns = col_nameS #更新欄位名稱
###username調整
df_Sep_betlist['username'] = [x.lower() for x in (df_Sep_betlist['username'])] #username轉小寫
df_Sep_betlist['username'].replace(to_replace=pd.Timestamp('2019-01-01 00:00:00'), value='janu1', inplace=True)
df_Sep_betlist['username'].replace(to_replace=43466, value='janu1', inplace=True)
df_Sep_betlist['username'].replace(to_replace='1-jan', value='janu1', inplace=True)
df_Sep_betlist['username'].replace(to_replace=43467, value='janu2', inplace=True)
df_Sep_betlist['username'].replace(to_replace='2-jan', value='janu2', inplace=True)
df_Sep_betlist['username'].replace(to_replace=43556, value='apr01', inplace=True)
df_Sep_betlist['username'].replace(to_replace='1-apr', value='apr01', inplace=True)

##10月
###調整欄標題
col_nameO = df_Oct_betlist.columns.tolist()
col_nameO = [x.lower() for x in col_nameO] #轉小寫
col_nameO = [x.replace(' ', '') for x in col_nameO] #去空白
df_Oct_betlist.columns = col_nameO #更新欄位名稱
###username調整
df_Oct_betlist['username'] = [x.lower() for x in (df_Oct_betlist['username'])] #username轉小寫
df_Oct_betlist['username'].replace(to_replace=pd.Timestamp('2019-01-01 00:00:00'), value='janu1', inplace=True)
df_Oct_betlist['username'].replace(to_replace=43466, value='janu1', inplace=True)
df_Oct_betlist['username'].replace(to_replace='1-jan', value='janu1', inplace=True)
df_Oct_betlist['username'].replace(to_replace=43467, value='janu2', inplace=True)
df_Oct_betlist['username'].replace(to_replace='2-jan', value='janu2', inplace=True)
df_Oct_betlist['username'].replace(to_replace=43556, value='apr01', inplace=True)
df_Oct_betlist['username'].replace(to_replace='1-apr', value='apr01', inplace=True)

##移除fancy
df_Aug_betlist = df_Aug_betlist.loc[df_Aug_betlist['categoryid'] < 100]
df_Sep_betlist = df_Sep_betlist.loc[df_Sep_betlist['categoryid'] < 100]
df_Oct_betlist = df_Oct_betlist.loc[df_Oct_betlist['categoryid'] < 100]

##計算P&L
###8月
df_Aug_betlist['ca_pnl'] = df_Aug_betlist['winlosscredit'] * df_Aug_betlist['companyadminpt'] / 100 * (-1)
df_Aug_betlist['sa_pnl'] = df_Aug_betlist['winlosscredit'] * df_Aug_betlist['superadminpt'] / 100 * (-1)
df_Aug_betlist['a_pnl'] = df_Aug_betlist['winlosscredit'] * df_Aug_betlist['adminpt'] / 100 * (-1)
df_Aug_betlist['s_pnl'] = df_Aug_betlist['winlosscredit'] * df_Aug_betlist['superpt'] / 100 * (-1)
df_Aug_betlist['m_pnl'] = df_Aug_betlist['winlosscredit'] * df_Aug_betlist['masterpt'] / 100 * (-1)

###9月
df_Sep_betlist['ca_pnl'] = df_Sep_betlist['winlosscredit'] * df_Sep_betlist['companyadminpt'] / 100 * (-1)
df_Sep_betlist['sa_pnl'] = df_Sep_betlist['winlosscredit'] * df_Sep_betlist['superadminpt'] / 100 * (-1)
df_Sep_betlist['a_pnl'] = df_Sep_betlist['winlosscredit'] * df_Sep_betlist['adminpt'] / 100 * (-1)
df_Sep_betlist['s_pnl'] = df_Sep_betlist['winlosscredit'] * df_Sep_betlist['superpt'] / 100 * (-1)
df_Sep_betlist['m_pnl'] = df_Sep_betlist['winlosscredit'] * df_Sep_betlist['masterpt'] / 100 * (-1)

###10月
df_Oct_betlist['ca_pnl'] = df_Oct_betlist['winlosscredit'] * df_Oct_betlist['companyadminpt'] / 100 * (-1)
df_Oct_betlist['sa_pnl'] = df_Oct_betlist['winlosscredit'] * df_Oct_betlist['superadminpt'] / 100 * (-1)
df_Oct_betlist['a_pnl'] = df_Oct_betlist['winlosscredit'] * df_Oct_betlist['adminpt'] / 100 * (-1)
df_Oct_betlist['s_pnl'] = df_Oct_betlist['winlosscredit'] * df_Oct_betlist['superpt'] / 100 * (-1)
df_Oct_betlist['m_pnl'] = df_Oct_betlist['winlosscredit'] * df_Oct_betlist['masterpt'] / 100 * (-1)

##配對player & super admin & super
df_Aug_betlist['sa'] = 0
df_Sep_betlist['sa'] = 0
df_Oct_betlist['sa'] = 0

df_Aug_betlist['a'] = 0
df_Sep_betlist['a'] = 0
df_Oct_betlist['a'] = 0

df_Aug_betlist['s'] = 0
df_Sep_betlist['s'] = 0
df_Oct_betlist['s'] = 0

df_Aug_betlist['m'] = 0
df_Sep_betlist['m'] = 0
df_Oct_betlist['m'] = 0

for i in df_tree['username']:
    SAname = df_tree['sa'][i]
    Aname = df_tree['a'][i]
    Sname = df_tree['s'][i]
    Mname = df_tree['m'][i]
    
    nameA = np.where(df_Aug_betlist['username'] == i)
    df_Aug_betlist['sa'].iloc[tuple(nameA)] = SAname
    df_Aug_betlist['a'].iloc[tuple(nameA)] = Aname
    df_Aug_betlist['s'].iloc[tuple(nameA)] = Sname
    df_Aug_betlist['m'].iloc[tuple(nameA)] = Mname
    
    nameS = np.where(df_Sep_betlist['username'] == i)
    df_Sep_betlist['sa'].iloc[tuple(nameS)] = SAname
    df_Sep_betlist['a'].iloc[tuple(nameS)] = Aname
    df_Sep_betlist['s'].iloc[tuple(nameS)] = Sname
    df_Sep_betlist['m'].iloc[tuple(nameS)] = Mname
    
    nameO = np.where(df_Oct_betlist['username'] == i)
    df_Oct_betlist['sa'].iloc[tuple(nameO)] = SAname
    df_Oct_betlist['a'].iloc[tuple(nameO)] = Aname
    df_Oct_betlist['s'].iloc[tuple(nameO)] = Sname
    df_Oct_betlist['m'].iloc[tuple(nameO)] = Mname

#%%
#資料整理
dfname = [df_Aug_betlist, df_Sep_betlist, df_Oct_betlist]

for i in dfname:
    ##調整欄標題
    col_name = i.columns.tolist()
    col_name = [x.lower() for x in col_name]
    col_name = [x.replace(' ', '') for x in col_name]
    i.columns = col_name
    ##username調整
    i['username'] = [x.lower() for x in (i['username'])]
    i['username'].replace(to_replace=pd.Timestamp('2019-01-01 00:00:00'), value='janu1', inplace=True)
    i['username'].replace(to_replace=43466, value='janu1', inplace=True)
    i['username'].replace(to_replace='1-jan', value='janu1', inplace=True)
    i['username'].replace(to_replace=43467, value='janu2', inplace=True)
    i['username'].replace(to_replace='2-jan', value='janu2', inplace=True)
    i['username'].replace(to_replace=43556, value='apr01', inplace=True)
    i['username'].replace(to_replace='1-apr', value='apr01', inplace=True)
    ##移除fancy
    i = i.loc[i['categoryid'] < 100]
    ##計算P&L
    i['ca_pnl'] = i['winlosscredit'] * i['companyadminpt'] / 100 * (-1)
    i['sa_pnl'] = i['winlosscredit'] * i['superadminpt'] / 100 * (-1)
    i['a_pnl'] = i['winlosscredit'] * i['adminpt'] / 100 * (-1)
    i['s_pnl'] = i['winlosscredit'] * i['superpt'] / 100 * (-1)
    i['m_pnl'] = i['winlosscredit'] * i['masterpt'] / 100 * (-1)
