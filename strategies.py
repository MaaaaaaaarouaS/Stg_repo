from indicateur import *

def strat_MA(df,p1,p2):
    df = moving_average(df, p1, p2)
    achat,vente,achat_price,vente_price= [],[],[],[]
    for i in range(len(df)):
        if (df['MA' + str(p1)].iloc[i] > df['MA' + str(p2)].iloc[i] and df['MA' + str(p1)].iloc[i - 1] < df['MA' + str(p2)].iloc[i - 1]):
            achat.append(i)
            achat_price.append(df.close.iloc[i])
        elif (df['MA' + str(p1)].iloc[i] < df['MA' + str(p2)].iloc[i] and df['MA' + str(p1)].iloc[i - 1] > df['MA' + str(p2)].iloc[i - 1]):
            vente.append(i)
            vente_price.append(df.close.iloc[i])
    return achat, vente, achat_price, vente_price


def strat_1_CCI(period,df,b):
    df = CCI_index(period,df)
    achat,vente,achat_price,vente_price= [],[],[],[]
    for i in range(len(df)):
        if (df.CCI.iloc[i] < b and df.CCI.iloc[i - 1] > b):
            vente.append(i)
            vente_price.append(df.close.iloc[i])
        elif (df.CCI.iloc[i] > -b and df.CCI.iloc[i - 1] < -b):
            achat.append(i)
            achat_price.append(df.close.iloc[i])
    return achat, vente, achat_price,vente_price

def strat_2_CCI(period,df,b):
    df=CCI_index(period,df)
    achat,vente,achat_price,vente_price= [],[],[],[]
    for i in range(len(df)):
        if (df.CCI.iloc[i] > b and df.CCI.iloc[i - 1] < b):
            achat.append(i)
            achat_price.append(df.close.iloc[i])
        elif (df.CCI.iloc[i] < -b and df.CCI.iloc[i - 1] > -b):
            vente.append(i)
            vente_price.append(df.close.iloc[i])
    return achat,vente,achat_price,vente_price