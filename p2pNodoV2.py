import socket
import time
import sys
import os
import random
from thread import *
import threading
from files import *
from log import *

diccIPsCli = {}
diccIPsServ = {}
ruta = sys.argv[1]
miip = sys.argv[2]

#controla desconexiones de un nodo
def lanzador(conn):
    try:
        acciones(conn)
    except:
        conn.close
        for k in diccIPsCli.keys():
            if diccIPsCli[k]==conn:
                del (diccIPsCli[k])
                del (diccIPsServ[k])

#todas las posibles soluciones a una peticion de un nodo
def acciones(conn):
    while True:
        case = conn.recv(1024)
        print('Se recibio opcion: ', case)
        if case == 'l':  # l define quien inicia la sync
            msg = conn.recv(1024)  # se queda bloqueado escuchando
            if int(msg) != 0:
                temp=diccIPsCli.values()
                temp.remove(None)
                rnd = random.choice(temp)
                rnd.send('l')
                rnd.send(str(int(msg) - 1))
                print 'se renvio l con valor: ', msg
            else:
                conn.send('r')  # inicia sync
                print 'se envio r con valor'
                enviarFile('logNodo.txt', rnd)
        elif case == 'r':  # r actualiza el log de revision
            recibirFile('logRevision.txt', conn)

            actualizaLogRevision('logNodo.txt', 'logRevision.txt', miip)

            ipList, fileList = leerLog('logRevision.txt')
            nodosNoVisitados = compararDirecciones(ipList)  # compara cada item en cada lista
            print 'obtuve no visi: ', nodosNoVisitados

            if len(nodosNoVisitados) > 0:
                con = diccIPs[nodosNoVisitados[0]]
                con.send('r')
                enviarFile('logRevision.txt', con)
                print 'renvio r'
            else:
                temp=ipList
                temp.remove(miip)
                conexion = diccIPs[temp[0]]  # ala primera ip empieza sync
                conexion.send('s')
                time.sleep(1)
                copiarLogSync('logRevision.txt', 'logSync.txt')
                print 'envio s y logSync'
                enviarFile('logSync.txt', conexion)
                actualizar()  # ya tienes log, lo abriste y ejecutas operaciones -> actualizacion

        elif case == 's':  # s actualiza la carpta local

            recibirFile('logSync.txt',conn)

            actualizar()
            ipList, fileList = leerLog('logSync.txt')
            ipList.append(miip)# aniado ip nood actual
            nodosNoVisitados = compararDirecciones(ipList)  # compara cada item en cada lista

            if len(nodosNoVisitados) > 0:

                con = diccIPs[nodosNoVisitados[0]]
                con.send('s')
                time.sleep(3)
                enviarFile('logSync.txt', con)
                # reinicio el tiempo de sync
            else:
                hiloTemporizadr(con)

        elif case=='f':  # f envia el archivo
            archivo = conn.recv(1024)
            enviarFile(archivo, conn)
        else:
            conn.close()
            for k in diccIPs.keys():
                if diccIPs[k] == conn:
                    del (diccIPs[k])

# borra, copia archivos creados en la carpeta remota
def actualizar():
    print 'empiezo la syncronizacion'

    #cargon info de los logs
    ipListSync, fileListSync = leerLog('logSync.txt')
    ipListLocal, fileListLocal = leerLog('logNodo.txt') # log Local .txt

    # comparo informacion de sincronizacion e infrmacion local
    for file in fileListSync:
        boo = False
        for a in fileListLocal:
            if file['nombre'] == a['nombre']:
                boo = True
                # ejecuto operacion si la operacion cambia de un archivo cambia
                if file['operacion'] != a['operacion']:
                    if file['operacion'] == 'delete':
                        borrarFile(file['nombre'], ruta)
                    else:
                        solicitarFile(file['nombre'], file['from'])  #
        # solicito un archivo si no existia localmente
        if boo == False:
            if file['operacion'] == 'add':
                solicitarFile(file['nombre'], diccIPs[file['from']])  #

    # el log local tiene ahora el contenido del syncronizado
    copiarLogSync('logSync.txt', 'logNodo.txt')
    print 'termino la syncronizacion'


