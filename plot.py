import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from indicateur import *

def plot_MA(df,p1,p2,a,v):
    df = moving_average(df, p1, p2)
    plt.figure(figsize=(20,10))
    plt.plot(df['close'], label='price')
    plt.plot(df['MA' + str(p1)], color='red', label='Moving average price ('+str(p1)+'p)')
    plt.plot(df['MA' + str(p2)], color='green', label='Moving average price ('+str(p2)+'p)')
    plt.scatter(df.iloc[a].index, df.iloc[a]['close'], marker='^', s=70, c='g')
    plt.scatter(df.iloc[v].index, df.iloc[v]['close'], marker='v', s=70, c='r')
    plt.xlabel('datetime')
    plt.legend()
    st.pyplot()

def plot_CCI_index(df,a,v,p):
    df = CCI_index(p, df)
    plt.figure(figsize=(20,10))
    plt.subplot(211)
    plt.plot(df['close'], color='skyblue', label='price')
    plt.scatter(df.iloc[a].index, df.iloc[a]['close'], marker='^', s=60, c='g')
    plt.scatter(df.iloc[v].index, df.iloc[v]['close'], marker='v', s=60, c='r')
    plt.legend()
    plt.subplot(212)
    plt.plot(df['CCI'], color='red', label='CCI')
    plt.xlabel('datetime')
    plt.legend()
    plt.axhline(0, linestyle='-', linewidth=0.5, color='black')
    plt.axhline(100, linestyle='--', linewidth=1, color='black')
    plt.axhline(-100, linestyle='--', linewidth=1, color='black')
    st.pyplot()

def plot_volatility(df,L):
    df = volatility(df, L)
    plt.figure(figsize=(20,10))
    for i in range(len(L)):
        plt.plot(df['vol' + str(L[i])], label='vol' + str(L[i]))
    plt.plot(df['close'], color='skyblue', label='price')
    plt.xlabel('datetime')
    plt.legend()
    st.pyplot()

def plot_correlation(df,L):
    df=volatility(df,L)
    corrMatrix = df.corr()
    sns.heatmap(corrMatrix,cmap='BuPu',annot=True)
    st.pyplot()

def plot_pnl(dfa,dfv,dfva):
    plt.figure(figsize=(20,10))
    plt.plot(dfv['pnl_vente'], color='red', label='pnl_vente', alpha=0.9)
    plt.plot(dfa['pnl_achat'], color='green', label='pnl_achat', alpha=0.9)
    plt.plot(dfva['pnl_vente_achat'], color='skyblue', label='pnl_vente_achat', alpha=0.9)
    plt.xlabel('datetime')
    plt.legend()
    st.pyplot()
    
def plot_max_drawdown(series,window):
    Roll_Max = series.rolling(window, min_periods=1).max()
    Daily_Drawdown = series/Roll_Max - 1.0
    Max_Daily_Drawdown = Daily_Drawdown.rolling(window, min_periods=1).min()
    plt.figure(figsize=(15,10))
    plt.subplot(211)
    plt.plot(series,label='price')
    plt.legend()
    plt.subplot(212)
    plt.plot(Max_Daily_Drawdown,color='red',label='Max_Daily_Drawdown')
    plt.plot(Daily_Drawdown,color='orange',label='Daily_Drawdown')
    plt.xlabel('datetime')
    plt.legend()
    st.pyplot()

def plot_sharpe_ratio(df,TRADING_DAYS,rf):
    volatility = df.close.rolling(window=TRADING_DAYS).std()*np.sqrt(TRADING_DAYS)
    sharpe_ratio = (df.close.rolling(window=TRADING_DAYS).mean()*TRADING_DAYS - rf) / volatility
    plt.figure(figsize=(15,10))
    plt.plot(sharpe_ratio,label='sharpe_ratio')
    plt.xlabel('datetime')
    plt.legend()
    st.pyplot()