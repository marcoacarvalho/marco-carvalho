#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import os
import pexpect
from sqlobject import *

i_expect = [
                       'assword:',
                       'connecting (yes/no)?',
                       'Host key verification failed.',
                       'Connection refused',
                       'route to host'
                       'from'
                       ]

db_filename = os.path.abspath('data.db')
conn = 'sqlite:' + db_filename #+ "?debug=True"
msg = "| %2s | %-16s | %-12s | %-22s |"
er_id = re.compile('^[0-9]{1,2}$')
er_ip = re.compile('^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$')
er_num = re.compile('^[0-9]{1,2}$')
er_ms = re.compile(".*\n.*time=(?P<ms>.*)")

class entry(SQLObject):
       __connection = conn
       connection = conn
       ip = StringCol()
       user = StringCol()
       passwd = StringCol()
       hostname = StringCol(default=None)
       desc = StringCol(default=None)

def list(id = -1):
       if id == -1 :
               query = entry.select()
       else :
               query = entry.select("entry.id = %s" %id)
       i = 0
       try :
               query[0]
       except :
               print "Objetc not found"
               return None
       print msg %("-"*2,"-"*16,"-"*12,"-"*22)
       print msg %("id","Ip","Hostname","Descricao")
       print msg %("-"*2,"-"*16,"-"*12,"-"*22)
       while i < query.count():
               tmp = query[i]
               print msg %(tmp.id,tmp.ip,tmp.hostname,tmp.desc)
               i = i + 1
       print msg %("--","----------------","------------","----------------------")

def delete(id):
       try :
               a = entry.get(id)
               a.destroySelf()
       except SQLObjectNotFound :
               print "Object not found!"

def edit(id,num,new_value):
       try :
               num = int(num)
               tmp = entry.get(id)
               if num == 1:
                       tmp.set(ip="%s" %new_value)
               elif num == 2:
                       tmp.hostname = "%s" %new_value
               elif num == 3:
                       tmp.passwd = "%s" %new_value
               elif num == 4:
                       tmp.user = "%s" %new_value
               elif num == 5:
                       tmp.desc = "%s" %new_value
       except SQLObjectNotFound :
               print "Object not found!"

def usage():
       print "Uso : auto_ssh id     (modo de conexão rápida)"
       print "      auto_ssh        (modo interativo)"
       print "      auto_ssh -l     (imprime a lista)"
       print "      auto_ssh -e id  (editar o registro id)"
       print "      auto_ssh ip     (adiciona/conecta no ip)"

def _exit(x) :
       print '-'*41
       print "----| Obrigado por usar o autossh ! |----"
       print '-'*41
       sys.exit(x)

def connect(id):
       reg = entry.get(id)
       ping = pexpect.spawn ('ping %s' %reg.ip)
       rc = ping.expect(['ms','Unreachable'])
       if rc == 0 :
               ms = er_ms.search(ping.before)
               ms =  ms.group('ms')
               ms = float(ms)
               if ms > 400 :
                       ms_msg = "WARNING :: Your ms is bad : %s , you connection may be slow" %ms
               else :
                       ms_msg = "INFO :: Your ms is good : %s " %ms
       else :
               print "The host %s is not online" %reg.ip
               ping.close()
               _exit(1)
       ping.close()
       child = pexpect.spawn ('ssh %s -l %s' %(reg.ip,reg.user))
       rc = child.expect (i_expect)
       if rc == 0 :
               child.sendline('%s' %reg.passwd)
               child.expect("\n")
       elif rc == 1:
               child.sendline('yes')
               child.expect('assword:')
               child.sendline('%s' %reg.passwd)
       elif rc == 2:
               er_ip = re.compile('^%s.*$' %reg.ip)
               hosts = open(host_path,"r")
               new_hosts = open(host_path_tmp,"w")
               while 1 :
                       tmp = hosts.readline()
                       if tmp == "":
                               os.remove("%s" %host_path)
                               os.rename(host_path,host_path_tmp)
                               break
                       elif er_ip.match(tmp):
                               continue
                       else:
                               new_hosts.write(tmp)
       elif rc == 3:
               print "Connection to " + reg.ip + " refused"
               _exit(1)
       elif rc == 4:
               print reg.ip + " : no route to host"
               _exit(1)
       er_f1 = re.compile(".*hostname.*")
       if not isinstance(reg.hostname,str):
               print "I will set the name"
               try :
                       child.expect("\n",5)
               except :
                       pass
               child.sendline("hostname") # envia o comando
               child.expect("\n") # vai comendo linha ate achar a resposta do "hostname"
               while er_f1.match(child.before):
                       child.expect("\n") # vai comendo linha ate achar a resposta do "hostname"
               reg.hostname = child.before[:-1]

       print "\n" + ms_msg
       msg = "| %-8s : %-22s |"
       print '\n+' + '-'*35 + '+'
       print msg %('Ip',reg.ip)
       print msg %('Hostname',reg.hostname)
       print msg %('Desc',reg.desc)
       print '+' + '-'*35 + '+'
       print "\n-----| Have Fun ! |-----"
       print "\n",
       child.interact()
       child.close()

# Se nao tiver a tabela , cria
entry.createTable(ifNotExists=1)
if len(sys.argv) > 1:
       if sys.argv[1] == "-e" :
               try :
                       reg = entry.get(sys.argv[2])
                       while 1:
                               msg = "| %s | %-10s : %-24s |"
                               print "What you want to edit?"
                               print '\n+' + '-'*43 + '+'
                               print msg %('1','ID',reg.id)
                               print msg %('2','IP',reg.ip)
                               print msg %('3','USER',reg.user)
                               print msg %('4','Hostname',reg.hostname)
                               print msg %('5','Pass','********')
                               print msg %('6','Desc',reg.desc)
                               t = '-'*24
                               print msg %('-','----------',t)
                               print msg %('7','Exit','Stop editing')
                               print '+' + '-'*43 + '+'
                               opc = input("Choose [2-7] : ")
                               if opc > 7:
                                       print "Enter a valid choice "
                                       continue
                               elif opc < 2:
                                       print "Enter a valid choice "
                                       continue
                               elif opc == 7:
                                       _exit(0)
                               new_value = raw_input("The new value are : ")
                               if opc == 2:
                                       reg.ip = new_value
                               elif opc == 3:
                                       reg.user = new_value
                               elif opc == 4:
                                       reg.hostname = new_value
                               elif opc == 5:
                                       reg.passwd = new_value
                               elif opc == 6:
                                       reg.desc = new_value
               except "maria" :
                       print "Wrong id or no id"
                       _exit(0)
       if sys.argv[1] == "-l" :
               if len(sys.argv) == 2:
                       list()
               else :
                       try :
                               list(sys.argv[2])
                       except SQLObjectNotFound :
                               print "Object not found!"
                       _exit(0)
       elif sys.argv[1] == "-r" :
               try:
                       reg = entry(sys.argv[2])
                       reg()
                       reg.remove()
               except :
                       print "Wrong id or no id"
               _exit(0)
       elif er_id.match(sys.argv[1]) :
               try :
                       connect(sys.argv[1])
               finally :
                       _exit(0)
       elif er_ip.match(sys.argv[1]) :
               ip = raw_input("Digite o IP: ")
               user = raw_input("Digite o USERNAME: ")
               passwd = raw_input("Digite o PASSWORD: ")
               reg = entry(user=user,ip=ip,passwd=passwd)
               connect(reg.id)
               _exit(0)
       elif sys.argv[1] == "-h" :
               usage()
       else:
               menu()
os._exit(0)
