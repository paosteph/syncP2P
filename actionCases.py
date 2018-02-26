import Peer2Peer as p2p
import socket

BUFFER_SIZE = 1024
TCP_IP = 'localhost'
TCP_PORT = 9001

def acciones(letra):
    if letra == 'r':
        revisarLog()
    elif letra == 's':
        sincronizar()
    elif letra == 'f':
        enviarFiles()
    else:
        escogerLeader()

def revisarLog():

    return 0

def sincronizar():
    return 0

def enviarFiles():
    #llamar a funcion que pase los archivos para server

    return 0

def escogerLeader():
    return 0


def transferirFiles(socket):
    sock = socket
    filename = 'mytext.txt' #path
    with open(filename, 'rb') as f:
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                sock.send(l)
                # print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                sock.close()
                break
                return 'Archivo transferido'


def monitorearFiles():
