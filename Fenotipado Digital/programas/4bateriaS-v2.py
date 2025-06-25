import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.dates import HourLocator, MonthLocator, YearLocator
import numpy as np

pd.options.mode.chained_assignment = None


dispositivo = pd.read_csv('..\\..\\datos\\da-device.csv',sep='\t')
dispositivoseleccionTablaado = dispositivo.loc[:,["CELULAR","buildid","brand","model","sdk"]]
tablaDispositivo = dispositivoseleccionTablaado.drop_duplicates(keep='first') # TOMA DISPOSITIVOS ÚNICOS
tablaDispositivo = tablaDispositivo.set_index('CELULAR')
diccDispositivo = tablaDispositivo.to_dict('index')

idDispositivo = tablaDispositivo["buildid"]
selDispositivo = idDispositivo.drop_duplicates()

    # INTERVALO A GRAFICAR
fechaMinima = datetime.datetime(2023,6,7)  
fechaMaxima = datetime.datetime(2023,7,15)
    
# CARGA
tabla = pd.read_csv('..\\..\\datos\\da-batB.csv',sep='\t')
#unido = pd.merge(tabla, tablaDispositivo, how='inner', left_on='CELULAR', right_on='CELULAR')

# DESCARGA
tablaD = pd.read_csv('..\\..\\datos\\da-batC.csv',sep='\t')
#unido = pd.merge(tablaD, tablaDispositivo, how='inner', left_on='CELULAR', right_on='CELULAR')

numero = 0
for unDispositivo in selDispositivo:
    primero = False
    usarDispositivos = tablaDispositivo[tablaDispositivo["buildid"] == unDispositivo] 
    usarCelulares = list(usarDispositivos.index)
    for unCelular in usarCelulares:
        if primero == False:
            restoTitulo = str(diccDispositivo.get(unCelular)['brand'])+' '+str(diccDispositivo.get(unCelular)['model'])+' SDK:'+str(diccDispositivo.get(unCelular)['sdk'])
            print("\nProcesando: ",unDispositivo,end="")   
            print(" ",restoTitulo)
            primero = True
        print("\tCelular: ",unCelular)
          
    seleccionTablaC = tabla[tabla['CELULAR'].isin(usarCelulares)]
    
    seleccionTablaD = tablaD[tablaD['CELULAR'].isin(usarCelulares)]

# SELECCIÓN DE FECHAS DE CARGA DE CELULAR    
    tdate = []
    fecha = seleccionTablaC["cFECHAINI"]
    for unaFecha in fecha:
        fechadma = str(unaFecha)[0:16]
        tdate.append(fechadma)
    seleccionTablaC['cFECHAINI'] = pd.to_datetime(tdate)
    seleccionTablaC.set_index(['cFECHAINI'])

    tdateF = []
    fechaF = seleccionTablaC["cFECHAFIN"]
    for unaFechaF in fechaF:
        fechadmaF = str(unaFechaF)[0:16]
        tdateF.append(fechadmaF)
    seleccionTablaC['cFECHAFIN'] = pd.to_datetime(tdateF)
    seleccionTablaC["DIFC"] = seleccionTablaC["cbend"] -  seleccionTablaC["cbstart"]

    acotarC = seleccionTablaC[ seleccionTablaC["DIFC"] != 0]
       
    # ELIMINAR TUPLAS DUPLICADAS DE ACOTAR 
    #acotarC.info()
    acotarC = acotarC.drop_duplicates()
    #acotarC.info()

# SELECCIÓN DE FECHAS DE DESCARGA DE CELULAR    
    tdateD = []
    fechaD = seleccionTablaD["dFECHAINI"]
    for unaFechaD in fechaD:
        fechadmaD = str(unaFechaD)[0:16]
        tdateD.append(fechadmaD)
    seleccionTablaD['dFECHAINI'] = pd.to_datetime(tdateD)
    seleccionTablaD.set_index(['dFECHAINI'])

    tdateFD = []
    fechaFD = seleccionTablaD["dFECHAFIN"]
    for unaFechaFD in fechaFD:
        fechadmaFD = str(unaFechaFD)[0:16]
        tdateFD.append(fechadmaFD)
    seleccionTablaD['dFECHAFIN'] = pd.to_datetime(tdateFD)
    seleccionTablaD["DIFD"] = seleccionTablaD["dbend"] -  seleccionTablaD["dbstart"]

    acotarD = seleccionTablaD[ seleccionTablaD["DIFD"] != 0]
       
    # ELIMINAR TUPLAS DUPLICADAS DE ACOTAR 
    #acotarD.info()
    acotarD = acotarD.drop_duplicates()
    #acotarD.info()

    
    from matplotlib.lines import Line2D
    
  
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    #fig, ax = plt.subplots()
    listaFecha = []
    listaValores = []
    for reg in acotarC.itertuples():
        ####print(reg[1],reg[3],reg[5],reg[4])

        listaFecha.append(reg[1])
        listaValores.append(reg[3])
        
        listaFecha.append(reg[5])
        listaValores.append(reg[4])
        
    for reg in acotarD.itertuples():
        ####print(reg[1],reg[3],reg[5],reg[4])

        listaFecha.append(reg[1])
        listaValores.append(reg[3])
        
        listaFecha.append(reg[5])
        listaValores.append(reg[4])
        
    integrado = {'laFecha':listaFecha,'valor':listaValores}
    dfintegrado = pd.DataFrame(integrado)
    dfordenado = dfintegrado.sort_values('laFecha')
      
    
    plt.xticks(rotation=20, ha='center')
    myFmt = mdates.DateFormatter('%a %Y-%m-%d')
    ax.xaxis.set_major_formatter(myFmt)
  
    plt.xlim(xmin=datetime.datetime(fechaMinima.year,fechaMinima.month,fechaMinima.day), xmax=datetime.datetime(fechaMaxima.year,fechaMaxima.month,fechaMaxima.day))
    plt.ylim(bottom=0, top=105)
  
    ax.grid('on', which='minor', axis='x' )
    ax.grid('on', which='major', axis='x' )
    ax.xaxis.set_major_locator(HourLocator(byhour=None, interval=168, tz=None))

    
    
    plt.plot_date(dfordenado['laFecha'], dfordenado['valor'], linestyle='--', color='g')
    plt.title('Batería carga-descarga \n'+restoTitulo, fontweight="bold")
    
    nombre = "celular"+str(numero+1)+"bateria.jpg"
    plt.savefig(nombre)
    plt.show()
    
    numero += 1