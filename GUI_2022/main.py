# coding=utf-8
from src.serialCom.index import SerialC
from src.serialCom.conection import ConectionS
import _thread
import time
from multiprocessing import Process
from src.dataframes.index import dataframe
from tela import Tela

class Main:            
    def setStart(final= False):
        print('chamado final', final)
        _thread.start_new_thread(SerialC.Captura, (ConectionS, '/dev/ttyACM0', ))
    
    def loadDataframes():
        print('entrei load Dataframes')
        while True:
            time.sleep(8)
            p = Process(target=SerialC.carregaCsv, args= (ConectionS, ))

    def loandDataset():
        print('entrei loadDataset')
        while True:
            time.sleep(10)
            p = Process(target=dataframe.unifyData, args= ())
            p.start()
            p.join()
    
    def renderTela():
        print('entrei render tela')
        _thread.start_new_thread(Tela.renderTela, ())
    
        
    
    