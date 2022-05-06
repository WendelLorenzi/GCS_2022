# -*- coding: utf-8 -*-
import serial
import matplotlib.pyplot as plt
import time
import pandas as pd
import Txt from utils.Path_txt

class ConectionS:
    def __init__(self, altitudeC=[], temperaturaC=[], voltageC=[], gpsLatitudeC=[], gpsLongitudeC=[], gpsAlturaC=[], altitudeP= [], temperaturaP=[]):
        self.__altitudeC= altitudeC
        self.__temperaturaC= temperaturaC
        self.__voltageC= voltageC
        self.__gpsLatitudeC= gpsLatitudeC
        self.__gpsLongitudeC= gpsLongitudeC
        self.__gpsAlturaC= gpsAlturaC
        self.__altitudeP= altitudeP
        self.__temperaturaP= temperaturaP
    
    def setAltitudeC(self, altitudeC):
        self.__altitudeC.append(altitudeC)
    
    def setTemperaturaC(self, temperaturaC):
        self.__temperaturaC.append(temperaturaC)
    
    def setVoltageC(self, voltageC):
        self.__voltageC.append(voltageC)
    
    def setGpsLatitudeC(self, gpsLatitudeC):
        self.__gpsLatitudeC.append(gpsLatitudeC)
    
    def setGpsLongitudeC(self, gpsLongitudeC):
        self.__gpsLongitudeC.append(gpsLongitudeC)
    
    def setGpsAlturaC(self, gpsAlturaC):
        self.__gpsAlturaC.append(gpsAlturaC)
    
    def setAltitudeP(self, altitudeP):
        self.__altitudeP.append(altitudeP)
    
    def setTemperaturaP(self, temperaturaP):
        self.__temperaturaP.append(temperaturaP)
    
    def getAltitudeC(self):
        return self.__altitudeC
    
    def getTemperaturaC(self):
        return self.__temperaturaC
    
    def getVoltageC(self):
        return self.__voltageC
    
    def getGpsLatitudeC(self):
        return self.__gpsLatitudeC
    
    def getGpsLongitudeC(self):
        return self.__gpsLongitudeC
    
    def getGpsAlturaC(self):
        return self.__gpsAlturaC
    
    def getAltitudeP(self):
        return self.__altitudeP
    
    def getTemperaturaP(self, temperaturaP):
        return self.__temperaturaP
    
    
        
    # def filterVector(vetor):
    #     cont=0
    #     for(i in vetor):
    #         cont= cont + 1
    #         if(i == ''):
    #             #se a posição estiver vazia a mesma será ocupada pelo valor da posição anterior
    #             vetor[cont]= vetor[cont - 1]
    #     return vetor

    def drop_database(df):
            df.drop(columns=[
                'altitudeC',
                'temperaturaC',
                'voltageC',
                'gpsLatitudeC',
                'gpsLongitudeC',
                'gpsAlturaC',
                'altitudeP',
                'temperaturaP',
                'voltageP',
                'giroscopioR',
                'giroscopioP',
                'giroscopioY',
                'acelerometroR',
                'acelerometroP',
                'acelerometroY',
                'magnetometroR',
                'magnetometroP',
                'magnetometroY'])

    def carregaDataset(
        altitudeC):
        # temperaturaC,
        # voltageC,
        # gpsLatitudeC,
        # gpsLongitudeC,
        # gpsAlturaC,
        # altitudeP,
        # temperaturaP,
        # voltageP,
        # giroscopioR,
        # giroscopioP,
        # giroscopioY,
        # acelerometroR,
        # acelerometroP,
        # acelerometroY,
        # magnetometroR,
        # magnetometroP,
        # magnetometroY

            df= pd.read_csv('/home/wendel/Área de Trabalho/LtSat/GCS_2022/GUI_2022/datasets/transicao.csv', skiprows=1, sep=',', encoding="utf-8")
            if (df):
                df['altitudeC']= altitudeC
                # df['temperaturaC']= temperaturaC
                # df['voltageC']= voltageC
                # df['gpsLatitudeC']= gpsLatitudeC
                # df['gpsLongitudeC']= gpsLongitudeC
                # df['gpsAlturaC']= gpsAlturaC
                # df['altitudeP']= altitudeP
                # df['temperaturaP']= temperaturaP
                # df['voltageP']= voltageP
                # df['giroscopioR']= giroscopioR
                # df['giroscopioP']= giroscopioP
                # df['giroscopioY']= giroscopioY
                # df['acelerometroR']= acelerometroR
                # df['acelerometroP']= acelerometroP
                # df['acelerometroY']= acelerometroY
                # df['magnetometroR']= magnetometroR
                # df['magnetometroP']= magnetometroP
                # df['magnetometroY']= magnetometroY
            else:
                print('Error')

    def Captura(self, MSP):
        arquivoAltitudeC = open(str(Txt.altitudeC), 'w')
        arquivoTemperaturaC = open(str(Txt.temperaturaC), 'w')
        try:
            while MSP.bytesize > 0:
                MSP.flushOutput()
                MSP.flushInput()

                data = MSP.readline().decode()
                dataSplit= data.split(',')
                print(dataSplit)
                if len(dataSplit) > 1:
                    #filterVector(dataSplit)
                    if dataSplit[3] == "c":
                        self.setAltitudeC(dataSplit[0])
                        self.setTemperaturaC(dataSplit[1])
                    #     __init__.voltageC.append(dataSplit[2])
                    #     __init__.gpsLatitudeC.append(dataSplit[4])
                    #     __init__.gpsLongitudeC.append(dataSplit[5])
                    #     __init__.gpsAlturaC.append(dataSplit[6])

                    # elif dataSplit[3] == "t":
                    #     __init__.altitudeP.append(dataSplit[7])
                    #     __init__.temperaturaP.append(dataSplit[8])
                    #     print("vetor temperatura paylod ", __init__.altitudeC)
                    #     __init__.voltageP.append(dataSplit[9])
                    #     __init__.giroscopioR.append(dataSplit[10])
                    #     __init__.giroscopioP.append(dataSplit[11])
                    #     __init__.giroscopioY.append(dataSplit[12])
                    #     __init__.acelerometroR.append(dataSplit[13])
                    #     __init__.acelerometroP.append(dataSplit[14])
                    #     __init__.acelerometroY.append(dataSplit[15])
                    #     __init__.magnetometroR.append(dataSplit[16])
                    #     __init__.magnetometroP.append(dataSplit[17])
                    #     __init__.magnetometroY.append(dataSplit[18])
                    #     print(dataSplit[18])
        finally:
            MSP.close()
            arquivoAltitudeC.write(str(self.getAltitudeC()))
            arquivoTemperaturaC.write(str(self.getTemperaturaC()))
            arquivoAltitudeC.close()
            arquivoTemperaturaC.close()

