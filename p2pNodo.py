import socket
import time
import sys
import os
import random
from thread import *
from files import *
from log import *

diccIPs = {}
ruta = sys.argv[1]
miip = sys.argv[2]

def lanzador(conn):
    if len(diccIPs.values()) == 1:
        rnd = random.choice(diccIPs.values())
        rnd.send('l')
        rnd.send(100)
    else:
        while True:
            case = conn.recv(1024)
            print('Se selecciono opcion: ', case)
            if case == 'l': #l define quien inicia la sync
                msg = conn.recv(1024) #se queda bloqueado escuchando
                if int(msg) != 0:
                    rnd = random.choice(diccIPs.values())
                    rnd.send(str(int(msg) - 1))
                else:
                    conn.send('r')  #inicia sync
                    enviarFile('logRevision.txt', rnd)
            elif case == 'r': #r actualiza el log de revision
                recibirFile('logRevision.txt',conn)
                creaLogRevision('logNodo .txt', 'logRevision.txt')

                ipList, fileList = leerLog('logRevision.txt')
                nodosNoVisitados = compararDirecciones(ipList) #compara cada item en cada lista

                if len(nodosNoVisitados) > 0:
                    con = diccIPs[nodosNoVisitados[0]]
                    con.send('r')
                    enviarFile('logRevision.txt', con)
                else:
                    conexion = diccIPs[ipList[0]] #ala primera ip empieza sync
                    conexion.send('s')
                    copiarLogSync('logRevision.txt', 'logSync.txt')
                    enviarFile('logSync.txt', conexion)
                    actualizar()    #ya tienes log, lo abriste y ejecutas operaciones -> actualizacion
            elif case == 's': #s actualiza la carpta local
                recibirFile('logSync.txt')
                actualizar()
                ipList, fileList = leerLog('logSync.txt')
                nodosNoVisitados = compararDirecciones(ipList)  # compara cada item en cada lista

                if len(nodosNoVisitados) > 0:
                    con = diccIPs[nodosNoVisitados[0]]
                    con.send('s')
                    enviarFile('logSync.txt', con)
                    # reinicio el tiempo de sync
                    conn.send('l')
                    conn.send(100)

            else: #f envia el archivo
                archivo = conn.recv(1024)
                enviarFile(archivo,conn)

def actualizar():
    ipListSync, fileListSync = leerLog('logSync.txt')
    ipListLocal, fileListLocal = leerLog('logNodo.txt') # log Local .txt
    for file in fileListSync:
        boo = False
        for a in fileListLocal:
            if file['nombre'] == a['nombre']:
                boo = True
                if file['operacion'] != a['operacion']:
                    if file['operacion'] == 'delete':
                        borrarFile(file['nombre'], ruta)
                    else:
                        solicitarFile(file['nombre'], file['from'])  #
        if boo == False:
            if file['operacion'] == 'add':
                solicitarFile(file['nombre'], diccIPs[file['from']])  #
    #
    copiarLogSync('logSync.txt', 'logRevision.txt')


def compararDirecciones(ipList):
    list = []
    for ipA in ipList:
        if not ipA in diccIPs.keys():
            list.append(ipA)
    return list


#conecto como cliente
def conectar(ip):
    HOST = ip  # The remote host
    PORT = 8888  # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #reusar socket
    s.connect((HOST, PORT))
    print 'conectado al punto ' + ip
    diccIPs[ip] = s
    #time.sleep(1)
    print 'Conexiones exitosas: ', diccIPs.values()
    lanzador(s) #inicia

#conecto como servidor
def serv():
    def clientthread(conn):
        try:
            lanzador(conn)
        except:
            conn.close()

    # ******************************************
    nc = 10         #num clientes
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

        start_new_thread(clientthread, (conn,)) #

        #time.sleep(1)
        global diccIPs
        if not addr in diccIPs.keys():
            diccIPs[addr]=conn

    s.close()

# ############################
# intenta conectarse con todos los posiubles ips
posibles = [] #dar ips default ojoo
for i in range(2, 50):
    print i
    try:
        cade = '192.168.0.'+ repr(i)
        a = os.popen('ping -n 1 ' + cade).read()
        #print a
        #if not 'inaccesible' in a:
        if not 'inaccesible' in a :
            posibles.append(cade)
            print 'Find, succes'
    except:
        continue

# levanta servidor como hilo
server = start_new_thread(serv())

# se coneccta como cliente
for ip in posibles:
    try:
        start_new_thread(conectar(ip))
    except:
        pass

# hilo que se encarga de monitorear los archivos y carpetas

def monitorear():
    #miip = sys.argv[2]
    fe = os.system("ls -l'"+ruta +" '|awk '{ print $8 '|' $9 }'")
    iplocal, fileLocal = leerLog('logNodo.txt')
    for file in fileLocal:
        file['operation']='delete'
        file['timestamp']=time.time()
    i=0
    for line in fe.split('\n'):
        boo = False
        campos = line.split('|')
        if i != 0:
            for file in fileLocal:
                if file['nombre'] == campos[1].strip('\n'):
                    boo = True
                    file['operacion'] = 'add'
                    file['timestamp'] = campos[0].strip('\n')
            if not boo:
                fileLocal.append({'nombre':campos[1].strip('\n'),
                   'operacion':'add',
                   'timestamp':campos[0].strip('\n'),
                   'from':miip})
        i += 1
