#####################Import packages#################
from data import *
from strategies import *
from PnL import *
import streamlit as st
from stream_plot import *
from ratio import *
####################################################
st.title('Trading Application!')
#####################Load data######################
stocks = ('BTCUSDT', 'ETHUSDT')
#intervals = ('1d','5m','3m','1m','1s')
selected_stock = st.selectbox('Select ticker', stocks)
#selected_interval = st.selectbox('Select Interval', intervals)
#d1 = st.date_input("select date",dt.datetime(2019, 7, 6))
#d2 = st.date_input("select date",dt.datetime(2019, 7, 6))
#def load_data(ticker,interval):
    #data = get_Future_price(ticker, interval, dt.datetime(2020, 1, 1), dt.datetime(2022, 1, 1))
    #return data

#data = load_data(selected_stock,selected_interval)
data=data_spot(selected_stock,'1 May 2021')
st.subheader('Raw data')
st.write(data)

#####################plot close price################
plot_close_price(data)

#####################Moving average##################
st.subheader('Moving average')
p1 = (5,10)
p2=(25,30)
selected_p1 = st.selectbox('Select short terme periode', p1)
selected_p2 = st.selectbox('Select long terme periode', p2)
a,v=strat_MA(data,selected_p1,selected_p2)[0:2]
ma = moving_average(data, selected_p1, selected_p2)
st.write(ma)
plot_ma(data,selected_p1,selected_p2,a,v)
st.set_option('deprecation.showPyplotGlobalUse', False)

#####################CCI Index 1######################
st.subheader('Commodity Channel Index (CCI)')
p = st.slider('Chose period', 0, 100, 14)
b = st.slider('Chose positif terminal', 0, 200, 100)
cci = CCI_index(p,data)
st.write(cci)
plot_cci(data,p,b)
a,v=strat_1_CCI(p,data,b)[0:2]
plot_fcci_signaux(data,p,a,v)

####################CCI_Index_2#######################
a,v=strat_2_CCI(p,data,b)[0:2]
plot_scci_signaux(data,p,a,v)



##################### PnL MA #########################
st.subheader('Profit and Loss')
reseau = ('BNB Smart Chain (BEP20)', 'Ethereum (ERC20)','Aion','Arweave','Acala','Ardor')
selected_reseau = st.selectbox('Select reseau', reseau)
niveau=('VIP 0','VIP 1','VIP 2','VIP 3','VIP 4','VIP 5','VIP 6','VIP 7','VIP 8','VIP 9')
selected_niveau = st.selectbox('Select niveau', niveau)
trading_type=('Maker','Taker')
selected_trading_type = st.selectbox('Select trading type', trading_type)
k = st.slider('Chose moment', 0, len(data), 1)
qte = st.number_input('Insert quantity')
s=strat_MA(data,selected_p1,selected_p2)
pnl_t=pnl(k,qte,s,data, selected_stock, selected_reseau, selected_niveau, selected_trading_type, False, retrait=False)
st.write(pnl_t)
#dfa,dfv,dfva=pnl_data(qte,s,data, selected_stock, selected_reseau,selected_niveau, selected_trading_type, False, retrait=False)
#plot_stream_pnl(dfa,dfv,dfva,data)
#NB: PnL prend du temps pour s'exécuter

##################### Absolute risque ################
st.set_option('deprecation.showPyplotGlobalUse', False)
st.subheader('Absolute risk of the investment portfolio')

##################### Max_Drawdowns ##################
plot_max_drawdown(data,TRADING_DAYS=365)
#st.subheader('Top N drawdowns')
#N = st.slider('Chose N', 0, 100, 10)
#st.write(top_N_dd(data,N+1))
st.write('Max drawdowns is :',max_drawdown(data.close))

##################### Volatility ##################
L = st.multiselect(
     'chose your list of periods',
     [10,25,60,90,120],
     [10, 60])
plt_volatility(data,L)
st.markdown('Correlation Matrix')
plot_corr(data,L)

##################### Relative risque ################
st.subheader('Relative risk of the investment portfolio')
##################### Sharpe ratio ###################
rf = st.number_input('Insert risk free return')
#plot_sharpe_ratio(data,rf,TRADING_DAYS=365)
st.write('Sharpe ratio is :', sharpe_ratio(data.close,rf,TRADING_DAYS=365))
st.write('Calmar ratio is :', calmar_ratio(data.close,TRADING_DAYS=365))
