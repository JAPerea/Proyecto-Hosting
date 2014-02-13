# -*- coding: utf-8 -*- 
import os
import sys
dominio=(sys.argv[1])

#MySQL
import MySQLdb
db = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="ftpd")
tabla = db.cursor()
consulta = "select username from usuarios where dominio='%s';" % (dominio)
tabla.execute(consulta)
resultado = tabla.fetchone()
if resultado == None:
    print "El dominio %s no existe" % (dominio)
else:
    borrarbase=" drop database %s" % (resultado)
    tabla.execute(borrarbase)
    quitarpermisos=" revoke all on *.* from %s@localhost;" % (resultado)
    tabla.execute(quitarpermisos)
    borrarusuario=" drop user %s@localhost" % (resultado)
    tabla.execute(borrarusuario)
    basereload = "FLUSH PRIVILEGES;"
    tabla.execute(basereload)
    db.commit()
