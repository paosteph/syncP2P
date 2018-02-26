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


def actualizaLogRevision(logA,logR,miip):
    ipA,fileListA=leerLog(logA)
    ipR,fileListR=leerLog(logR)

    for fileA in fileListA:
        boo=False
        for fileR in fileListR:
            if fileA['nombre']==fileR['nombre']:
                if int(fileR['timestamp'].strip(':'))<int(fileA['timestamp'].strip(':')):
                    fileR['operacion']=fileA['operacion']
        if boo==False:
            fileListR.append(fileA)

    # aumento ip visitada
    ipR.append(miip)

    creaLog(ipR,fileListR)

def copiarLogSync():

