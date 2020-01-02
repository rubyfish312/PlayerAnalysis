#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:10:20 2019

@author: nickren
"""

import pandas as pd
import numpy as np

#%%
#輸入注單
df_BFbets = pd.read_excel('BFordersNov.xlsx')
#df_Fbets = pd.read_excel('FancyOrdersNov.xlsx')

#%%
df_tree = pd.read_csv('treeline20191205.csv')

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
#注單整理
def betlistClean(df_betlist, df_treeline):
    # 調整欄標題(轉小寫、去空白)
    df_betlist = fixColumnName(df_betlist)
    
    if ('username' in df_betlist.columns) == False:
        df_betlist['username'] = df_betlist['creator']
    
    df_betlist = fixName(df_betlist)
    
    df_betlist = matchTreeline(df_betlist, df_treeline)
    
    df_betlist['bf_pnl'] = df_betlist['winlosscredit'] * df_betlist['betfairpt'] / 100
    df_betlist['ca_pnl'] = df_betlist['winlosscredit'] * df_betlist['companyadminpt'] / 100 * (-1)
    df_betlist['sa_pnl'] = df_betlist['winlosscredit'] * df_betlist['superadminpt'] / 100 * (-1)
    df_betlist['a_pnl'] = df_betlist['winlosscredit'] * df_betlist['adminpt'] / 100 * (-1)
    df_betlist['s_pnl'] = df_betlist['winlosscredit'] * df_betlist['superpt'] / 100 * (-1)
    df_betlist['m_pnl'] = df_betlist['winlosscredit'] * df_betlist['masterpt'] / 100 * (-1)
    
    df_betlist = realOrderCredit(df_betlist)
    #df_bets.drop_duplicates('ordernumber', keep = 'first', inplace = True)
    return df_betlist

#%%
df_BFbets = betlistClean(df_BFbets, df_tree)

#%%
df_BFbets.to_excel('BFbets.xlsx', index = False)

#%%
#手續費
def comm(df):
    
    df_BFmarket = df.pivot_table(index = 'marketid', values = 'bf_pnl', aggfunc = np.sum)
    df_BFplyMarket = df.pivot_table(index = ['username', 'marketid'], values = ['winlosscredit', 'bf_pnl', 'ca_pnl'], aggfunc = np.sum)
    
    BBBComm = df_BFplyMarket.loc[df_BFplyMarket['winlosscredit'] > 0]['winlosscredit'].sum() * 0.02
    bfComm = df_BFmarket.loc[df_BFmarket['bf_pnl'] > 0]['bf_pnl'].sum() * 0.02
    bfCommBBB = df_BFplyMarket.loc[df_BFplyMarket['bf_pnl'] > 0]['bf_pnl'].sum() * 0.02
    caComm = df_BFplyMarket.loc[df_BFplyMarket['ca_pnl'] < 0]['ca_pnl'].sum() * 0.02 * (-1)
    
    commission = {'BBB': BBBComm, 'bf': bfComm, 'bfBBB': bfCommBBB, 'ca': caComm}
    
    return commission

#%%
#統整
def BBBreport(df):
    
    turnover = df['realordercredit'].sum()
    ggr = df['winlosscredit'].sum() * (-1)
    commission = comm(df)['BBB']
    ngr = ggr + commission
    ggrMargin = ggr / turnover
    ngrMargin = ngr / turnover
    
    return {'Turnover': turnover, 'GGR': ggr, 'Commission': commission, 'NGR': ngr, 'GGR margin': ggrMargin, 'NGR margin': ngrMargin}

def CAreport(df):
    
    turnover = df['ca_stake'].sum()
    ggr = df['ca_pnl'].sum()
    commission = comm(df)['ca']
    bfCommissionGain = comm(df)['bfBBB'] - comm(df)['bf']
    ngr = ggr + commission + bfCommissionGain
    ggrMargin = ggr / turnover
    ngrMargin = ngr / turnover
    
    return {'Turnover': turnover, 'GGR': ggr, 'Commission': commission, 'CommissionNetGain(predict)': bfCommissionGain, 'NGR': ngr, 'GGR margin': ggrMargin, 'NGR margin': ngrMargin}

#%%
#活動玩家
def livePlayers(df):
    
    playerList = list(set(df['username']))
    
    return len(playerList)

#%%
#比賽數量
def categoryEvents(df):
    
    cricket = list(set(df.loc[df['categoryid'] == 4]['eventid']))
    football = list(set(df.loc[df['categoryid'] == 1]['eventid']))
    tennis = list(set(df.loc[df['categoryid'] == 2]['eventid']))
    
    events = {'football': football, 'tennis': tennis, 'cricket': cricket}
    
    return events
