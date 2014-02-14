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
#PROFTPD
    borrarcolumna="delete from usuarios where dominio='%s';" % (dominio)
    tabla.execute(borrarcolumna)
    basereload = "FLUSH PRIVILEGES;"
    tabla.execute(basereload)
    db.commit()

#CARPETAS PERSONALES Y DE APACHE2
    os.system("rm -r /srv/www/%s" % resultado)
    os.system("rm -r /home/%s" % resultado)
    os.system("a2dissite %s" % resultado)
    os.system("a2dissite phpmyadmin%s" % resultado)
    os.system("rm -r /etc/apache2/sites-available/%s" % resultado)
    os.system("service apache2 restart")
    os.system("rm -r /etc/apache2/sites-available/phpmyadmin%s" % resultado)
    os.system("rm -r /var/cache/bind/db.%s" % dominio)
    os.system("sed '/zone " + '"%s"'% dominio + "/,/};/d' /etc/bind/named.conf.local > temporal")
    os.system("mv temporal /etc/bind/named.conf.local")
    print "El usuario %s con dominio %s se elimino correctamente" % (resultado,dominio)
