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
if resultado == None:
    print "El usuario %s no exite" % (usuario)
else:
    if "-sql" == sys.argv[2]:
        print "La nueva contraseña para MySQL del usuario %s es %s" % (usuario,dominio)
        consulta2 = "update user set password=PASSWORD('%s') where user='%s';" % (dominio,usuario)
        tabla2.execute(consulta2)
        basereload = "FLUSH PRIVILEGES;"
        tabla2.execute(basereload)
        db2.commit()

    elif "-ftp" == sys.argv[2]:
        print "La nueva contraseña para Proftpd del usuario %s es %s" % (usuario,dominio)
        consulta3 = "update usuarios set password=PASSWORD('%s') where username='%s';" % (dominio,usuario)
        tabla.execute(consulta3)
        basereload = "FLUSH PRIVILEGES;"
        tabla.execute(basereload)
        db.commit()

