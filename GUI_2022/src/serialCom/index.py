# -*- coding: utf-8 -*-
import csv
from distutils.log import error
import serial
from enum import Enum

from conection import ConectionS

class File(Enum):
    ALTITUDEC = 'datasets/csvTransicao/altitudeC.csv'
    TEMPERATURAC = 'datasets/csvTransicao/TemperaturaC.csv'
    VOLTAGEC= 'datasets/csvTransicao/VoltageC.csv'
    GPSLATITUDE= 'datasets/csvTransicao/gpsLatitudeC.csv'
    GPSLONGITUDE= 'datasets/csvTransicao/gpsLongitudeC.csv'
    GPSALTURAC= 'datasets/csvTransicao/GpsAlturaC.csv'
    ALTITUDEP= 'datasets/csvTransicao/AltitudeP.csv'
    TEMPERATURAP= 'datasets/csvTransicao/TemperaturaP.csv'
    VOLTAGEP= 'datasets/csvTransicao/VoltageP.csv'
    GIROSCOPIOR= 'datasets/csvTransicao/GiroscopioR.csv'
    GIROSCOPIOP= 'datasets/csvTransicao/GiroscopioP.csv'
    GIROSCOPIOY= 'datasets/csvTransicao/GiroscopioY.csv'
    ACELEROMETROR= 'datasets/csvTransicao/AcelerometroR.csv'
    ACELEROMETROP= 'datasets/csvTransicao/AcelerometroP.csv'
    ACELEROMETROY= 'datasets/csvTransicao/AcelerometroY.csv'
    MAGNETOMETROR= 'datasets/csvTransicao/MagnetometroR.csv'
    MAGNETOMETROP= 'datasets/csvTransicao/MagnetometroP.csv'
    MAGNETOMETROY= 'datasets/csvTransicao/MagnetometroY.csv'
    PACKAGETYPE= 'datasets/csvTransicao/packageType.csv'


class SerialC:
    def unloadVet(self, arquivo, ConectionS):
        arquivo = csv.writer(arquivo)
        for value in range(len(ConectionS)):
            arquivo.writerow([ConectionS[value]])
        return arquivo
        
    def carregaCsv(self, ConectionS):
        print('chamou carrega csv')
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/altitudeC.csv', 'w') as arquivoAltitudeC:
            arquivoAltitudeC = self.unloadVet(arquivoAltitudeC, ConectionS.getAltitudeC())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/TemperaturaC.csv', 'w') as arquivoTemperaturaC:
            arquivoTemperaturaC = self.unloadVet(arquivoTemperaturaC, ConectionS.getTemperaturaC())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/VoltageC.csv', 'w') as arquivoVoltageC:
            arquivoVoltageC = self.unloadVet(arquivoVoltageC, ConectionS.getVoltageC())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/gpsLatitudeC.csv', 'w') as arquivoGpsLatitudeC:
            arquivoGpsLatitudeC = self.unloadVet(arquivoGpsLatitudeC, ConectionS.getGpsLatitudeC())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/gpsLongitudeC.csv', 'w') as arquivoGpsLongitudeC:
            arquivoGpsLongitudeC = self.unloadVet(arquivoGpsLongitudeC, ConectionS.getGpsLongitudeC())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/gpsLongitudeC.csv', 'w') as arquivoGpsAlturaC:
            arquivoGpsAlturaC = self.unloadVet(arquivoGpsAlturaC, ConectionS.getGpsAlturaC())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/packageType.csv', 'w') as arquivoPackageType:
            arquivoPackageType = self.unloadVet(arquivoPackageType, ConectionS.getPackegeType())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/GpsAlturaC.csv', 'w') as arquivoAltitudeP:
            arquivoAltitudeP = self.unloadVet(arquivoAltitudeP, ConectionS.getAltitudeP())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/TemperaturaP.csv', 'w') as arquivoTemperaturaP:
            arquivoTemperaturaP = self.unloadVet(arquivoTemperaturaP, ConectionS.getTemperaturaP())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/VoltageP.csv', 'w') as arquivosetVoltageP:
            arquivosetVoltageP = self.unloadVet(arquivosetVoltageP, ConectionS.getVoltageP())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/GiroscopioR.csv', 'w') as arquivoGiroscopioR:
            arquivoGiroscopioR = self.unloadVet(arquivoGiroscopioR, ConectionS.getGiroscopioR())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/GiroscopioP.csv', 'w') as arquivoGiroscopioP:
            arquivoGiroscopioP = self.unloadVet(arquivoGiroscopioP, ConectionS.getGiroscopioP())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/GiroscopioY.csv', 'w') as arquivoGiroscopioY:
            arquivoGiroscopioY = self.unloadVet(arquivoGiroscopioY, ConectionS.getGiroscopioY())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/AcelerometroR.csv', 'w') as arquivoAcelerometroR:
            arquivoAcelerometroR = self.unloadVet(arquivoAcelerometroR, ConectionS.getAcelerometroR())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/AcelerometroP.csv', 'w') as arquivoAcelerometroP:
            arquivoAcelerometroP = self.unloadVet(arquivoAcelerometroP, ConectionS.getAcelerometroP())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/AcelerometroY.csv','w') as arquivoAcelerometroY:
            arquivoAcelerometroY = self.unloadVet(arquivoAcelerometroY, ConectionS.getAcelerometroY())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/MagnetometroR.csv','w') as arquivoMagnetometroR:
            arquivoMagnetometroR = self.unloadVet(arquivoMagnetometroR, ConectionS.getMagnetometroR())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/MagnetometroP.csv','w') as arquivoMagnetometroP:
            arquivoMagnetometroP = self.unloadVet(arquivoMagnetometroP, ConectionS.getMagnetometroP())
        with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/MagnetometroY.csv','w') as arquivoMagnetometroY:
            arquivoMagnetometroY = self.unloadVet(arquivoMagnetometroY, ConectionS.getMagnetometroY())

        ConectionS.clear()
        
    def Captura(self, ConectionS, porta, stop=False):
        MSP = serial.Serial(str(porta), 9600, timeout=3)
        try:
            while True:
                MSP.flushOutput()
                MSP.flushInput()

                data = MSP.readline().decode()
                dataSplit= data.split(',')
                print(dataSplit)
                if (len(dataSplit) > 1 & stop != True):
                    if (dataSplit[3] == "c"):
                        ConectionS.setAltitudeC(dataSplit[0])
                        ConectionS.setTemperaturaC(dataSplit[1])
                        ConectionS.setVoltageC(dataSplit[2])
                        ConectionS.setPackagetType(dataSplit[3])
                        ConectionS.setGpsLatitudeC(dataSplit[4])
                        ConectionS.setGpsLongitudeC(dataSplit[5])
                        ConectionS.setGpsAlturaC(dataSplit[6])
                    elif (dataSplit[3] == "t"):
                        ConectionS.setAltitudeC(dataSplit[0])
                        ConectionS.setTemperaturaC(dataSplit[1])
                        ConectionS.setVoltageC(dataSplit[2])
                        ConectionS.setPackagetType(dataSplit[3])
                        ConectionS.setGpsLatitudeC(dataSplit[4])
                        ConectionS.setGpsLongitudeC(dataSplit[5])
                        ConectionS.setGpsAlturaC(dataSplit[6])
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
                    MSP.close()
                    self.carregaCsv(ConectionS)
        except:
            self.carregaCsv(ConectionS)
            
SerialC().Captura(ConectionS(), '/dev/ttyACM0')
            

