from plotly import graph_objs as go
import streamlit as st
import seaborn as sns
from indicateur import *

def plot_close_price(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['close'], name="stock_close"))
    fig.layout.update(title_text='Chart of historical stock price data', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def plot_ma(data,p1,p2,a,v):
    data = moving_average(data, p1, p2)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['datetime'].index, y=data['close'], name="stock_close"))
    fig.add_trace(go.Scatter(x=data['datetime'].index, y=data['MA' + str(p1)], name='MA ('+str(p1)+'p)'))
    fig.add_trace(go.Scatter(x=data['datetime'].index, y=data['MA' + str(p2)], name='MA ('+str(p2)+'p)'))
    fig.add_trace(go.Scatter(x=data.iloc[a].index, y=data.iloc[a]['close'], mode='markers',name='achat',))
    fig.add_trace(go.Scatter(x=data.iloc[v].index, y=data.iloc[v]['close'], mode='markers',name='vente'))
    fig.layout.update(title_text='Buy and sell signals of moving average strategy', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def plot_stream_pnl(dfa,dfv,dfva,data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['datetime'].index, y=dfv['pnl_vente'], name="pnl_vente"))
    fig.add_trace(go.Scatter(x=data['datetime'].index, y=dfa['pnl_achat'], name="pnl_achat"))
    fig.add_trace(go.Scatter(x=data['datetime'].index, y=dfva['pnl_vente_achat'], name="pnl_vente_achat"))
    fig.layout.update(title_text='PnL Achat & Vente', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def plot_fcci_signaux(data,p,a,v):
    data = CCI_index(p, data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['datetime'].index, y=data['close'], name="stock_close"))
    fig.add_trace(go.Scatter(x=data.iloc[a].index, y=data.iloc[a]['close'], mode='markers',name='achat'))
    fig.add_trace(go.Scatter(x=data.iloc[v].index, y=data.iloc[v]['close'], mode='markers',name='vente'))
    fig.layout.update(title_text='Buy and sell signals of the first CCI index strategy', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def plot_scci_signaux(data,p,a,v):
    data = CCI_index(p, data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['datetime'].index, y=data['close'], name="stock_close"))
    fig.add_trace(go.Scatter(x=data.iloc[a].index, y=data.iloc[a]['close'], mode='markers',name='achat'))
    fig.add_trace(go.Scatter(x=data.iloc[v].index, y=data.iloc[v]['close'], mode='markers',name='vente'))
    fig.layout.update(title_text='Buy and sell signals of the second CCI index strategy', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def plot_cci(data,p,b):
    data = CCI_index(p, data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['datetime'], y=data['CCI'], name="CCI"))
    fig.add_trace(go.Scatter(x=data['datetime'], y=[b for i in range(len(data))], name="surachat",line=dict(color='black'),
    mode='lines'))
    fig.add_trace(go.Scatter(x=data['datetime'], y=[-b for i in range(len(data))], name="survente",line=dict(color='black'),
    mode='lines'))
    fig.layout.update(title_text='CCI index chart', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def plot_max_drawdown(data,TRADING_DAYS):
    series=data.close
    Roll_Max = series.rolling(window=TRADING_DAYS, min_periods=1).max()
    Daily_Drawdown = series/Roll_Max - 1.0
    Max_Daily_Drawdown = Daily_Drawdown.rolling(window=TRADING_DAYS, min_periods=1).min()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['datetime'], y=Max_Daily_Drawdown, name="Max_Daily_Drawdown"))
    fig.add_trace(go.Scatter(x=data['datetime'], y=Daily_Drawdown, name="Daily_Drawdown"))
    fig.layout.update(title_text='Drawdowns chart', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def plt_volatility(df,L):
    df = volatility(df, L)
    fig = go.Figure()
    for i in range(len(L)):
        fig.add_trace(go.Scatter(x=df['datetime'].index, y=df['vol' + str(L[i])], name='vol' + str(L[i])))
    fig.add_trace(go.Scatter(x=df['datetime'].index, y=df['close'], name="stock_close"))
    fig.layout.update(title_text='Volatility', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

def plot_corr(df,L):
    df=volatility(df,L)
    corrMatrix = df.corr()
    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            x=corrMatrix.columns,
            y=corrMatrix.index,
            z=np.array(corrMatrix),
            text=corrMatrix.values,
            texttemplate='%{text:.2f}'
        )
    )
    st.plotly_chart(fig)

def plot_sharpe_ratio(data,rf,TRADING_DAYS):
    series = data.close
    daily_series=series.pct_change()
    volatility = daily_series.rolling(window=TRADING_DAYS).std()*np.sqrt(TRADING_DAYS)
    sharpe_ratio = (daily_series.rolling(window=TRADING_DAYS).mean()*TRADING_DAYS - rf) / volatility
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['datetime'], y=sharpe_ratio, name="sharpe_ratio"))
    fig.layout.update(title_text='Sharpe ratio chart', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
