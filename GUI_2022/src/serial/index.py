# -*- coding: utf-8 -*-
import serial
import time
import pandas as pd
from utils import Path_txt
from conection import ConectionS


class serial:
    #MSP = serial.Serial('/dev/ttyACM0', 9600, timeout=3)
    
    def Captura(self, MSP):
        arquivoAltitudeC = open(Path_txt.ALTITUDEC, 'w')
        arquivoTemperaturaC = open(Path_txt.TEMPERATURAC, 'w')
        arquivoVoltageC= open(Path_txt.VOLTAGEC, 'w')
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
                        ConectionS.setAltitudeC(dataSplit[0])
                        ConectionS.setTemperaturaC(dataSplit[1])
                        ConectionS.setVoltageC(dataSplit[2])
                        ConectionS.setGpsLatitudeC(dataSplit[4])
                        ConectionS.setGpsLongitudeC(dataSplit[5])
                        ConectionS.setGpsAlturaC(dataSplit[6])
                    elif dataSplit[3] == "t":
                        ConectionS.setAltitudeP(dataSplit[7])
                        ConectionS.setTemperaturaP(dataSplit[8])
                        ConectionS.setVoltageP(dataSplit[9])
                        ConectionS.setGiroscopioR(dataSplit[10])
                        ConectionS.setGiroscopioP(dataSplit[11])
                        ConectionS.setGiroscopioY(dataSplit[12])
                        ConectionS.setAcelerometroR(dataSplit[13])
                        ConectionS.setAcelerometroP(dataSplit[14])
                        ConectionS.setAcelerometroY(dataSplit[15])
                        ConectionS.setMagnetometroR(dataSplit[16])
                        ConectionS.setMagnetometroP(dataSplit[17])
                        ConectionS.setMagnetometroY(dataSplit[18])
        finally:
            MSP.close()
            arquivoAltitudeC.write(str(ConectionS.getAltitudeC()))
            arquivoTemperaturaC.write(str(ConectionS.getTemperaturaC()))
            arquivoVoltageC.write(str(ConectionS.getVoltageC()))
            arquivoAltitudeC.close()
            arquivoTemperaturaC.close()
        
    # def filterVector(vetor):
    #     cont=0
    #     for(i in vetor):
    #         cont= cont + 1
    #         if(i == ''):
    #             #se a posição estiver vazia a mesma será ocupada pelo valor da posição anterior
    #             vetor[cont]= vetor[cont - 1]
    #     return vetor

#     def drop_database(df):
#             df.drop(columns=[
#                 'altitudeC',
#                 'temperaturaC',
#                 'voltageC',
#                 'gpsLatitudeC',
#                 'gpsLongitudeC',
#                 'gpsAlturaC',
#                 'altitudeP',
#                 'temperaturaP',
#                 'voltageP',
#                 'giroscopioR',
#                 'giroscopioP',
#                 'giroscopioY',
#                 'acelerometroR',
#                 'acelerometroP',
#                 'acelerometroY',
#                 'magnetometroR',
#                 'magnetometroP',
#                 'magnetometroY'])

#     def carregaDataset(
#         altitudeC,
#         temperaturaC,
#         voltageC,
#         gpsLatitudeC,
#         gpsLongitudeC,
#         gpsAlturaC,
#         altitudeP,
#         temperaturaP,
#         voltageP,
#         giroscopioR,
#         giroscopioP,
#         giroscopioY,
#         acelerometroR,
#         acelerometroP,
#         acelerometroY,
#         magnetometroR,
#         magnetometroP,
#         magnetometroY
#         ):

#             df= pd.read_csv('/home/wendel/Área de Trabalho/LtSat/GCS_2022/GUI_2022/datasets/transicao.csv', skiprows=1, sep=',', encoding="utf-8")
#             if (df):
#                 df['altitudeC']= altitudeC
#                 df['temperaturaC']= temperaturaC
#                 df['voltageC']= voltageC
#                 df['gpsLatitudeC']= gpsLatitudeC
#                 df['gpsLongitudeC']= gpsLongitudeC
#                 df['gpsAlturaC']= gpsAlturaC
#                 df['altitudeP']= altitudeP
#                 df['temperaturaP']= temperaturaP
#                 df['voltageP']= voltageP
#                 df['giroscopioR']= giroscopioR
#                 df['giroscopioP']= giroscopioP
#                 df['giroscopioY']= giroscopioY
#                 df['acelerometroR']= acelerometroR
#                 df['acelerometroP']= acelerometroP
#                 df['acelerometroY']= acelerometroY
#                 df['magnetometroR']= magnetometroR
#                 df['magnetometroP']= magnetometroP
#                 df['magnetometroY']= magnetometroY
#             else:
#                 print('Error')
                
                
#     def Captura(self, MSP): 
#         while MSP.bytesize > 0:
#             MSP.flushOutput()
#             MSP.flushInput()

# def segundo():
#     time.sleep(1)
#     return 1
    
# if __name__ == '__main__':
#     ConectionS()
#     #a cada 5 segundo o dataset de transição é carregado
#     cont= 0
#     tempo= segundo()
#     cont= tempo + cont
#     print(cont)
#     if((cont % 5) == 0):
#         print('altitude',  ConectionS.altitudeC)
#         ConectionS.carregaDataset(
#             ConectionS.altitudeC,
#             ConectionS.temperaturaC,
#             ConectionS.voltageC,
#             ConectionS.gpsLatitudeC,
#             ConectionS.gpsLongitudeC,
#             ConectionS.gpsAlturaC,
#             ConectionS.altitudeP,
#             ConectionS.temperaturaP,
#             ConectionS.voltageP,
#             ConectionS.giroscopioR,
#             ConectionS.giroscopioP,
#             ConectionS.giroscopioY,
#             ConectionS.acelerometroR,
#             ConectionS.acelerometroP,
#             ConectionS.acelerometroY,
#             ConectionS.magnetometroR,
#             ConectionS.magnetometroP,
#             ConectionS.magnetometroY
#             )

        