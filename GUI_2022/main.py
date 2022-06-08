# coding=utf-8
from xmlrpc.client import boolean
from src.serialCom.index import SerialC
from src.serialCom.conection import ConectionS
import _thread
import time
from multiprocessing import Process
from src.dataframes.index import dataframe
import tela

class Main:
    def getData(self, conection: ConectionS, serial:  SerialC):
        while True:
            time.sleep(3)
            serial.carregaCsv(conection)
            
    def setStart(self, final= False):
        conection= ConectionS()
        serial= SerialC()
        if(final != True):
            _thread.start_new_thread(serial.Captura, (conection, '/dev/ttyACM0', ))
            _thread.start_new_thread(self.getData, (serial, conection, ))
        else:
            self.loandDataset()
            
    
    def loandDataset():
        while True:
            time.sleep(5)
            p = Process(target=dataframe().unifyData, args= ())
            p.start()
            p.join()
        
if __name__ == '__main__':
    tela.Tela()
    
    