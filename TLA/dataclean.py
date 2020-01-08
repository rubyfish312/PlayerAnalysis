#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 09:22:47 2019

@author: nickren
"""

#%%
import pandas as pd
import numpy as np
from pandas import Timestamp

#%%
#輸入betlist
#df_Aug = pd.read_csv('AugDataClean.csv')
#df_Sep = pd.read_csv('SepDataClean.csv')
#df_Oct = pd.read_csv('BFordersOct.csv')

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
#df_treeline = df_treeline_clean(df_tree)
#df_Aug = df_betlist_clean(df_Aug, df_treeline)
#df_Aug = df_betlist_clean(df_Aug, df_treeline)
#df_Aug = df_betlist_clean(df_Aug, df_treeline)


#%%
#betfair & fancy
#%%
#column name調整
def fixColumnName(df):
    
    col_nameA = df.columns.tolist()
    col_nameA = [x.lower() for x in col_nameA]
    col_nameA = [x.replace(' ', '') for x in col_nameA]
    df.columns = col_nameA
    
    return df

#%%
#username調整
def fixName(df):
    
    df['username'].replace(to_replace=pd.Timestamp('2019-01-01 00:00:00'), value='janu1', inplace=True)
    df['username'].replace(to_replace=43466, value='janu1', inplace=True)
    df['username'].replace(to_replace='1-jan', value='janu1', inplace=True)
    df['username'].replace(to_replace=pd.Timestamp('2019-01-02 00:00:00'), value='janu2', inplace=True)
    df['username'].replace(to_replace=43467, value='janu2', inplace=True)
    df['username'].replace(to_replace='2-jan', value='janu2', inplace=True)
    df['username'].replace(to_replace=pd.Timestamp('2019-04-01 00:00:00'), value='apr01', inplace=True)
    df['username'].replace(to_replace=43556, value='apr01', inplace=True)
    df['username'].replace(to_replace='1-apr', value='apr01', inplace=True)
    df['username'] = [str(x) for x in df['username']]
    df['username'] = [x.lower() for x in df['username']] 
    
    return df

#%%
#treeline整理
def treelineClean(df):
    
    df = fixColumnName(df)
    
    df['sa'] = [x.split('-')[0] for x in df['treeline']]
    df['a'] = [x.split('-')[1] for x in df['treeline']]
    df['s'] = [x.split('-')[2] for x in df['treeline']]
    df['m'] = [x.split('-')[3] for x in df['treeline']]
    
    df = fixName(df)
    
    df.index = df.username
    df.drop_duplicates(subset=['username'], keep='first', inplace=True)
    
    return df

#%%
#配對下線
def matchTreeline(df_betlist, df_treeline):
    
    df_treeline = treelineClean(df_treeline)
    
    df_betlist['sa'] = 0
    df_betlist['a'] = 0
    df_betlist['s'] = 0
    df_betlist['m'] = 0

    for i in df_treeline['username']:
        SAname = df_treeline['sa'][i]
        Aname = df_treeline['a'][i]
        Sname = df_treeline['s'][i]
        Mname = df_treeline['m'][i]

        name = np.where(df_betlist['username'] == i)
        df_betlist['sa'].iloc[tuple(name)] = SAname
        df_betlist['a'].iloc[tuple(name)] = Aname
        df_betlist['s'].iloc[tuple(name)] = Sname
        df_betlist['m'].iloc[tuple(name)] = Mname
    
    return df_betlist

#%%
#計算有效流水
def realOrderCredit(df):
    
    df['realordercredit'] = 0
    df['ca_stake'] = 0
    
    for o in range(len(df['ordercredit'])):
        if df['side'][o] == 'LAY':
            df['realordercredit'][o] = df['ordercredit'][o] * (df['orderprice'][o] - 1)
        else:
            df['realordercredit'][o] = df['ordercredit'][o]
    
    df['ca_stake'] = df['realordercredit'] * df['companyadminpt'] / 100
    
    return df

#%%
#betfair、fancy注單整理
def betlistClean(df_betlist, df_treeline):
    # 調整欄標題(轉小寫、去空白)
    df_betlist = fixColumnName(df_betlist)
    
    if ('username' in df_betlist.columns) == False:
        df_betlist['username'] = df_betlist['creator']
    
    df_betlist = fixName(df_betlist)
    
    df_betlist = matchTreeline(df_betlist, df_treeline)
    
    df_betlist['bf_pnl'] = df_betlist['winlosscredit'] * (100 - (df_betlist['companyadminpt'] + df_betlist['superadminpt'] + df_betlist['adminpt'] + df_betlist['superpt'] + df_betlist['masterpt'])) / 100
    df_betlist['ca_pnl'] = df_betlist['winlosscredit'] * df_betlist['companyadminpt'] / 100 * (-1)
    df_betlist['sa_pnl'] = df_betlist['winlosscredit'] * df_betlist['superadminpt'] / 100 * (-1)
    df_betlist['a_pnl'] = df_betlist['winlosscredit'] * df_betlist['adminpt'] / 100 * (-1)
    df_betlist['s_pnl'] = df_betlist['winlosscredit'] * df_betlist['superpt'] / 100 * (-1)
    df_betlist['m_pnl'] = df_betlist['winlosscredit'] * df_betlist['masterpt'] / 100 * (-1)
    
    df_betlist['checkoutat'] = pd.to_datetime(df_betlist['checkoutat'], format='%d/%m/%Y %H:%M:%S')
    df_betlist['checkoutat'] = [Timestamp(i) for i in df_betlist['checkoutat']]

    df_betlist = realOrderCredit(df_betlist)
    #df_bets.drop_duplicates('ordernumber', keep = 'first', inplace = True)
    return df_betlist

#%%
#playtech & BTi
#%%
#資料格式統一
def fixData(df):
    
    df['Account'] = [str(x) for x in (df['Account'])]
    df['Account'] = [x.lower() for x in (df['Account'])]
    
    df['Stake'] = [float(x) for x in (df['Stake'])]
    df['Win/Loss'] = [float(x) for x in (df['Win/Loss'])]
    
    df['Settled Time'] = pd.to_datetime(df['Settled Time'], format='%Y-%m-%d %H:%M:%S')
    df['Settled Time'] = [Timestamp(i) for i in df['Settled Time']]
    df['Placed Time'] = pd.to_datetime(df['Placed Time'], format='%Y-%m-%d %H:%M:%S')
    df['Placed Time'] = [Timestamp(i) for i in df['Placed Time']]
    
    return df

#%%
#匯率轉換
def exchange(df):
    
    exchangeRate = {'BBB-TXD': 1, 'BBB-GBP': 0.12, 'BBB-INR': 12, 'BBB-USD': 0.16, 'BBB-AED': 0.6, 'BBB-HKD': 1.2, 'BBB-HKD14': 1.4, 'BBB-USD14': 0.2, 'BBB-GBP14': 0.14, 'BBB-AED14': 0.7, 'BBB-INR14': 14, 'BBB-SNK5': 2.8, 'BBB-SG14': 0.27, 'BBB-HKD16': 1.6, 'BBB-USD16': 0.22, 'BBB-GBP16': 0.16, 'BBB-AED16': 0.8, 'BBB-INR16': 16, 'BBB-SG16': 0.3, 'BBB-SG12': 0.24}

    df['exchangeRate'] = 0

    for i in exchangeRate:
        eR = exchangeRate[i]
        currency = np.where(df['Agent'] == i)
        df['exchangeRate'].iloc[tuple(currency)] = eR
    
    df['stake_TXD'] = df['Stake'] / df['exchangeRate']
    df['winloss_TXD'] = df['Win/Loss'] / df['exchangeRate']
    
    return df

#%%
#playtech & BTi資料整理
def PTClean(df):
    
    fixData(df)
    exchange(df)
    
    return df
