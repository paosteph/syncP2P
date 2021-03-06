import os

def creaLog(listaIP,listaArchivos,nombre):
    with open(nombre,'w') as archivoLog:
        # escribo IP
        for ip in listaIP:
            archivoLog.write(ip.strip('\n')+'\n')

        # escribo Archivos
        archivoLog.write('Files:')
        for file in listaArchivos:
            #print 'va a escribir logR'
            line=str(file['nombre'])+'|'+str(file['operacion'])+'|'+str(file['timestamp'])+'|'+str(file['from'])
            archivoLog.write('\n')
            archivoLog.write(line)


def leerLog(archivoLog):
    ipList=[]
    fileList=[]

    with open (archivoLog,'r') as arch:
        # leo IP
        line=arch.readline()
        while not 'Files:' in line:
            ipList.append(line.strip('\n'))#ojo strip
            line=arch.readline()

        # leo archivos
        line = arch.readline()
        while line:
            campos = line.split('|')
            # creo un diccionario de los campos y lo pongo en la lista
            diccionCampo = {'nombre':campos[0].strip('\n'),
                   'operacion':campos[1].strip('\n'),
                   'timestamp':campos[2].strip('\n'),
                   'from':campos[3].strip('\n')}
            #print diccionCampo
            fileList.append(diccionCampo)
            line=arch.readline()

    return ipList,fileList


def actualizaLogRevision(logA,logR,miip):
    ipA,fileListA=leerLog(logA)
    ipR,fileListR=leerLog(logR)
    fileListTemp=[]
    print 'Actualizando log revision'
    print 'fileA: ',fileListA
    print 'fileR: ', fileListR
    boo = False  # para que sino existe un archivo en la revision, se aniada
    for fileA in fileListA:
        for fileR in fileListR:
            if fileA['nombre']==fileR['nombre']:
                print('coinciden archivos')
                a=int(fileR['timestamp'].replace(':',''))
                print 'a',a
                b=int(fileA['timestamp'].replace(':',''))
                print 'b',b
                if a >= b:
                    fileR['operacion']=fileA['operacion']
                    print 'comparo horas'
                boo=True
        if boo==False:
            fileListTemp.append(fileA)
            print('agrego archivo nuevo')
    fileListR += fileListTemp
    # aumento ip visitada
    if miip not in ipR:
        ipR.append(miip)
    print 'ip actuales: ', ipR
    print 'filelist: ', fileListR
    creaLog(ipR,fileListR,'logRevision.txt')

def copiarLogSync(fileA, fileB):
    os.system('cp '+fileA+' '+ fileB)
    print fileA,' copiado en ',fileB

