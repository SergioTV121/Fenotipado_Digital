import mysql.connector
from datetime import datetime
import json


datos = open(".\\datos\\da-batC.csv",'w')
datos.write("dFECHAINI\tCELULAR\tdbstart\tdbend\tdFECHAFIN\n")
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM battery_charges")
myresult = mycursor.fetchall()
for reg in myresult:
  fechhoraini = float(reg[1]) / 1000
  fechstrini = datetime.fromtimestamp(fechhoraini)

  fechhorafin = float(reg[5]) / 1000
  fechstrfin = datetime.fromtimestamp(fechhorafin)

  datos.write(str(fechstrini)[0:22]+'\t'+str(reg[2])+'\t'+str(reg[3])+'\t'+str(reg[4])+'\t'+str(fechstrfin)[0:22]+'\n')
datos.close()
mydb.close()
