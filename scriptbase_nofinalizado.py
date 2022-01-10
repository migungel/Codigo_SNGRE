#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import xlrd
import psycopg2
import os 
import sys
import pandas as pd
from datetime import datetime
#Abrimos el fichero excel

conexion = psycopg2.connect(host="192.168.40.23", database="logueo", user="root", password="adm1n.2018")
cursor= conexion.cursor()
#file = open("C:/Users/migun/Dropbox/GR/Matriz_de_calificación_de_campamentos_temporales_30-06-2021.xlsx", "w")

#transformar los caracteres especiales a normales
a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
trans = str.maketrans(a,b)

#abrimos el fichero excel
camp = pd.read_excel("MATRIZ CAMPAMENTOS 2021 CONALI - copia - copia.xlsx", sheet_name="Matriz AT 2021 Camp CONALI")
datos = camp.values.tolist()

cursor.execute("select u.id from usuario u")
usuarios = cursor.fetchall()

##########################Christian 0914829296 id 67

us_id=0
#obtener el ID de Christian
for user in usuarios:
	#print(user[0])
	if user[0]==67:
		us_id=user[0]
		#print(user[0])

for row in datos:
	#print(row)
	if (str(row[2])!='nan' and (str(row[2])!="PROVINCIA")): #and (str(row[75]).replace(" ","")!="NOAPTO") and (str(row[75]).replace(" ","")!="NOAPTO "):
		
		#manejar la fecha actual, para fecha_actualizacion
		fechaac = str(datetime.today()).split(" ")[0].split("-")
		fechaacp = "/".join(reversed(fechaac))
		fechaactualizacion=fechaacp

		#manejar la fecha de registro que se encuentra en el excel, en el campo "fecha de inspeccion"
		fecharegistro=fechaactualizacion
		if str(row[11])!='nan':
			#fecharegistro = str(row[11]).replace("\n",";").split(";")[0].split(" ")[0].replace("-","/")
			#fecharegistro = str(row[11]).replace("\n",";").replace(" ",";").replace("-","/").split(";")
			#fecharegistro=datetime.strptime(fecha, '%m/%d/%Y')
			if type(row[11])!=str:
				fechap = str(row[11]).split(" ")[0].split("-")
				fecha = "/".join(reversed(fechap))
				#fecharegistro=datetime.strptime(fecha, '%d/%m/%Y')
				fecharegistro=fecha
			else:
				fechas = str(row[11]).replace("\n",";").replace(" ",";").replace("-","/").split(";")
				if len(fechas)>=2:
					fecharegistro=fechas[len(fechas)-1]
				else:
					fecharegistro=fechas[0]

		fecha_re=datetime.strptime(fecharegistro, '%d/%m/%Y')
		#timestamp = datetime.
		timestamp = datetime.timestamp(fecha_re)
		#fecha1=float(timestamp)
		print("fecha =", fecha_re)
		print("timestamp =", timestamp)

		fechaactualizacion=datetime.strptime(fechaacp, '%d/%m/%Y')
		timestampac = datetime.timestamp(fechaactualizacion)

		altitud=float(row[9])
		if str(row[9])=='nan':
			#altitud = float(row[9])
			altitud = 0

		print("Provincia: " + row[2] + ", canton: " + row[3] + ", parroquia: " + row[4] + " " + str(row[74]).replace(" ",""))

		print(
			"usuario_registro: " + str(us_id) + "\n" +
			"usuario_actualizacion: " + str(us_id) + "\n" +
			"sector: " + str(row[5]) + "\n" 
			"calle_principal: " + str(" ") + "\n" 
			"calle_secundaria: " + str(" ") + "\n" 
			"punto_referencia: " + str(row[6]) + "\n" + #direccion
			#"fecha_registro: " + str(datetime.strptime(fecharegistro, '%m/%d/%Y')) + "\n"  #la del excel 11
			"fecha_registro: " + str(fecha_re) + " " + str(timestamp) + "\n"
			"fecha_actualizacion: " + str(fechaactualizacion) + " " + str(timestampac) + "\n" #actual
			"nombre: " + str(row[10]) + "\n" #nombre de la infraestructura o terreno
			"tipo: " + str(2) + "\n" +
			"tipo_servicio: " + str(row[12]) + "\n"
			"lat: " + str(float(row[7])) + "\n"
			"lng: " + str(row[8]) + "\n"
			"alt: " + str(float(altitud)) + "\n"
			"nombre_representante: " + str(row[14]) + "\n"
			"celular: " + str(row[16]) + "\n"
			"tel_convencional: " + str(row[15]) + "\n"
			"nombre_institucion: " + str(row[13]) + "\n"
			"celular_institucional: " + str(" ") + "\n"
			"telefono_conv_inst " + str(" ") + "\n"
		)

		id_prueba=1

		cursor_insert= conexion.cursor()
		#lineaubi= "INSERT INTO ubicacion (sector) VALUES('"+str(row[5])+"')RETURNING id;"
		lineaubi= "INSERT INTO ubicacion (id, usuario_registro, usuario_actualizacion, sector, calle_principal, calle_secundaria, punto_referencia, fecha_registro, fecha_actualizacion, nombre, tipo, tipo_servicio, lat, lng, alt, nombre_representante, celular, tel_convencional, nombre_institucion, celular_institucional, tel_conv_institucional) VALUES(DEFAULT,'"+str(int(us_id))+"','"+str(int(us_id))+"','"+str(row[5])+"','"+str(" ")+"','"+str(" ")+"','"+str(row[6])+"','"+str(fecha_re)+"','"+str(fechaactualizacion)+"','"+str(row[10])+"','"+str(int(2))+"','"+str(row[12])+"','"+str(float(row[7]))+"','"+str(float(row[8]))+"','"+str(float(altitud))+"','"+str(row[14])+"','"+str(row[16])+"','"+str(row[15])+"','"+str(row[13])+"','"+str(" ")+"','"+str(" ")+"')RETURNING id;"
		#lineaubi= "INSERT INTO ubicacion (id, usuario_registro, usuario_actualizacion, sector, calle_principal, calle_secundaria, punto_referencia, fecha_registro, fecha_actualizacion, nombre, tipo, tipo_servicio, lat, lng, alt, nombre_representante, celular, tel_convencional, nombre_institucion, celular_institucional, tel_conv_institucional) VALUES(DEFAULT,'"+str(int(us_id))+"','"+str(int(us_id))+"','"+str(row[5])+"','"+str(" ")+"','"+str(" ")+"','"+str(row[6])+"','"+str(fecha_re)+"','"+str(fechaactualizacion)+"','"+str(row[10])+"','"+str(int(2))+"','"+str(row[12])+"','"+str(float(row[7]))+"','"+str(float(row[8]))+"','"+str(float(altitud))+"','"+str(row[14])+"','"+str(row[16])+"','"+str(row[15])+"','"+str(row[13])+"','"+str(" ")+"','"+str(" ")+"')"
		#cursor_insert.execute("""insert into ubicacion (usuario_registro, usuario_actualizacion, sector, calle_principal, calle_secundaria, punto_referencia, fecha_registro, fecha_actualizacion, nombre, tipo, tipo_servicio, lat, lng, alt, nombre_representante, celular, tel_convencional, nombre_institucion, celular_institucional, tel_conv_institucional) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(us_id,us_id,str(row[5]),str(" "),str(" "),str(row[6]),fecha_re,fechaactualizacion,str(row[10]),str(int(2)),str(row[12]),str(float(row[7])),str(float(row[8])),str(altitud),str(row[14]),str(row[16]),str(row[15]),str(row[13]),str(" "),str(" ")))
		#cursor_insert.execute(lineaubi)
		#conexion.commit()
		print(lineaubi)