def segundo():
    time.sleep(1)
    return 1
    
if __name__ == '__main__':
    conetion= ConectionS()
    MSP= serial.Serial('/dev/ttyACM0', 9600, timeout=3)
    while 1:
        conetion.Captura(MSP)
    # #a cada 5 segundo o dataset de transição é carregado
    # cont= 0
    # tempo= segundo()
    # cont= tempo + cont
    # print(cont)
    # if((cont % 5) == 0):
    #     print('altitude',  ConectionS.altitudeC)
    #     ConectionS.carregaDataset(
    #         ConectionS.altitudeC,
    #         ConectionS.temperaturaC,
    #         ConectionS.voltageC,
    #         ConectionS.gpsLatitudeC,
    #         ConectionS.gpsLongitudeC,
    #         ConectionS.gpsAlturaC,
    #         ConectionS.altitudeP,
    #         ConectionS.temperaturaP,
    #         ConectionS.voltageP,
    #         ConectionS.giroscopioR,
    #         ConectionS.giroscopioP,
    #         ConectionS.giroscopioY,
    #         ConectionS.acelerometroR,
    #         ConectionS.acelerometroP,
    #         ConectionS.acelerometroY,
    #         ConectionS.magnetometroR,
    #         ConectionS.magnetometroP,
    #         ConectionS.magnetometroY
    #         )

        
            



