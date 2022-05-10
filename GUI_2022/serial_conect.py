# # -*- coding: utf-8 -*-
# import serial
# import matplotlib.pyplot as plt
# import time
# import pandas as pd
# from utils import Path_txt

        
#     # def filterVector(vetor):
#     #     cont=0
#     #     for(i in vetor):
#     #         cont= cont + 1
#     #         if(i == ''):
#     #             #se a posição estiver vazia a mesma será ocupada pelo valor da posição anterior
#     #             vetor[cont]= vetor[cont - 1]
#     #     return vetor

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
                
#     def segundo():
#         time.sleep(1)
#         return 1
            
            



