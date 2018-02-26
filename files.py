import os

BUFFER_SIZE = 1024

def enviarFile(file, conn):
    f = open(file, 'rb')
    while True:
        l = f.read(BUFFER_SIZE)
        while (l):
            conn.send(l)
            print('Enviado ',repr(l))
            l = f.read(BUFFER_SIZE)
        if not l:
            f.close()
            #conn.close()
            break

def recibirFile(file, conn):
    with open(file, 'wb') as f:
        print 'file',file,' opened'
        while True:
            data = conn.recv(BUFFER_SIZE)
            print('data=%s', (data))
            if not data:
                f.close()
                print 'file close()'
                break
            # write data to a file
            f.write(data)

    print('Recibio archivo')
    #conn.close()

def borrarFile(file, ruta):
    fd = os.system('rm '+ruta+' '+file)
    if 'No se pudo acceder al fichero' in fd:
        print 'Error borrando, no existe'
    else:
        print file, ' : borrado'


def solicitarFile(arch,con):
    con.send('f')
    con.send(arch)
    recibirFile(arch,con)

