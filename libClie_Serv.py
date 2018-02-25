import socket
import sys
from thread import *
import threading


def sendClient(cli, msg):
    j = 0
    for name in nickname:
        if name == cli:
            connectionsCli[j].send(msg)
            return True
        j += 1

    return False


def sendBroad(msg):
    for con in connectionsCli:
        try:
            con.sendall(msg)
        except:
            continue

def readInput():
    x = 'si'
    text = ''
    while x == 'si':
        tecla = sys.stdin.read(1)
        text += tecla
        if tecla == '\n':
            x = 'no'

    return text

def responder():

    while 1:
        # msg = raw_input()
        msg = readInput().strip('\n')

        if msg == 'adios':
            sendBroad(msg)
            print 'terminando'
            break

        client = msg.split(':')[0].strip('\n')
        message = msg.split(':')[1].strip('\n')

        try:
            sendClient(client, message)
        except Exception:
            # s.close()
            break
             # s.close()

def conectar(ip):
    HOST = ip  # The remote host
    PORT = 8888  # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print 'conectado al punto ' + ip
    s.send(mynick)
    return  s

def cliSender():
    # envio
    t2 = threading.Thread(target=responder, args=())
    t2.start()


def serv():


    # Function for handling connections. This will be used to create threads
    def clientthread(conn):
        # Sending message to connected client
        name = conn.recv(1024)
        global nickname
        nickname.append(name)
        print('new user: '+name+' Connected users: ' + repr(nickname))

        # infinite loop so that function do not terminate and thread do not end.
        while True:
            try:
                # Receiving from client
                receive = conn.recv(1024)

                if receive == 'adios':
                    print 'eliminando cliente ' + name
                    connections.remove(conn)
                    nickname.remove(name)
                    sendBroad('Connected users: ' + repr(nickname))
                    break

                client = receive.split(':')[0].strip('\n')
                message = receive.split(':')[1].strip('\n')

                reply = name + ': ' + message  # raw_input()#'OK...' + data
                print reply

                #confirma recivido
                #if sendClient(client, reply):
                    #conn.send('You: ' + message)
                #else:
                 #   conn.send('Client searched disconnected')

            except:
                continue

        # came out of loop
        conn.close()


    # ******************************************
    nc = 10
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 8888  # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    # Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket bind complete'

    # Start listening on socket
    s.listen(nc)
    print 'Socket now listening'

    # now keep talking with the client
    threads = []
    # position address

    while 1:
        # wait to accept a connection - blocking call
        conn, addr = s.accept()
        connections.append(conn)
        print 'Connected with ' + addr[0] + ':' + str(addr[1])

        # hilo de escucha
        threads.append(start_new_thread(clientthread, (conn,)))

        #hilo de envio
        connections.append(start_new_thread(conectar(addr[0])))

    s.close()

mynick=raw_input('your nick? ')
connections = []
nickname = []

# cada punto tiene su servidor
sever = serv()

#busco cada posible destino
IPs=['172.29.36.143']

#creo conexion a cada destino
connectionsCli=[]
for ip in IPs:
    try:
        connectionsCli.append(conectar(ip))
    except:
        continue


#levanto hilo enviador a cualquier conexion
sender=cliSender()