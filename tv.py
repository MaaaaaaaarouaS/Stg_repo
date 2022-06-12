#https://pypi.org/project/tvdatafeed/
#https://github.com/StreamAlpha/tvdatafeed/blob/binary/tv.ipynb
from tvDatafeed import TvDatafeed,Interval

username = 'Marouasab'
password = 'Maroua.Lat@@99'
tv=TvDatafeed(username=username,password=password,chromedriver_path=None)

#print(tv.get_hist('GLDUSD','FTX',))
#print(tv.get_hist('O87','SGX',))
print(tv.get_hist('GLDUSD','BITTREX',interval=Interval.in_1_minute,n_bars=5000))
print(tv.get_hist('USOUSD','BITTREX',interval=Interval.in_1_minute,n_bars=5000))
print(tv.get_hist('BTCUSDT','BINANCE',interval=Interval.in_1_minute,n_bars=5000))
print(tv.get_hist('ETHUSDT','BINANCE',interval=Interval.in_1_minute,n_bars=5000))
