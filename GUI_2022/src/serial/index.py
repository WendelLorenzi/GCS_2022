# -*- coding: utf-8 -*-
import serial
from Path_txt import Txt
from conection import ConectionS


class serialC:  
        def Captura(self, ConectionS, porta):
            MSP = serial.Serial(str(porta), 9600, timeout=3)
            arquivoAltitudeC = open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/altitudeC.csv', 'w')
            arquivoTemperaturaC = open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/temperaturaC.csv', 'w')
            arquivoVoltageC= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/VoltageC.csv', 'w')
            arquivoGpsLatitudeC= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/gpsLatitudeC.csv', 'w')
            arquivoGpsLongitudeC= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/gpsLongitudeC.csv', 'w')
            arquivoGpsAlturaC= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/GpsAlturaC.csv', 'w')
            arquivoAltitudeP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/AltitudeP.csv', 'w')
            arquivoTemperaturaP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/TemperaturaP.csv', 'w')
            arquivosetVoltageP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/VoltageP.csv', 'w')
            arquivoGiroscopioR= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/GiroscopioR.csv', 'w')
            arquivoGiroscopioP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/GiroscopioP.csv', 'w')
            arquivoGiroscopioY= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/GiroscopioY.csv', 'w')
            arquivoAcelerometroR= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/AcelerometroR.csv', 'w')
            arquivoAcelerometroP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/AcelerometroP.csv', 'w')
            arquivoAcelerometroY= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/AcelerometroY.csv','w')
            arquivoMagnetometroR= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/MagnetometroR.csv','w')
            arquivoMagnetometroP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/MagnetometroP.csv','w')
            arquivoMagnetometroY= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/MagnetometroY.csv','w')
            try:
                while MSP.bytesize > 0:
                    MSP.flushOutput()
                    MSP.flushInput()

                    data = MSP.readline().decode()
                    dataSplit= data.split(',')
                    print(dataSplit)
                    if len(dataSplit) > 1:
                        #filterVector(dataSplit)
                        if (dataSplit[3] == "c"):
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
                arquivoGpsLatitudeC.write(str(ConectionS.getGpsLatitudeC()))
                arquivoGpsLongitudeC.write(str(ConectionS.getGpsLongitudeC()))
                arquivoGpsAlturaC.write(str(ConectionS.getGpsAlturaC()))
                arquivoAltitudeP.write(str(ConectionS.getAltitudeP()))
                arquivoTemperaturaP.write(str(ConectionS.getTemperaturaP()))
                arquivosetVoltageP.write(str(ConectionS.getVoltageP()))
                arquivoGiroscopioR.write(str(ConectionS.getGiroscopioR()))
                arquivoGiroscopioP.write(str(ConectionS.getGiroscopioP()))
                arquivoGiroscopioY.write(str(ConectionS.getGiroscopioY()))
                arquivoAcelerometroR.write(str(ConectionS.getAcelerometroR()))
                arquivoAcelerometroP.write(str(ConectionS.getAcelerometroP()))
                arquivoAcelerometroY.write(str(ConectionS.getAcelerometroY()))
                arquivoMagnetometroR.write(str(ConectionS.getMagnetometroR()))
                arquivoMagnetometroP.write(str(ConectionS.getMagnetometroP()))
                arquivoMagnetometroY.write(str(ConectionS.getMagnetometroY()))
                arquivoAltitudeC.close()
                arquivoTemperaturaC.close()
                arquivoVoltageC.close()
                arquivoGpsLongitudeC.close()
                arquivoGpsAlturaC.close()
                arquivoAltitudeP.close()
                arquivoTemperaturaP.close()
                arquivosetVoltageP.close()
                arquivoGiroscopioR.close()
                arquivoGiroscopioP.close()
                arquivoGiroscopioY.close()
                arquivoAcelerometroR.close()
                arquivoAcelerometroP.close()
                arquivoAcelerometroY.close()
                arquivoMagnetometroR.close()
                arquivoMagnetometroP.close()
                arquivoMagnetometroY.close()

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

# def segundo():
#     time.sleep(1)
#     return 1
    
if __name__ == '__main__':
    A= serialC()
    A.Captura(ConectionS(), '/dev/ttyACM0')
    #print(serialC.getAltitudeC())