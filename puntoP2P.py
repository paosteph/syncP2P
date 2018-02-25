import os
#import libClie_Serv as wc
import threading
clientes=[]

for i in range(2, 254):
    print i
    try:
        cade = '192.168.0.'+ repr(i)
        a=os.popen('ping -n 1 ' + cade).read()
        #print a
        #if not 'inaccesible' in a:
        if not 'inaccesible' in a :
            clientes.append(cade)
            print 'succes'
    except:
        continue

"""
for c in clientes:
    print c
    try:
        a = threading.Thread(target=wc.cli(c), args=())
        a.daemon = True
        a.start()
    except:
        continue

threading.Thread(target=wc.serv(), args=()).start()"""

