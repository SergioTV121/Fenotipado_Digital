import mysql.connector
from datetime import datetime
import json

datos = open(".\\datos\\union.csv",'w')
datos.write("cFECHAINI,CELULAR,cbstart,cbend,cFECHAFIN\n")
mycursor = mydb.cursor()
mycursor.execute("SELECT * from battery_charges UNION SELECT * from battery_discharges order by timestamp")
myresult = mycursor.fetchall()
for reg in myresult:
  fechhoraini = float(reg[1]) / 1000
  fechstrini = datetime.fromtimestamp(fechhoraini)

  fechhorafin = float(reg[5]) / 1000
  fechstrfin = datetime.fromtimestamp(fechhorafin)
  if reg[4]!=reg[3]: #Omitir valores iguales
    datos.write(str(fechstrini)[0:22]+','+str(reg[2])+','+str(reg[3])+','+str(reg[4])+','+str(fechstrfin)[0:22]+'\n')

datos.close()
mydb.close()
