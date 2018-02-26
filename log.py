import datetime

def creaLog(listaIP,listaArchivos):
    with open('log.txt','w') as archivoLog:

        # escribo IP
        for ip in listaIP:
            archivoLog.write(str(ip)+'\n')

        # escribo Archivos
        archivoLog.write('Files:\n')
        for file in listaArchivos:
            line=file['nombre']+'|'
            +file['operacion']+'|'
            +file['timestamp']+'|'
            +file['from']
            archivoLog.write(line+'\n')

def leerLog(archivoLog):
    ipList=[]
    fileList=[]

    with open (archivoLog,'r') as arch:
        # leo IP
        line=arch.readline()
        while not 'Files' in line:
            ipList.append(line)
            line=arch.readline()

        # leo archivos
        while line:
            campos = line.split('|')
            # creo un diccionario de los campos y lo pongo en la lista
            diccionCampo = {'nombre':campos[0].strip('\n'),
                   'operacion':campos[1].strip('\n'),
                   'timestamp':campos[2].strip('\n'),
                   'from':campos[3].strip('\n')}
            print diccionCampo
            fileList.append(diccionCampo)
            line=arch.readline()

    return ipList,fileList


def creaLogRevision(logA,logR):
    ipA,fileListA=leerLog(logA)
    ipR,fileListR=leerLog(logR)
    logFinal=[]

    for fileA in fileListA:
        if fileA in fileListR:
            if fileA['nombre']==fileR['nombre']:
                tiempoA = datetime.
                tiempoB=
                if
            else:

def actualiza()
    ip