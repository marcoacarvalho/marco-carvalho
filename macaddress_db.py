import os, sys

try:
    from sqlobject import *
except:
    print "Erro ao carregar o modulo SQLObject"
    sys.exit(1)

session_db = 'sqlite://' + os.path.dirname(__file__) +'/macaddress.db'
class Host(SQLObject):
    _connection = connectionForURI(session_db)
    HostName = StringCol (length=10, unique = "True")
    MacAddress = StringCol (length=11, unique = "True")
    Host_IP = StringCol (length=7, unique = "True")
    Local = StringCol (length=15, default="OFM")