#consultamos las tablas de provincia, canton, parroquia y zona
#cursor.execute("select c.id, c.parroquia, pa.nombre from calificacion c inner join parroquia pa on c.id=pa.id")
cursor.execute("select pa.id, pa.codigo, pa.nombre, pa.area, pa.canton, pa.activo, pa.usuario_registro, pa.fecha_registro, pa.usuario_actualizacion, pa.fecha_actualizacion, pa.codigo_ficha from parroquia pa")
parroquias = cursor.fetchall()
#print(parroquias)

cursor.execute("select pr.id, pr.codigo, pr.nombre, pr.regional, pr.area, pr.zona, pr.activo, pr.usuario_registro, pr.fecha_registro, pr.usuario_actualizacion, pr.fecha_actualizacion from provincia pr")
provincias = cursor.fetchall()
#print(provincias)

cursor.execute("select c.id, c.codigo, c.nombre, c.area, c.provincia, c.zona, c.activo, c.usuario_registro, c.fecha_registro, c.usuario_actualizacion, c.fecha_actualizacion from canton c")
cantones = cursor.fetchall()
#print(cantones)

cursor.execute("select z.id, z.zona, z.region, z.activo, z.usuario_registro, z.fecha_registro, z.usuario_actualizacion, z.fecha_actualizacion from zona z")
regiones = cursor.fetchall()
#print(regiones)


#print(datos[7])
cnt=1
#iterar los datos obtenidos del excel
for row in datos:
	#elimina los campos vacios y los puntos que esten como NO APTOS
	if (str(row[3])!='nan') and (str(row[75]).replace(" ","")!="NOAPTO") and (str(row[75]).replace(" ","")!="NOAPTO "):
		#presentar los datos de provincia, canton y parroquia que seran ingresados
		#print("Provincia: " + row[3] + ", canton: " + row[4] + ", parroquia: " + row[5] + " " + str(row[75]).replace(" ",""))
		#iterar los datos de la tabla provincia
		for prov in provincias:
			#translate para eliminar caracteres especiales
			#upper para poner en mayusculas los nombres, al igual que la base
			#comparar el campo provincia de los datos(row) con los datos de la base(prov)
			if row[3].translate(trans).upper()==prov[2].translate(trans):
				cnt+=1
				#iterar los datos de la tabla canton
				for can in cantones:
					#compara el numero de codigo de la provincia, para obtener los cantones
					if int(prov[1])==int(can[4]):
						#commpara los cantones de la base, con los datos de canton de los datos del excel
						if can[2].replace(" ","").translate(trans)==str(row[4]).replace(" ","").translate(trans).upper():
							#print(can[2])
							for pa in parroquias:
								#compara el codigo de las parroquias, con la de los cantones
								if pa[4]==can[0]:
									#compara las parroquias de la base, con las parroquias del excel
									if pa[2].replace(" ","").translate(trans)==row[5].replace(" ","").translate(trans).upper():
										fecharegistro = str(str(row[12]).split(";")[0].split(" ")[0].replace("-","/"))
										
										#cursor_insert= conexion.cursor()
										#linea= "insert into ubicacion (usuario_registro, usuario_actualizacion, sector, punto_referencia) values('"+str(us_id)+"'+'"+str(row[6])+"','"+str(row[7])+"','')RETURNING marca_id;"
										#cursor_insert.execute(linea)
										#conexion.commit()
						
						#else:
							#print("Crearlo")



