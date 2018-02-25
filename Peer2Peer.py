import socket
import time
import sys
from thread import *
import threading

def sendClient(cli, msg):
    global adressingCli
    adressingCli.get(cli).send(msg)



def responder():

    while 1:
        msg = raw_input()

        if msg == 'adios':
            sendBroad(msg)
            print 'terminando'
            break

        client = msg.split(':')[0].strip('\n')
        message = msg.split(':')[1].strip('\n')

        try:
            sendClient(client, message)
        except:
            break#:3

def cliSender():
    # envio
    t = threading.Thread(target=responder, args=())
    t.start()

#enviar a todos
def sendBroad(msg):
    for con in adressingCli:
        try:
            con.sendall(msg)
        except:
            continue

#conecto como cliente
def conectar(ip):
    HOST = ip  # The remote host
    PORT = 8888  # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#reusar socket
    s.connect((HOST, PORT))
    print 'conectado al punto ' + ip
    time.sleep(2)
    nickR=s.recv(1024)
    print('new user: ' + nickR + ' Connected users: ' + repr(adressingCli))
    s.send(mynick)
    return nickR, s

#conecto como servidor
def serv():
    def clientthread(conn):
        # Sending message to connected client
        conn.send(mynick)
        name=conn.recv(1024)
        # infinite loop so that function do not terminate and thread do not end.
        while True:
            try:
                print 'escuchando'
                # Receiving from client
                receive = conn.recv(1024)

                if receive == 'adios':
                    print 'eliminando cliente ' + name
                    adressingCli.pop(name)
                    #sendBroad('Connected users: ' + repr(adressingCli))
                    break


                reply = name + ': ' + receive  # raw_input()#'OK...' + data
                print reply


            except:
                pass

        # came out of loop
        conn.close()


    # ******************************************
    nc = 10
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 8888  # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reusar socket
    print 'Socket created'

    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket bind complete'

    # Start listening on socket
    s.listen(nc)
    print 'Socket now listening'

    while 1:
        # wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        # hilo de escucha

        Threads.append(start_new_thread(clientthread, (conn,)))

        time.sleep(1)
        global adressingCli
        if conn in adressingCli.values():

            aux0,aux1 = conectar(addr[0])
            print 'Encontro',aux0,aux1
            adressingCli[aux0] = aux1

    s.close()

Threads=[]
mynick=raw_input('your nick? ')
adressingCli={}

#busco cada posible destino
IPs=['172.29.36.143']

print 'buscando'
for ip in IPs:
    try:
        aux0,aux1=conectar(ip)
        print 'Encontro',aux0,aux1
        #global adressingCli
        adressingCli[aux0]=aux1
    except:
        pass

#print adressingCli
# levanto hilo enviador a cualquier conexion
sender = cliSender()

# cada punto tiene su servidor
server = start_new_thread(serv())

