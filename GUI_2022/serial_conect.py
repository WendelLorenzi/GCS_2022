# -*- coding: utf-8 -*-

from numpy import vectorize
import serial
import matplotlib.pyplot as plt
import time
import pandas as pd


MSP = serial.Serial('/dev/ttyACM0', 9600, timeout=3)

#declando variaveis a serem plotadas
altitudeC= []
temperaturaC= []
voltageC= []
gpsLatitudeC= []
gpsLongitudeC= []
gpsAlturaC= []
voltageC= []
altitudeP= []
temperaturaP= []
voltageP= []
giroscopioR= []
giroscopioP= []
giroscopioY= []
acelerometroR= []
acelerometroP= []
acelerometroY= []
magnetometroR= []
magnetometroP= []
magnetometroY= []

def segundo():
    time.sleep(1)
    return 1
    
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

        df= pd.read_csv('/home/wendel/Área de Trabalho/LtSat/GCS_2022/GUI_2022/datasets/transicao.csv', skiprows=1)
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

cont= 0
while MSP.bytesize > 0:
    MSP.flushOutput()
    MSP.flushInput()

    data = MSP.readline().decode()
    dataSplit= data.split(',')
    print(dataSplit)
    if len(dataSplit) > 1:
        #filterVector(dataSplit)
        if dataSplit[3] == "c":
            altitudeC.append(dataSplit[0])
            print("vetor altitude container", altitudeC)
            temperaturaC.append(float(dataSplit[1]))
            voltageC.append(float(dataSplit[2]))
            gpsLatitudeC.append(float(dataSplit[4]))
            gpsLongitudeC.append(float(dataSplit[5]))
            gpsAlturaC.append(float(dataSplit[6]))

        elif dataSplit[3] == "t":
            altitudeP.append(dataSplit[7])
            temperaturaP.append(float(dataSplit[8]))
            print("vetor temperatura paylod ", altitudeC)
            voltageP.append(float(dataSplit[9]))
            giroscopioR.append(float(dataSplit[10]))
            giroscopioP.append(float(dataSplit[11]))
            giroscopioY.append(float(dataSplit[12]))
            acelerometroR.append(float(dataSplit[13]))
            acelerometroP.append(float(dataSplit[14]))
            acelerometroY.append(float(dataSplit[15]))
            magnetometroR.append(float(dataSplit[16]))
            magnetometroP.append(float(dataSplit[17]))
            magnetometroY.append(float(dataSplit[18]))

        #a cada 5 segundo o dataset de transição é carregado
        tempo= segundo()
        cont= tempo + cont
        if((cont % 5) == 0):
            print('altitude', 'temp', 'tensao', altitudeC, temperaturaC, voltageC)
            carregaDataset(
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
                )

        
            



