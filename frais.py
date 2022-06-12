import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import numpy as np

def net(s):
  return ''.join( x for x in s if x not in '%/')

def position(s1,s2,s3,s4):
    s1,s2,s3,s4 = net(s1),net(s2),net(s3),net(s4)
    t=(s1[:len(s1) // 2], s1[len(s1) // 2:],s2[:len(s2) // 2], s2[len(s2) // 2:],s3[:(len(s3) // 2)+1], s3[(len(s3) // 2)+1:],s4[:(len(s4)// 2)+1], s4[(len(s4) // 2)+1:])
    return list(t)

def df_frais_trading():
    soup = BeautifulSoup(requests.get("https://www.binance.com/fr/fee/futureFee").text, 'html.parser')
    tables=soup.find_all("table")
    body=tables[0].tbody
    cs=["Niveau","Volume d'échanges sur 30j (BUSD)","et/ou","Solde de BNB","USDT Maker/Taker","USDT Maker/Taker BNB 10 % de réduction","BUSD Maker / Taker","BUSD Maker/Taker 10 % de réduction"]
    df = pd.DataFrame(columns=["Niveau","Volume d'échanges sur 30j (BUSD)","et/ou","Solde de BNB","USDT Maker/Taker","USDT Maker/Taker BNB 10 % de réduction","BUSD Maker / Taker","BUSD Maker/Taker 10 % de réduction"]
    )
    for row in body.find_all('tr'):
        columns = row.find_all('td')
        if(columns != []):
            Niveau = columns[0].text.strip()
            Volume_Echanges_30j_BUSD= columns[1].text.strip()
            et_ou = columns[2].text.strip()
            Solde_BNB=columns[3].text.strip()
            USDT_Maker_Taker=columns[4].text.strip()
            USDT_Maker_Taker_BNB=columns[5].text.strip()
            BUSD_Maker_Taker=columns[6].text.strip()
            BUSD_Maker_Taker_BNB=columns[7].text.strip()
            df = df.append({"Niveau": Niveau,"Volume d'échanges sur 30j (BUSD)": Volume_Echanges_30j_BUSD, "et/ou": et_ou, "Solde de BNB": Solde_BNB, "USDT Maker/Taker": USDT_Maker_Taker, "USDT Maker/Taker BNB 10 % de réduction": USDT_Maker_Taker_BNB,"BUSD Maker / Taker":BUSD_Maker_Taker,"BUSD Maker/Taker 10 % de réduction":BUSD_Maker_Taker_BNB}, ignore_index=True)
    for c in cs:
        df[c].replace('', np.nan, inplace=True)
        df.dropna(subset=[c], inplace=True)
    df.Niveau[1]='VIP 0'
    L = []
    for i in df.index:
        L.append(position(df['USDT Maker/Taker'][i], df['USDT Maker/Taker BNB 10 % de réduction'][i],
                          df['BUSD Maker / Taker'][i], df['BUSD Maker/Taker 10 % de réduction'][i]))
    df2 = pd.DataFrame(L, columns=['USDT Maker', 'USDT Taker', 'USDT Maker BNB 10 % de réduction',
                                   'USDT Taker BNB 10 % de réduction', 'BUSD Maker', 'BUSD Taker',
                                   'BUSD Maker BNB 10 % de réduction', 'BUSD Maker BNB 10 % de réduction'])
    df2.loc[len(df2)] = ['NaN' for i in range(8)]
    df2 = df2.shift(periods=1).dropna()
    df2 = pd.concat([df['Niveau'], df2], axis=1)
    return df2

def df_frais_retrait():
    soup = BeautifulSoup(requests.get("https://www.binance.com/fr/fee/cryptoFee").text, 'html.parser')
    soup.find(id='__APP_DATA')
    data = json.loads(soup.find(id='__APP_DATA', type='application/json').text)
    cryptoFee = data['pageData']['redux']['ssrStore']['cryptoFee']
    list = []
    for j in range(len(cryptoFee)):
        for k in range(len(cryptoFee[j]['networkList'])):
            list.append([cryptoFee[j]['networkList'][k]['coin']] + [cryptoFee[j]['networkList'][k]['name']] + [
                cryptoFee[j]['networkList'][k]['withdrawMin']] + [cryptoFee[j]['networkList'][k]['withdrawFee']])
    df = pd.DataFrame(list)
    df.columns = ['Monnaie/Token', 'Réseau', 'Retrait minimum', 'Frais de retrait']
    return df