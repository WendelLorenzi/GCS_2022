# coding=utf-8
from src.serialCom.index import SerialC
from src.serialCom.conection import ConectionS
import _thread
import time
from multiprocessing import Process
from src.dataframes.index import dataframe

class Main:            
    def setStart(final= False):
        print('chamado final', final)
        conection= ConectionS()
        serial= SerialC()
        _thread.start_new_thread(serial.Captura, (conection, '/dev/ttyACM0', ))

    def loandDataset():
        while True:
            time.sleep(5)
            p = Process(target=dataframe().unifyData, args= ())
            p.start()
            p.join()
        
    
    