# coding=utf-8
from src.serialCom.index import SerialC
from src.serialCom.conection import ConectionS
import _thread
import time
from multiprocessing import Process

def setStart(conection= ConectionS(), serial= SerialC()):
    print('fui chamadoooooo start')
    _thread.start_new_thread(serial.Captura, (conection, '/dev/ttyACM0', ))
    while True:
        time.sleep(9)
        p = Process(target= serial.carregaCsv, args= (conection, ))
        print('chamei process')
        p.start()
        p.join()
        p.terminate()
        
    
def setStop(conection= ConectionS(), serial= SerialC()):
    print('fui chamadoooooo stop')
    p = Process(target= serial.Captura, args= (conection, '/dev/ttyACM0', True, ))
    p.start()
    print('fui chamado terminate process')
        