#compara ip de un log con ipdel Diccionario de conexxiones
def compararDirecciones(ipList):
    print 'comparandodirecciones'
    list = []
    print diccIPs.keys()
    for ipA in ipList:
        if ipA not in diccIPs.keys():
            list.append(ipA)
            print ipA
    return list


#conecto como cliente
def conectar(ip):
    HOST = ip  # The remote host
    PORT = 8888  # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #reusar socket
    s.connect((HOST, PORT))
    print 'conectado como cliente al punto ' + ip
    diccIPsCli[ip] = s
    #time.sleep(1)
    print 'todas las conexiones cli: ', diccIPsCli.values()
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

        diccIPsServ[addr[0]] = conn
        #time.sleep(1)
        global diccIPsCli
        if not addr[0] in diccIPsCli.keys():
            conectar(addr[0])

    s.close()

#chequea archivos en la carpeta compartida
def monitorear(x):
    #contenido de ls
    fe = os.popen("ls -l "+ruta +" |awk '{ print $8 \"|\" $9 }'").read()
    print 'monitoreando', fe

    # todoo el contenido como borrado
    iplocal, fileLocal = leerLog('logNodo.txt')
    if '' in iplocal:
        iplocal.remove('') ###OJOOO
    if len(iplocal)==0:
        iplocal.append(miip)
    for file in fileLocal:
        file['operation']='delete'
        file['timestamp']=time.strftime("%H:%M")

    #comparo ultimo log local con el contenido actual de ls
    aux=fe.splitlines()
    for i in range(1,len(aux)):
        boo = False
        campos = aux[i].split('|')
        # valido un archivo si existe y no ha sido elminado
        for file in fileLocal:
            if file['nombre'] == campos[1].strip('\n'):
                boo = True
                file['operacion'] = 'add'
                file['timestamp'] = campos[0].strip('\n')
        # se coloca nuevos campos
        if not boo:
            fileLocal.append({'nombre': campos[1].strip('\n'),
                              'operacion': 'add',
                              'timestamp': campos[0].strip('\n'),
                              'from': miip})
    #print 'Iplocal: ', iplocal, ' FileLocal: ', fileLocal
    creaLog(iplocal,fileLocal,'logNodo.txt')  #escribe el log


#fin monitorear

# hilo temporizador reinicio sincronizacion
def hiloTemporizadr(conn):
    threading.Thread(target=temporizador, args=(conn))

# este hilo espera para poder realizar la sincronizacion nuevamente
def temporizador(conn):
    print 'fin sincronizar nodos'
    time.sleep(60)
    conn.send('l')
    conn.send('100')
    print 'reinicio conteo regresivo'

# ############################
# intenta conectarse con todos los posiubles ips
posibles = ['192.168.59.132','192.168.59.149'] #dar ips default ojoo
posibles.remove(miip)


print 'calculando posibles ip'
"""
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
"""
print 'finalizado posibles: ', posibles

# levanta servidor como hilo
server = threading.Thread(target=serv, args=()).start()
print 'Se levanto el servidor'
time.sleep(2)


# se coneccta como cliente
for ip in posibles:
    try:
        threading.Thread(target=conectar, args=(ip,)).start()
    except:
        pass
print 'finalizo busqueda e intento de conexion '

time.sleep(4)

# si es el segundo equipo conectarse en la red inicia sincronizacion
if len(diccIPsCli.values()) == 1:
    rnd = random.choice(diccIPsCli.values())
    print 'Por enviar a: ',rnd
    rnd.send('l')
    rnd.send('30')

diccIPsCli[miip]=None #doy direccion local vacia
diccIPsServ[miip]=None


# hilo que se encarga de monitorear los archivos y carpetas
x=0
while True:
    monitorear(x)
    x+=1
    time.sleep(180)



