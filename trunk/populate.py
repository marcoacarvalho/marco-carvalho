from macaddress_db import *
Host._connection.debug = True
print "Esse software depende do SQLObject instalado em sua maquina"
instalar = raw_input ("Voce esta pronto para instalar o sistema agora? (sim/nao) :")
if instalar == "sim":
    print "Criando o banco de dados..."
    Host.createTable()
    print "Ok\n"
for line in open("macaddresses.txt").readlines():
    (mac, ip,local,ret) = line.split('|')
    print mac, ip, local, ret
    if local == '':
        local = "OFM"
    Host(HostName = ip, MacAddress = mac, Host_IP = ip, Local = local)
print "seu sistema jah pode ser usado"
