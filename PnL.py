from frais import *

def prix(t,df):
  return df.loc[t].close

def signal_achat(t,s,df):
  if prix(t,df) in s[2]:
      return 1
  return 0

def signal_vente(t,s,df):
  if prix(t,df) in s[3]:
      return 1
  return 0

def pnl_achat(t,qte,s,df):
  if t==0:
      return(0)
  return(pnl_achat(t-1,qte,s,df) + qte *signal_achat(t,s,df)*(prix(t,df)-prix(t-1,df)))

def pnl_vente(t,qte,s,df):
  if t==0:
      return(0)
  return(pnl_vente(t-1,qte,s,df) + qte *signal_vente(t,s,df)*(prix(t-1,df)-prix(t,df)))

def signal(t,s,df):
  if prix(t,df) in s[2] :
      return 1
  elif prix(t,df) in s[3]:
      return -1
  return 0

def pnl_vente_achat(t,qte,s,df):
  if t==0:
      return(0)
  return(pnl_vente_achat(t-1,qte,s,df) + qte *signal(t,s,df)*(prix(t,df)-prix(t-1,df)))


def frais_retrait(Token, reseau, montant):
    df=df_frais_retrait()
    dk = df[(df['Monnaie/Token'] == Token) & (df['Réseau'] == reseau)]
    retrait_min = dk['Retrait minimum'].iloc[0]
    frais_retrait = dk['Frais de retrait'].iloc[0]
    if montant >= float(retrait_min):
        return float(frais_retrait)
    return -1

def frais_trading(Niveau, Token, MT, BNB):
    df=df_frais_trading()
    l = df[(df['Niveau'] == Niveau)]
    if MT.lower() == 'maker' and BNB == False:
        if Token.upper() == 'USDT':
            return float(l['USDT Maker'].iloc[0])
        else:
            return float(l['BUSD Maker'].iloc[0])
    elif MT.lower() == 'taker' and BNB == False:
        if Token.upper() == 'USDT':
            return float(l['USDT Taker'].iloc[0])
        else:
            return float(l['BUSD Taker'].iloc[0])
    elif MT.lower() == 'maker' and BNB == True:
        if Token.upper() == 'USDT':
            return float(l['USDT Maker BNB 10 % de réduction'].iloc[0])
        else:
            return float(l['BUSD Maker BNB 10 % de réduction'].iloc[0])
    else:
        if Token.upper() == 'USDT':
            return float(l['USDT Taker BNB 10 % de réduction'].iloc[0])
        else:
            return float(l['BUSD Taker BNB 10 % de réduction'].iloc[0])

def pnl_V(t, qte,s,df, Token, reseau, Niveau, MT, BNB, retrait=False):
    F = (frais_trading(Niveau, Token, MT, BNB) / 100) * prix(t,df) * qte
    if retrait == False:
        frais = F
    else:
        if frais_retrait(Token, reseau, prix(t,df) * qte) == -1:
            raise Exception("impossible d'effectuer un retrait")
        else:
            frais = F + frais_retrait(Token, reseau, prix(t,df) * qte)
    return pnl_vente(t, qte,s,df) - frais

def pnl_A(t, qte,s,df,Token, reseau, Niveau, MT, BNB, retrait=False):
    F = (frais_trading(Niveau, Token, MT, BNB) / 100) * prix(t,df) * qte
    if retrait == False:
        frais = F
    else:
        if frais_retrait(Token, reseau, prix(t,df) * qte) == -1:
            raise Exception("impossible d'effectuer un retrait")
        else:
            frais = F + frais_retrait(Token, reseau, prix(t,df) * qte)
    return pnl_achat(t, qte,s,df) - frais

def pnl(t, qte,s,df, Token, reseau, Niveau, MT, BNB, retrait=False):
    F = (frais_trading(Niveau, Token, MT, BNB) / 100) * prix(t,df) * qte
    if retrait == False:
        frais = F
    else:
        if frais_retrait(Token, reseau, prix(t,df) * qte) == -1:
            raise Exception("impossible d'effectuer un retrait")
        else:
            frais = F + frais_retrait(Token, reseau, prix(t,df) * qte)
    return pnl_vente_achat(t, qte,s,df) - frais

def pnl_data(qte,s,df, Token, reseau, Niveau, MT, BNB, retrait=False):
    somme,vente,achat=[],[],[]
    for t in range(len(df)):
        print(t)
        vente.append(pnl_V(t, qte,s,df, Token, reseau, Niveau, MT, BNB, retrait=False))
        achat.append(pnl_A(t, qte,s,df, Token, reseau, Niveau, MT, BNB, retrait=False))
        somme.append(pnl(t, qte,s,df, Token, reseau, Niveau, MT, BNB, retrait=False))
    dfv = pd.DataFrame (vente, columns = ['pnl_vente'])
    dfa= pd.DataFrame (achat, columns = ['pnl_achat'])
    dfva=pd.DataFrame (somme, columns = ['pnl_vente_achat'])
    return dfa,dfv,dfva