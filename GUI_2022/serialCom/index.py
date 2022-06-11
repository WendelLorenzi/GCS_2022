# -*- coding: utf-8 -*-
import csv
from distutils.log import error
import serial
from conection import ConectionS

class SerialC:
    def unloadVet(self, arquivo, ConectionS):
        arquivo = csv.writer(arquivo)
        for value in range(len(ConectionS)):
            arquivo.writerow([ConectionS[value]])
        return arquivo
        
    def carregaCsv(self, ConectionS):
        with open('datasets\csvTransicao\altitudeC.csv', 'w') as arquivoAltitudeC:
            arquivoAltitudeC = self.unloadVet(arquivoAltitudeC, ConectionS.getAltitudeC())
        with open('datasets\csvTransicao\temperaturaC.csv', 'w') as arquivoTemperaturaC:
            arquivoTemperaturaC = self.unloadVet(arquivoTemperaturaC, ConectionS.getTemperaturaC())
        with open('datasets\csvTransicao\VoltageC.csv', 'w') as arquivoVoltageC:
            arquivoVoltageC = self.unloadVet(arquivoVoltageC, ConectionS.getVoltageC())
        with open('datasets\csvTransicao\gpsLatitudeC.csv', 'w') as arquivoGpsLatitudeC:
            arquivoGpsLatitudeC = self.unloadVet(arquivoGpsLatitudeC, ConectionS.getGpsLatitudeC())
        with open('datasets\csvTransicao\gpsLongitudeC.csv', 'w') as arquivoGpsLongitudeC:
            arquivoGpsLongitudeC = self.unloadVet(arquivoGpsLongitudeC, ConectionS.getGpsLongitudeC())
        with open('datasets\csvTransicao\GpsAlturaC.csv', 'w') as arquivoGpsAlturaC:
            arquivoGpsAlturaC = self.unloadVet(arquivoGpsAlturaC, ConectionS.getGpsAlturaC())
        with open('datasets\csvTransicao\Counter.csv', 'w') as arquivoPackageType:
            arquivoPackageType = self.unloadVet(arquivoPackageType, ConectionS.getPackegeType())
        with open('datasets\csvTransicao\AltitudeP.csv', 'w') as arquivoAltitudeP:
            arquivoAltitudeP = self.unloadVet(arquivoAltitudeP, ConectionS.getAltitudeP())
        with open('datasets\csvTransicao\TemperaturaP.csv', 'w') as arquivoTemperaturaP:
            arquivoTemperaturaP = self.unloadVet(arquivoTemperaturaP, ConectionS.getTemperaturaP())
        with open('datasets\csvTransicao\VoltageP.csv', 'w') as arquivosetVoltageP:
            arquivosetVoltageP = self.unloadVet(arquivosetVoltageP, ConectionS.getVoltageP())
        with open('datasets\csvTransicao\GiroscopioR.csv', 'w') as arquivoGiroscopioR:
            arquivoGiroscopioR = self.unloadVet(arquivoGiroscopioR, ConectionS.getGiroscopioR())
        with open('datasets\csvTransicao\GiroscopioP.csv', 'w') as arquivoGiroscopioP:
            arquivoGiroscopioP = self.unloadVet(arquivoGiroscopioP, ConectionS.getGiroscopioP())
        with open('datasets\csvTransicao\GiroscopioY.csv', 'w') as arquivoGiroscopioY:
            arquivoGiroscopioY = self.unloadVet(arquivoGiroscopioY, ConectionS.getGiroscopioY())
        with open('datasets\csvTransicao\AcelerometroR.csv', 'w') as arquivoAcelerometroR:
            arquivoAcelerometroR = self.unloadVet(arquivoAcelerometroR, ConectionS.getAcelerometroR())
        with open('datasets\csvTransicao\AcelerometroP.csv', 'w') as arquivoAcelerometroP:
            arquivoAcelerometroP = self.unloadVet(arquivoAcelerometroP, ConectionS.getAcelerometroP())
        with open('datasets\csvTransicao\AcelerometroY.csv','w') as arquivoAcelerometroY:
            arquivoAcelerometroY = self.unloadVet(arquivoAcelerometroY, ConectionS.getAcelerometroY())
        with open('datasets\csvTransicao\MagnetometroR.csv','w') as arquivoMagnetometroR:
            arquivoMagnetometroR = self.unloadVet(arquivoMagnetometroR, ConectionS.getMagnetometroR())
        with open('datasets\csvTransicao\MagnetometroP.csv','w') as arquivoMagnetometroP:
            arquivoMagnetometroP = self.unloadVet(arquivoMagnetometroP, ConectionS.getMagnetometroP())
        with open('datasets\csvTransicao\MagnetometroY.csv','w') as arquivoMagnetometroY:
            arquivoMagnetometroY = self.unloadVet(arquivoMagnetometroY, ConectionS.getMagnetometroY())
            
        ConectionS.clear()

    def Captura(self, ConectionS, porta):
        MSP = serial.Serial(str(porta), 9600, timeout=3)
        try:
            while True:
                MSP.flushOutput()
                MSP.flushInput()

                data = MSP.readline().decode()
                dataSplit = data.split(',')
                print(dataSplit)
                if (len(dataSplit) > 1):
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
            
SerialC().Captura(ConectionS(), 'com3')
            
#  LISTA DE ATRIBUTOS E POSIÇÃO NO VETOR SERIAL   
# posição 0: Altitude Container
# posição 1: Temperatura Container
# posição 2: Voltage Container
# posição 3: pakage type
# posição 4: Gps Latitude Container
# posição 5: Gps Longitude Container
# posição 6: Gps Altura Container
# posição 7: Altitude Payload
# posição 8: Temperatura Payload
# posição 9: Voltage Payload
# posição 10: GiroscopioR
# posição 11: GiroscopioP
# posição 12: GiroscopioY
# posição 13: AcelerometroR
# posição 14: AcelerometroP
# posição 15: AcelerometroY
# posição 16: MagnetometroR
# posição 17: MagnetometroP
# posição 18: MagnetometroY