# -*- coding: utf-8 -*-
import serial
import matplotlib.pyplot as plt
import time
import pandas as pd

class ConectionS:
    def __init__(self, altitudeC=[],
                 temperaturaC=[],
                 voltageC=[],
                 gpsLatitudeC=[],
                 gpsLongitudeC=[],
                 gpsAlturaC=[],
                 altitudeP= [],
                 temperaturaP=[],
                 voltageP=[],
                 giroscopioR=[],
                 giroscopioP=[],
                 giroscopioY=[],
                 acelerometroR=[],
                 acelerometroP=[],
                 acelerometroY=[],
                 magnetometroR=[],
                 magnetometroP=[],
                 magnetometroY=[]
                 ):
                    self.altitudeC= altitudeC
                    self.temperaturaC= temperaturaC
                    self.voltageC= voltageC
                    self.gpsLatitudeC= gpsLatitudeC
                    self.gpsLongitudeC= gpsLongitudeC
                    self.gpsAlturaC= gpsAlturaC
                    self.altitudeP= altitudeP
                    self.temperaturaP= temperaturaP
                    self.voltageP= voltageP
                    self.giroscopioR= giroscopioR
                    self.giroscopioP= giroscopioP
                    self.giroscopioY= giroscopioY
                    self.acelerometroR= acelerometroR
                    self.acelerometroP= acelerometroP
                    self.acelerometroY= acelerometroY
                    self.magnetometroR= magnetometroR
                    self.magnetometroP= magnetometroP
                    self.magnetometroY= magnetometroY

    MSP = serial.Serial('/dev/ttyACM0', 9600, timeout=3)
        
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
        altitudeC,
        temperaturaC,
        voltageC,
        gpsLatitudeC,
        gpsLongitudeC,
        gpsAlturaC,
        altitudeP,
        temperaturaP,
        voltageP,
        giroscopioR,
        giroscopioP,
        giroscopioY,
        acelerometroR,
        acelerometroP,
        acelerometroY,
        magnetometroR,
        magnetometroP,
        magnetometroY
        ):

            df= pd.read_csv('/home/wendel/Área de Trabalho/LtSat/GCS_2022/GUI_2022/datasets/transicao.csv', skiprows=1, sep=',', encoding="utf-8")
            if (df):
                df['altitudeC']= altitudeC
                df['temperaturaC']= temperaturaC
                df['voltageC']= voltageC
                df['gpsLatitudeC']= gpsLatitudeC
                df['gpsLongitudeC']= gpsLongitudeC
                df['gpsAlturaC']= gpsAlturaC
                df['altitudeP']= altitudeP
                df['temperaturaP']= temperaturaP
                df['voltageP']= voltageP
                df['giroscopioR']= giroscopioR
                df['giroscopioP']= giroscopioP
                df['giroscopioY']= giroscopioY
                df['acelerometroR']= acelerometroR
                df['acelerometroP']= acelerometroP
                df['acelerometroY']= acelerometroY
                df['magnetometroR']= magnetometroR
                df['magnetometroP']= magnetometroP
                df['magnetometroY']= magnetometroY
            else:
                print('Error')
    
    while MSP.bytesize > 0:
        MSP.flushOutput()
        MSP.flushInput()

        data = MSP.readline().decode()
        dataSplit= data.split(',')
        print(dataSplit)
        if len(dataSplit) > 1:
            #filterVector(dataSplit)
            if dataSplit[3] == "c":
                __init__.altitudeC.append(dataSplit[0])
                print("vetor altitude container", __init__.altitudeC)
                __init__.temperaturaC.append(dataSplit[1])
                __init__.voltageC.append(dataSplit[2])
                __init__.gpsLatitudeC.append(dataSplit[4])
                __init__.gpsLongitudeC.append(dataSplit[5])
                __init__.gpsAlturaC.append(dataSplit[6])

            elif dataSplit[3] == "t":
                __init__.altitudeP.append(dataSplit[7])
                __init__.temperaturaP.append(dataSplit[8])
                print("vetor temperatura paylod ", __init__.altitudeC)
                __init__.voltageP.append(dataSplit[9])
                __init__.giroscopioR.append(dataSplit[10])
                __init__.giroscopioP.append(dataSplit[11])
                __init__.giroscopioY.append(dataSplit[12])
                __init__.acelerometroR.append(dataSplit[13])
                __init__.acelerometroP.append(dataSplit[14])
                __init__.acelerometroY.append(dataSplit[15])
                __init__.magnetometroR.append(dataSplit[16])
                __init__.magnetometroP.append(dataSplit[17])
                __init__.magnetometroY.append(dataSplit[18])
                print(dataSplit[18])

def segundo():
    time.sleep(1)
    return 1
    
if __name__ == '__main__':
    ConectionS()
    #a cada 5 segundo o dataset de transição é carregado
    cont= 0
    tempo= segundo()
    cont= tempo + cont
    print(cont)
    if((cont % 5) == 0):
        print('altitude',  ConectionS.altitudeC)
        ConectionS.carregaDataset(
            ConectionS.altitudeC,
            ConectionS.temperaturaC,
            ConectionS.voltageC,
            ConectionS.gpsLatitudeC,
            ConectionS.gpsLongitudeC,
            ConectionS.gpsAlturaC,
            ConectionS.altitudeP,
            ConectionS.temperaturaP,
            ConectionS.voltageP,
            ConectionS.giroscopioR,
            ConectionS.giroscopioP,
            ConectionS.giroscopioY,
            ConectionS.acelerometroR,
            ConectionS.acelerometroP,
            ConectionS.acelerometroY,
            ConectionS.magnetometroR,
            ConectionS.magnetometroP,
            ConectionS.magnetometroY
            )

        
            



