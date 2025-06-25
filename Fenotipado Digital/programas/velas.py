from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import mplfinance as mpf 
import matplotlib.dates as mpl_dates 

def eda(dataframe): #Analisis exploratorio
    df=dataframe
    print(df.shape) #Dimensiones del dataset
    print(df.info())    #Metadatos del dataset
    
    for column in df.columns:
        print(df[column])

def set_open_close(dataframe):
    open,close=[],[]
    for i in range(dataframe.shape[0]):
        low=dataframe["cbstart"][i]
        high=dataframe["cbend"][i]
        dif=(high-low)/3
        open.append(low+dif)
        close.append(high-dif)
    dataframe["open"]=open
    dataframe["close"]=close

def graficaIndividual(csv):

    batery_levelU=csv.loc[:70,["cFECHAINI","cbstart","cbend"]]
    set_open_close(batery_levelU)
    batery_levelU=batery_levelU.rename(columns={"cFECHAINI":"date","cbstart":"low","cbend":"high"})
    batery_levelU=batery_levelU.loc[:,["date","open","close","low","high"]]
    batery_levelU.index = pd.DatetimeIndex(batery_levelU['date'])
    
    mpf.plot(batery_levelU,type="candle",title="Carga de la bateria",xlabel="Fecha",ylabel="Nivel de carga (%)",
        style="yahoo")

def graficaSolapadas(df_c,df_d):
    import datetime
    batery_levelC=df_c.loc[:60,["cFECHAINI","cbstart","cbend"]]
    set_open_close(batery_levelC)
    batery_levelC=batery_levelC.rename(columns={"cFECHAINI":"date","cbstart":"low","cbend":"high"})
    batery_levelC=batery_levelC.loc[:,["date","open","close","low","high"]]
    batery_levelC.index = pd.DatetimeIndex(batery_levelC['date'])

    batery_levelD=df_d.loc[:60,["cFECHAINI","cbstart","cbend"]]
    set_open_close(batery_levelD)
    batery_levelD=batery_levelD.rename(columns={"cFECHAINI":"date","cbstart":"low","cbend":"high"})
    batery_levelD=batery_levelD.loc[:,["date","open","close","low","high"]]
    batery_levelD.index = pd.DatetimeIndex(batery_levelD['date'])

    fig = mpf.figure(style='charles',figsize=(8,5))
    ax1 = fig.add_subplot(1,1,1)
    #ax2 = fig.add_subplot(1,1,1)
    #ax2.sharex(ax1)
    # ap = [ mpf.make_addplot(batery_levelC,type='candle',ax=ax1)]

    mpf.plot(batery_levelC,type="candle",style="yahoo",ax=ax1)
    mpf.plot(batery_levelD,type="candle",style="yahoo",ax=ax1)
    
    plt.show()


#eda(dataframe)

df_c=pd.read_csv("datos/carga.csv")
df_d=pd.read_csv("datos/descarga.csv")
df_u=pd.read_csv("datos/union.csv")


graficaIndividual(df_c)    #Carga
graficaIndividual(df_d)     #Descarga
graficaIndividual(df_u)    #Ambas
#graficaSolapadas(df_c,df_d)

