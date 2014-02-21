import os
import sys

usuario=(sys.argv[1])
subdom=(sys.argv[2])

import MySQLdb
base = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="ftpusers")
cursor = base.cursor()
consulta = "select domain from users where userid='%s';" % (usuario)
cursor.execute(consulta)
resultado = cursor.fetchone()
if resultado == None:
    print "El usuario %s no exite" % (usuario)
else:
    os.system("mkdir /var/www/%s/subdominio" % (usuario))
    os.system("mkdir /var/www/%s/subdominio/%s" % (usuario,subdom))
    os.system("echo Pagina %s en construccion  > /var/www/%s/subdominio/%s/index.html" %(subdom,usuario,subdom))
    virtual=open("modeloapache","r")
    lista=virtual.read()
    virtual.close()
    lista=lista.replace("@pagina@","%s.%s.com" % (subdom,usuario))
    lista=lista.replace("@correo@","%s@gmail.com"% usuario)
    lista=lista.replace("@mio@","%s/subdominio/%s"% (usuario,subdom))
    virtual=open("/etc/apache2/sites-available/%s" % subdom,"w")
    virtual.write(lista)
    virtual.close()
    os.system("a2ensite %s" % resultado)
    os.system("service apache2 restart ")

    directa = open("/var/cache/bind/db.%s" % resultado,"a")
    directa.write("%s  CNAME servidor\n" % subdom)
    directa.close()
    os.system("service bind9 restart ")

