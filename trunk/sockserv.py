import socket
import thread
import os
import commands

HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta


def conectado(con):
    print 'Conectado por', cliente
    while True:
        msg = con.recv(1024)
        if not msg: break
    print commands.getstatusoutput("%s") % msg
    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con]))

tcp.close()
