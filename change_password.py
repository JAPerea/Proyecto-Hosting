# -*- coding: utf-8 -*- 
import os
import sys
usuario=(sys.argv[1])
dominio=(sys.argv[3])

#MySQL
import MySQLdb
db = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="ftpd")
db2 = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="mysql")
tabla = db.cursor()
tabla2 = db2.cursor()
consulta = "select username from usuarios where username='%s';" % (usuario)
tabla.execute(consulta)
resultado = tabla.fetchone()
