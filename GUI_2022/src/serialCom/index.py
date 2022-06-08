# -*- coding: utf-8 -*-
import csv
from distutils.log import error
import serial
from enum import Enum

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
        with open(str(File.ALTITUDEC.value), 'w') as arquivoAltitudeC:
            arquivoAltitudeC = self.unloadVet(arquivoAltitudeC, ConectionS.getAltitudeC())
        with open(str(File.TEMPERATURAC.value), 'w') as arquivoTemperaturaC:
            arquivoTemperaturaC = self.unloadVet(arquivoTemperaturaC, ConectionS.getTemperaturaC())
        with open(str(File.VOLTAGEC.value), 'w') as arquivoVoltageC:
            arquivoVoltageC = self.unloadVet(arquivoVoltageC, ConectionS.getVoltageC())
        with open(str(File.GPSLATITUDE.value), 'w') as arquivoGpsLatitudeC:
            arquivoGpsLatitudeC = self.unloadVet(arquivoGpsLatitudeC, ConectionS.getGpsLatitudeC())
        with open(str(File.GPSLONGITUDE.value), 'w') as arquivoGpsLongitudeC:
            arquivoGpsLongitudeC = self.unloadVet(arquivoGpsLongitudeC, ConectionS.getGpsLongitudeC())
        with open(str(File.GPSALTURAC.value), 'w') as arquivoGpsAlturaC:
            arquivoGpsAlturaC = self.unloadVet(arquivoGpsAlturaC, ConectionS.getGpsAlturaC())
        with open(str(File.ALTITUDEP.value), 'w') as arquivoAltitudeP:
            arquivoAltitudeP = self.unloadVet(arquivoAltitudeP, ConectionS.getAltitudeP())
        with open(str(File.TEMPERATURAP.value), 'w') as arquivoTemperaturaP:
            arquivoTemperaturaP = self.unloadVet(arquivoTemperaturaP, ConectionS.getTemperaturaP())
        with open(str(File.VOLTAGEP.value), 'w') as arquivosetVoltageP:
            arquivosetVoltageP = self.unloadVet(arquivosetVoltageP, ConectionS.getVoltageP())
        with open(str(File.GIROSCOPIOR.value), 'w') as arquivoGiroscopioR:
            arquivoGiroscopioR = self.unloadVet(arquivoGiroscopioR, ConectionS.getGiroscopioR())
        with open(str(File.GIROSCOPIOP.value), 'w') as arquivoGiroscopioP:
            arquivoGiroscopioP = self.unloadVet(arquivoGiroscopioP, ConectionS.getGiroscopioP())
        with open(str(File.GIROSCOPIOY.value), 'w') as arquivoGiroscopioY:
            arquivoGiroscopioY = self.unloadVet(arquivoGiroscopioY, ConectionS.getGiroscopioY())
        with open(str(File.ACELEROMETROR.value), 'w') as arquivoAcelerometroR:
            arquivoAcelerometroR = self.unloadVet(arquivoAcelerometroR, ConectionS.getAcelerometroR())
        with open(str(File.ACELEROMETROP.value), 'w') as arquivoAcelerometroP:
            arquivoAcelerometroP = self.unloadVet(arquivoAcelerometroP, ConectionS.getAcelerometroP())
        with open(str(File.ACELEROMETROY.value),'w') as arquivoAcelerometroY:
            arquivoAcelerometroY = self.unloadVet(arquivoAcelerometroY, ConectionS.getAcelerometroY())
        with open(str(File.MAGNETOMETROR.value),'w') as arquivoMagnetometroR:
            arquivoMagnetometroR = self.unloadVet(arquivoMagnetometroR, ConectionS.getMagnetometroR())
        with open(str(File.MAGNETOMETROP.value),'w') as arquivoMagnetometroP:
            arquivoMagnetometroP = self.unloadVet(arquivoMagnetometroP, ConectionS.getMagnetometroP())
        with open(str(File.MAGNETOMETROY.value),'w') as arquivoMagnetometroY:
            arquivoMagnetometroY = self.unloadVet(arquivoMagnetometroY, ConectionS.getMagnetometroY())
        with open(str(File.PACKAGETYPE.value), 'w') as arquivoPackageType:
            arquivoPackageType = self.unloadVet(arquivoPackageType, ConectionS.getPackegeType())
        
        ConectionS.clear()
        
    def Captura(self, ConectionS, porta, stop=False):
        print('chamou captura')
        MSP = serial.Serial(str(porta), 9600, timeout=3)
        try:
            while True:
                MSP.flushOutput()
                MSP.flushInput()

                data = MSP.readline().decode()
                dataSplit= data.split(',')
                print(dataSplit)
                if (len(dataSplit) > 1 & stop != True):
                    ConectionS.setPackagetType(dataSplit[3])
                    if (dataSplit[3] == "c"):
                        ConectionS.setAltitudeC(dataSplit[0])
                        ConectionS.setTemperaturaC(dataSplit[1])
                        ConectionS.setVoltageC(dataSplit[2])
                        ConectionS.setGpsLatitudeC(dataSplit[4])
                        ConectionS.setGpsLongitudeC(dataSplit[5])
                        ConectionS.setGpsAlturaC(dataSplit[6])
                    elif (dataSplit[3] == "t"):
                        ConectionS.setAltitudeC(dataSplit[0])
                        ConectionS.setTemperaturaC(dataSplit[1])
                        ConectionS.setVoltageC(dataSplit[2])
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
                    self.carregaCsv(ConectionS)
        except:
            print(error)
        finally:
            MSP.close()
            self.carregaCsv(ConectionS)
