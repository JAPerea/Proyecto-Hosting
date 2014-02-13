# -*- coding: utf-8 -*- 
import os
import MySQLdb
import string
import sys
usuario=(sys.argv[1])
dominio=(sys.argv[2])

#MySQL
db = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="ftpd")
tabla = db.cursor()
consulta1 = "select username from usuarios where username='%s';" % (usuario)
tabla.execute(consulta1)
resultado1 = tabla.fetchone()
if resultado1 != None:
    print "Lo sentimos, el usuario %s ya exite" % (usuario)
elif resultado1 == None:
    consulta2 = "select dominio from usuarios where dominio='%s';" % (dominio)
    tabla.execute(consulta2)
    resultado2 = tabla.fetchone()
    if resultado2 != None:
        print "Lo sentimos, el dominio %s ya exite" % (dominio)
    else:
        os.system("pwgen 12 1 > contramysql")
        contrasql=open("contramysql","r")
        docucontra=contrasql.read()
        contrasql.close()
        contrasplit=docucontra.split("\n")
        resultadosql=contrasplit[0]
        print "La contraseña de MySQL para el usuario %s es %s" % (usuario,resultadosql)
        creabase=" create database %s" % (usuario)
        tabla.execute(creabase)
        permisosql= "grant all privileges on %s.* to"% (usuario)+ " %s@localhost"% (usuario)+ " identified by "+"'%s'" % (resultadosql)
        tabla.execute(permisosql)
        basereload = "FLUSH PRIVILEGES;"
       	tabla.execute(basereload)
        db.commit()
#CREAR DNS
        fichero=open("modelodirecta","r")
        fichero2=open("modelodominio","r")
        lista=fichero.read()
        lista2=fichero2.read()
        fichero.close()
        fichero2.close()
        lista2=lista2.replace("@dominio@","%s" % dominio)
        fichero2=open("/etc/bind/named.conf.local","a")
        fichero2.write(lista2)
        fichero2.close()
        lista=lista.replace("@dominio@","%s" % dominio)
        fichero=open("/var/cache/bind/db.%s" % (dominio),"w")
        fichero.write(lista)
        fichero.close()
        os.system("service bind9 restart")
#CARPETAS PERSONALES Y DE APACHE2
        os.system("mkdir /srv/www/%s" % usuario)
        os.system("echo Pagina de %s en construccion > /srv/www/%s/index.html" %(usuario,usuario))
        os.system("mkdir /home/%s" % usuario)
        os.system("chmod -R 777 /home/'%s'" % usuario)
        os.system("chmod -R 777 /srv/www/'%s'" % usuario)
        virtual=open("modeloapache","r")
        lista=virtual.read()
        virtual.close()
        lista=lista.replace("@pagina@","www.%s" % usuario)
        lista=lista.replace("@correo@","%s@gmail.com"% usuario)
        lista=lista.replace("@mio@","%s"% usuario)
        virtual=open("/etc/apache2/sites-available/%s" % usuario,"w")
        virtual.write(lista)
        virtual.close()
        ficherophp= open("modelophp","r")
        lista2=ficherophp.read()
        ficherophp.close()
        lista2=lista2.replace("@pagina@","%s.com" % usuario)
        lista2=lista2.replace("@mio@","%s"% usuario)
        ficherophp=open("/etc/apache2/sites-available/phpmyadmin%s" % usuario,"w")
        ficherophp.write(lista2)
        ficherophp.close()
        os.system("a2ensite phpmyadmin%s" % usuario)
        os.system("a2ensite %s" % usuario)
        os.system("service apache2 restart")
#PROFTPD
        os.system("pwgen 12 1 > contraproftpd")
        contraftp=open("contraproftpd","r")
        docucontra2=contraftp.read()
        contraftp.close()
        contrasplit2=docucontra2.split("\n")
        resultadoftp=contrasplit2[0]
        contadoruid=open("contadoruid","r")
        lectura=contadoruid.read()
        lecturasplit=lectura.split("\n")
        lecturasplit2=int(lecturasplit[0])
        contadoruid.close()
        sumauid=lecturasplit2+1
        sumauid2=str(sumauid)
        contadoruid2=open("contadoruid","w")
        contadoruid2.write(sumauid2)
        contadoruid2.close()
        print "La contraseña de Proftpd para el usuario %s es %s" % (usuario,resultadoftp)
        anadirusua = "insert into usuarios values ('%s', PASSWORD('%s'), '%s', 6000, '/home/%s','/bin/false',1,'%s');" % (usuario,resultadoftp,sumauid,usuario,dominio)
	tabla.execute(anadirusua)
        basereload = "FLUSH PRIVILEGES;"
        tabla.execute(basereload)
        db.commit()
        print "Se ha creado el usuario y el dominio correctamente"
