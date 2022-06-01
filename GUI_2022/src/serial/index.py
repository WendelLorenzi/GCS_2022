# -*- coding: utf-8 -*-
import csv
from distutils.log import error
import serial
#from utils.pathArquivos import File
from conection import ConectionS


class serialC:
    def teste(self, arquivo, ConectionS):
        arquivo = csv.writer(arquivo)
        for value in range(len(ConectionS)):
            arquivo.writerow([ConectionS[value]])
        return arquivo
        
    def carregaCsv(self, ConectionS):
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/altitudeC.csv', 'w') as arquivoAltitudeC:
            arquivoAltitudeC = self.teste(arquivoAltitudeC, ConectionS.getTemperaturaC())
        # arquivoTemperaturaC = open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/temperaturaC.csv', 'w')
        # arquivoVoltageC= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/VoltageC.csv', 'w')
        # arquivoGpsLatitudeC= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/gpsLatitudeC.csv', 'w')
        # arquivoGpsLongitudeC= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/gpsLongitudeC.csv', 'w')
        # arquivoGpsAlturaC= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/GpsAlturaC.csv', 'w')
        # arquivoAltitudeP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/AltitudeP.csv', 'w')
        # arquivoTemperaturaP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/TemperaturaP.csv', 'w')
        # arquivosetVoltageP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/VoltageP.csv', 'w')
        # arquivoGiroscopioR= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/GiroscopioR.csv', 'w')
        # arquivoGiroscopioP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/GiroscopioP.csv', 'w')
        # arquivoGiroscopioY= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/GiroscopioY.csv', 'w')
        # arquivoAcelerometroR= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/AcelerometroR.csv', 'w')
        # arquivoAcelerometroP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/AcelerometroP.csv', 'w')
        # arquivoAcelerometroY= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/AcelerometroY.csv','w')
        # arquivoMagnetometroR= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/MagnetometroR.csv','w')
        # arquivoMagnetometroP= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/MagnetometroP.csv','w')
        # arquivoMagnetometroY= open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/MagnetometroY.csv','w')
        #arquivoAltitudeC = self.teste(arquivoAltitudeC, ConectionS.getAltitudeC())
            # arquivoTemperaturaC.write(str(ConectionS.getTemperaturaC()))
            # arquivoVoltageC.write(str(ConectionS.getVoltageC()))
            # arquivoGpsLatitudeC.write(str(ConectionS.getGpsLatitudeC()))
            # arquivoGpsLongitudeC.write(str(ConectionS.getGpsLongitudeC()))
            # arquivoGpsAlturaC.write(str(ConectionS.getGpsAlturaC()))
            # arquivoAltitudeP.write(str(ConectionS.getAltitudeP()))
            # arquivoTemperaturaP.write(str(ConectionS.getTemperaturaP()))
            # arquivosetVoltageP.write(str(ConectionS.getVoltageP()))
            # arquivoGiroscopioR.write(str(ConectionS.getGiroscopioR()))
            # arquivoGiroscopioP.write(str(ConectionS.getGiroscopioP()))
            # arquivoGiroscopioY.write(str(ConectionS.getGiroscopioY()))
            # arquivoAcelerometroR.write(str(ConectionS.getAcelerometroR()))
            # arquivoAcelerometroP.write(str(ConectionS.getAcelerometroP()))
            # arquivoAcelerometroY.write(str(ConectionS.getAcelerometroY()))
            # arquivoMagnetometroR.write(str(ConectionS.getMagnetometroR()))
            # arquivoMagnetometroP.write(str(ConectionS.getMagnetometroP()))
            # arquivoMagnetometroY.write(str(ConectionS.getMagnetometroY()))
            # arquivoAltitudeC.close()
            # arquivoTemperaturaC.close()
            # arquivoVoltageC.close()
            # arquivoGpsLongitudeC.close()
            # arquivoGpsAlturaC.close()
            # arquivoAltitudeP.close()
            # arquivoTemperaturaP.close()
            # arquivosetVoltageP.close()
            # arquivoGiroscopioR.close()
            # arquivoGiroscopioP.close()
            # arquivoGiroscopioY.close()
            # arquivoAcelerometroR.close()
            # arquivoAcelerometroP.close()
            # arquivoAcelerometroY.close()
            # arquivoMagnetometroR.close()
            # arquivoMagnetometroP.close()
            # arquivoMagnetometroY.close()
    def Captura(self, ConectionS, porta, stop=False):
        MSP = serial.Serial(str(porta), 9600, timeout=3)
        try:
            while MSP.bytesize > 0:
                MSP.flushOutput()
                MSP.flushInput()

                data = MSP.readline().decode()
                dataSplit= data.split(',')
                print(dataSplit)
                if (len(dataSplit) > 1 & stop != True):
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
                else:
                    self.carregaCsv(ConectionS)
        except:
            print(error)
        finally:
            MSP.close()
            self.carregaCsv(ConectionS)
    
if __name__ == '__main__':
    A= serialC()
    A.Captura(ConectionS(), '/dev/ttyACM0')