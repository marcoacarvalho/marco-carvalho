import socket

def verifica_conexao (self):
    retorno = True
    a=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a.settimeout(.3)
    try:
        a.connect_ex(("www.antonioprado.eti.br", 81))
    except:
        retorno = False
    a.close()
    return retorno
