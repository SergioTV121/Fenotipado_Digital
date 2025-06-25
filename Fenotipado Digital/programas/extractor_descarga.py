import mysql.connector
from datetime import datetime
import json


#mydb = mysql.connector.connect(user='administra', 
#        password='U5u4r1o', host='148.204.64.161', port='3306', database='sensores3')

mydb = mysql.connector.connect(user='root',password='', host='localhost', port='3306', database='sensores')


datos = open(".\\datos\\descarga.csv",'w')
datos.write("cFECHAINI,CELULAR,cbstart,cbend,cFECHAFIN\n")
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM battery_discharges")
myresult = mycursor.fetchall()
for reg in myresult:
  fechhoraini = float(reg[1]) / 1000
  fechstrini = datetime.fromtimestamp(fechhoraini)

  fechhorafin = float(reg[5]) / 1000
  fechstrfin = datetime.fromtimestamp(fechhorafin)
  if reg[4]<=reg[3]: #Correcion de datos anomalos
    datos.write(str(fechstrini)[0:22]+','+str(reg[2])+','+str(reg[3])+','+str(reg[4])+','+str(fechstrfin)[0:22]+'\n')
  else:
    print("Error en la carga")
datos.close()
mydb.close()
