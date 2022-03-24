# -*- coding: utf-8 -*-

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

def drop_database(df):
        df.drop(columns=[    'altitudeC','temperaturaC', 'voltageC',
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

    data = MSP.readline().decode('ascii')
    print(data)
    dataSplit= data.split(',')
    print(dataSplit)
    if len(dataSplit) > 1:
        if dataSplit[28] == "1":
            if dataSplit[3] == "c":
                altitudeC.append(dataSplit[6])
                temperaturaC.append(float(dataSplit[7]))
                voltageC.append(float(dataSplit[8]))
                gpsLatitudeC.append(float(dataSplit[10]))
                gpsLongitudeC.append(float(dataSplit[11]))
                gpsAlturaC.append(float(dataSplit[12]))

            elif dataSplit[3] == "t":
                altitudeP.append(dataSplit[16])
                temperaturaP.append(float(dataSplit[17]))
                voltageP.append(float(dataSplit[18]))
                giroscopioR.append(float(dataSplit[19]))
                giroscopioP.append(float(dataSplit[20]))
                giroscopioY.append(float(dataSplit[21]))
                acelerometroR.append(float(dataSplit[22]))
                acelerometroP.append(float(dataSplit[23]))
                acelerometroY.append(float(dataSplit[24]))
                magnetometroR.append(float(dataSplit[25]))
                magnetometroP.append(float(dataSplit[26]))
                magnetometroY.append(float(dataSplit[27]))

        # a cada 5 segundo o dataset de transição é carregado
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

        
            



