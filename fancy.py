#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 09:22:47 2019

@author: nickren
"""

#%%
import pandas as pd
import numpy as np

#%%
#輸入betlist
df_Aug = pd.read_csv('AugDataClean.csv')
df_Sep = pd.read_csv('SepDataClean.csv')
df_Oct = pd.read_csv('BFordersOct.csv')

#輸入treeline
df_tree = pd.read_excel('treeline20191112.xls', names = ['username', 'treeline', 'currency', 'exchangerate'])


#%%   
def df_treeline_clean(df_tree=''):
    # 分割treeline
    df_tree['sa'] = [x.split('-')[0] for x in df_tree['treeline']]
    df_tree['a'] = [x.split('-')[1] for x in df_tree['treeline']]
    df_tree['s'] = [x.split('-')[2] for x in df_tree['treeline']]
    df_tree['m'] = [x.split('-')[3] for x in df_tree['treeline']]
   
    # username調整
    df_tree['username'] = [x.lower() for x in (df_tree['username'])] 
    df_tree['username'].replace(to_replace=pd.Timestamp('2019-01-01 00:00:00'), value='janu1', inplace=True)
    df_tree['username'].replace(to_replace=43466, value='janu1', inplace=True)
    df_tree['username'].replace(to_replace='1-jan', value='janu1', inplace=True)
    df_tree['username'].replace(to_replace=43467, value='janu2', inplace=True)
    df_tree['username'].replace(to_replace='2-jan', value='janu2', inplace=True)
    df_tree['username'].replace(to_replace=43556, value='apr01', inplace=True)
    df_tree['username'].replace(to_replace='1-apr', value='apr01', inplace=True)
 
    # 移除重複username
    df_tree.index = df_tree.username
    df_tree.drop_duplicates(subset=['username'], keep='first', inplace=True)
    
    return df_tree
    
def df_betlist_clean(df, df_tree):
    # 調整欄標題
    col_nameA = df.columns.tolist()
    col_nameA = [x.lower() for x in col_nameA] # 轉小寫
    col_nameA = [x.replace(' ', '') for x in col_nameA] # 去空白
    df.columns = col_nameA # 更新欄位名稱

    # username調整
    df['username'] = [x.lower() for x in (df['username'])] #username轉小寫
    df['username'].replace(to_replace=pd.Timestamp('2019-01-01 00:00:00'), value='janu1', inplace=True)
    df['username'].replace(to_replace=43466, value='janu1', inplace=True)
    df['username'].replace(to_replace='1-jan', value='janu1', inplace=True)
    df['username'].replace(to_replace=43467, value='janu2', inplace=True)
    df['username'].replace(to_replace='2-jan', value='janu2', inplace=True)
    df['username'].replace(to_replace=43556, value='apr01', inplace=True)
    df['username'].replace(to_replace='1-apr', value='apr01', inplace=True)

    # 移除fancy
    df = df.loc[df['categoryid'] < 100]

    # 計算P&L
    df['ca_pnl'] = df['winlosscredit'] * df['companyadminpt'] / 100 * (-1)
    df['sa_pnl'] = df['winlosscredit'] * df['superadminpt'] / 100 * (-1)
    df['a_pnl'] = df['winlosscredit'] * df['adminpt'] / 100 * (-1)
    df['s_pnl'] = df['winlosscredit'] * df['superpt'] / 100 * (-1)
    df['m_pnl'] = df['winlosscredit'] * df['masterpt'] / 100 * (-1)

    #配對player & super admin & super
    df['sa'] = 0
    df['a'] = 0
    df['s'] = 0
    df['m'] = 0

    for i in df_tree['username']:
        SAname = df_tree['sa'][i]
        Aname = df_tree['a'][i]
        Sname = df_tree['s'][i]
        Mname = df_tree['m'][i]

        name = np.where(df['username'] == i)
        df['sa'].iloc[tuple(name)] = SAname
        df['a'].iloc[tuple(name)] = Aname
        df['s'].iloc[tuple(name)] = Sname
        df['m'].iloc[tuple(name)] = Mname
    
    return df
                
        

#%%
df_treeline = df_treeline_clean(df_tree)
df_Aug = df_betlist_clean(df_Aug, df_treeline)
df_Aug = df_betlist_clean(df_Aug, df_treeline)
df_Aug = df_betlist_clean(df_Aug, df_treeline)

    