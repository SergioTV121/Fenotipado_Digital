import mysql.connector
from datetime import datetime
import json

datos = open("./datos/da-batA.csv",'w')
datos.write("FECHA,CELULAR,bstatus,blevel,bscale,bvoltage,btemperature,badaptor,bhealth,btechnology\n")
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM battery")
myresult = mycursor.fetchall()

for reg in myresult:
    fechhora = float(reg[1]) / 1000
    fechstr = datetime.fromtimestamp(fechhora)
    datos.write(str(fechstr)[0:22]+','+str(reg[2])+','+str(reg[3])+','+str(reg[4])+','+str(reg[5])+','+str(reg[6])+','+str(reg[7])+','+str(reg[8])+','+str(reg[9])+','+str(reg[10])+'\n')

datos.close()
mydb.close()
