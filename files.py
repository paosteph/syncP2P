import os
#from socket import error

BUFFER_SIZE = 1024

def enviarFile(file, conn):
    f = open(file, 'rb')
    print 'enviando: ',file

    while True:
        l = f.read(BUFFER_SIZE)
        while (l):
            conn.send(l)
            print 'Tipo dato l: ', type(l)
            print 'Enviado ',repr(l)
            l = f.read(BUFFER_SIZE)
        #if not l:
        #    conn.send('12345')
        #    f.close()
            #conn.close()
        break
    conn.send(chr(1))
    f.close()

    print 'fin enviar: ',file

def recibirFile(file, conn):
    print 'recibiendo: ',file
    with open(file, 'wb') as f:
        print 'file',file,' opened'
        while True:
            try:
                data = conn.recv(BUFFER_SIZE)
            except:
                print("Error de lectura.")
                break
            else:
                if data:
                    # Compatibilidad con Python 3.
                    if isinstance(data, bytes):
                        end = data[0] == 1
                    else:
                        end = data == chr(1)
                    if not end:
                        # Almacenar datos.
                        f.write(data)
                        print('data: ', (data))
                    else:
                        break
            #print 'Tipo de dato de data: ',type(data)
            """
            print('data: ', (data))
            if '1' in data:
                f.close()
                print 'file close()'
                break
            # write data to a file
            f.write(data)
            data = ''
            """

    print("El archivo se ha recibido correctamente.")
    f.close()
    print('Recibio archivo',file)
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
    print 'solicitado: ',arch
    recibirFile(arch,con)

