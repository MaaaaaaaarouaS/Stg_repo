import numpy as np
def CCI_index(p,df):
    typical_price = (df.high + df.low + df.close) / 3
    SMA = typical_price.rolling(p).mean()
    standard_diviation = typical_price.rolling(p).std()
    df['CCI'] = (typical_price - SMA) / (0.015 * standard_diviation)
    df = df[['datetime','close', 'CCI']].dropna()
    return df

def volatility(df,L):
    for i in range(len(L)):
        df['vol' + str(L[i])] = df['close'].rolling(L[i]).std() * np.sqrt(L[i])
    df = df[['datetime','close'] + ['vol' + str(L[i]) for i in range(len(L))]].dropna()
    return df

def moving_average(df,p1,p2):
    df['MA'+str(p1)] = df['close'].rolling(p1).mean()
    df['MA'+str(p2)] = df['close'].rolling(p2).mean()
    df = df.dropna()
    df = df[['datetime','close', 'MA'+str(p1), 'MA'+str(p2)]]
    return df

