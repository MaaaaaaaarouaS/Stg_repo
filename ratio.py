import pandas as pd
import numpy as np
def max_drawdown(series):
    returns = series.pct_change().dropna()
    cumulative_returns = (returns+1).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns/peak)-1
    return drawdown.min()*100

def topdd(df,N):
    df['ret'] = df.close/df.close[0]
    df['modMax'] = df.ret.cummax()
    df['modDD'] = 1-df.ret.div(df['modMax'])
    groups = df.groupby(df['modMax'])
    dd = groups['modMax','modDD'].apply(lambda g: g[g['modDD'] == g['modDD'].max()])
    topdd = dd.sort_values('modDD', ascending=False).head(N)
    return topdd

def drawdown_group(df,index_list):
    group_max,dd_date = index_list
    ddGroup = df[df['modMax'] == group_max]
    group_length = len(ddGroup)
    group_dd = ddGroup['modDD'].max()*100
    group_dd_length = len(ddGroup[ddGroup.index <= dd_date])
    group_start = ddGroup[0:1].index[0]
    group_end = ddGroup.tail(1).index[0]
    group_rec = group_length - group_dd_length
    return group_start,group_end,group_max,group_dd,dd_date,group_dd_length,group_rec,group_length

def top_N_dd(df,N):
    dd_col = ('start','end','peak', 'dd %','dd_date','dd_length','dd_rec','tot_length')
    df_dd = pd.DataFrame(columns = dd_col)
    for i in range(1,N):
        index_list = topdd(df,N)[i-1:i].index.tolist()[0]
        start,end,peak,dd,dd_date,dd_length,dd_rec,tot_length = drawdown_group(df,index_list)
        df_dd.loc[i-1] = drawdown_group(df,index_list)
    return df_dd

def sharpe_ratio(series,rf,TRADING_DAYS):
    daily_series=series.pct_change()
    mean = daily_series.mean() * TRADING_DAYS -rf
    sigma = daily_series.std() * np.sqrt(TRADING_DAYS)
    return mean / sigma

def calmar_ratio(series,TRADING_DAYS):
    daily_series=series.pct_change().dropna()
    calmars = (daily_series.mean() * TRADING_DAYS)/abs(max_drawdown(series))
    return calmars