import os
import time
#from socket import error

BUFFER_SIZE = 1024

def enviarFile(file, conn):
    f = open(file, 'rb')
    print 'enviando: ',file

    while True:
        l = f.read(BUFFER_SIZE)
        while (l):
            conn.send(l)
            #print 'Tipo dato l: ', type(l)
            print 'Enviado ',repr(l)
            l = f.read(BUFFER_SIZE)
        #if not l:
        #    conn.send('12345')
        #    f.close()
            #conn.close()
        break
    time.sleep(1)
    conn.send('12345')
    f.close()

    print 'fin enviar: ',file

def recibirFile(file, conn):
    print 'recibiendo: ',file
    with open(file, 'wb') as f:
        print 'file',file,' opened'
        while True:
            data = conn.recv(BUFFER_SIZE)
            print('data: ', (data))
            if '12345' in data:
                f.close()
                print 'file cerrado'
                break
            # write data to a file
            f.write(data)

    print('Recibio archivo',file)
    #conn.close()
    return True

def borrarFile(file, ruta):
    fd = os.system('rm '+ruta+' '+file)
    if 'No se pudo acceder al fichero' in fd:
        print 'Error borrando, no existe'
    else:
        print file, ' : borrado'


def solicitarFile(arch,con):
    con.send('f')
    con.send(arch)
    print 'solicitado: ',arch
    recibirFile(arch,con)

