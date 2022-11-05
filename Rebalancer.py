import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def rebalance(m):
    symbols = [ 'galausdt',
                'chrusdt',
                'maticusdt',
                'sandusdt',
                'nearusdt',
                'atomusdt',
                'ltcusdt',
                'solusdt',
                'adausdt',
                'flowusdt'
            ]
    asset={}
    capital=1000
    investment=1000/len(symbols)
    portfolio={}
    portfolio_market={}
    for smb in symbols:
        _filename = '_market_data_csv/'+smb+'_1d'
        d = pd.read_parquet(_filename+'.gzip')
        length=len(d)
        asset[smb]=d
        portfolio[smb]=investment/d['close'].iloc[0]
        portfolio_market[smb] = portfolio[smb]
    new_row = { 'time':[asset[symbols[0]]['time'].iloc[0]], 'market':[1000], 'bot':[1000] }
    marketdata=pd.DataFrame(new_row)

    for i in range(0,length-50,m):
        sum=0
        sum2=0
        for smb in symbols:
            sum=(portfolio[smb]*(asset[smb]['close'].iloc[i]))+sum
            sum2=sum2+portfolio_market[smb]*(asset[smb]['close'].iloc[i])
        fund_per_asset=sum/len(symbols)
        for smb in symbols:
            if (portfolio[smb]*asset[smb]['close'].iloc[i])>fund_per_asset:
                to_usdt=portfolio[smb]-(fund_per_asset/asset[smb]['close'].iloc[i])
                portfolio[smb]=(fund_per_asset/asset[smb]['close'].iloc[i])
            elif (portfolio[smb]*asset[smb]['close'].iloc[i])<fund_per_asset:
                to_buy_asset=(fund_per_asset/asset[smb]['close'].iloc[i])-portfolio[smb]
                portfolio[smb]=(fund_per_asset/asset[smb]['close'].iloc[i])
        new_row = { 'time':[asset[smb]['time'].iloc[i]], 'market':[sum2], 'bot':[sum] }
        d2=pd.DataFrame(new_row, index=[len(marketdata)])
        marketdata = pd.concat([marketdata, d2], ignore_index = True)
        marketdata.reset_index()

    y_market=[]
    y_bot=[]
    for i in range(len(marketdata)):
        y_market.append(marketdata['market'].iloc[i])
        y_bot.append(marketdata['bot'].iloc[i])
    gain=((y_bot[-1]-y_market[-1])/y_market[-1])*100
    print("Rebalancing gain vs market gain : ",gain,"%")
    return gain
    y_market=np.array(y_market)
    y_bot=np.array(y_bot)
    plt.title("Market-Bot Performance Data")
    plt.xlabel("TimeStamp")
    plt.ylabel("Account Balance")
    plt.plot(y_market)
    plt.plot(y_bot)
    plt.legend(["MARKET", "BOT"], loc="upper right")
    plt.grid()
    #plt.show()

Gains=[]
Period=[]
for j in range(1,90,1):
    g=rebalance(j)
    Gains.append(g)
    Period.append(j)
    plt.title("Rebalancing_Period vs Profit_Gains")
    plt.xlabel("Period")
    plt.ylabel("Profit gain")
    plt.plot(Period,Gains)
    plt.grid()
print("Profit gain is maximum at rebalancing period of ",Period[Gains.index(max(Gains))])
plt.show()