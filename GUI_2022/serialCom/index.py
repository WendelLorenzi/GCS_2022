# -*- coding: utf-8 -*-
import csv
from distutils.log import error
import serial
from conection import ConectionS
import pandas as pd

class SerialC:
    def unifyData(self, a, b, c, d, e, f, g, h, i, j, l, k, o, p, q, r, s, t, u):
        dfC = pd.read_csv('datasets\csvTransicao\light_1038_C.csv', skiprows=1)
        dfT = pd.read_csv('datasets\csvTransicao\flight_1038_T.csv', skiprows=1)
        dfC['TEMP'] = a
        dfC['VOLTAGE'] = b
        dfC['GPS_LATITUDE'] = c
        dfC['GPS_LONGITUDE'] = d
        dfC['GPS_ALTITUDE'] = f
        dfC['ALTITUDE'] = e
        dfT['TP_ALTITUDE'] = h
        dfT['TP_TEMP'] = i
        dfT['TP_VOLTAGE'] = j
        dfT['GYRO_R'] = l
        dfT['GYRO_P'] = k
        dfT['GYRO_Y'] = o
        dfT['ACCEL_R'] = p
        dfT['ACCEL_P'] = q
        dfT['ACCEL_Y'] = r
        dfT['MAG_R'] = s
        dfT['MAG_P'] = t
        dfT['MAG_Y'] = u
        dfT['PACKET_TYPE'] = g
        dfC['PACKET_TYPE'] = g
    
    def unloadVet(self, arquivo, ConectionS):
        arquivo = csv.writer(arquivo)
        for value in range(len(ConectionS)):
            arquivo.writerow([ConectionS[value]])
        return arquivo
        
    def carregaCsv(self, ConectionS):
        a = ConectionS.getTemperaturaC()
        b = ConectionS.getVoltageC()
        c = ConectionS.getGpsLatitudeC()
        d = ConectionS.getGpsLongitudeC()
        e = ConectionS.getAltitudeC()
        f = ConectionS.getGpsAlturaC()
        g = ConectionS.getPackegeType()
        h = ConectionS.getAltitudeP()
        i = ConectionS.getTemperaturaP()
        j = ConectionS.getVoltageP()
        l = ConectionS.getGiroscopioR()
        k = ConectionS.getGiroscopioP()
        o = ConectionS.getGiroscopioY()
        p = ConectionS.getAcelerometroR()
        q = ConectionS.getAcelerometroP()
        r = ConectionS.getAcelerometroY()
        s = ConectionS.getMagnetometroR()
        t = ConectionS.getMagnetometroP()
        u = ConectionS.getMagnetometroY()
        with open('datasets\csvTransicao\altitudeC.csv', 'w') as arquivoAltitudeC:
            arquivoAltitudeC = self.unloadVet(arquivoAltitudeC, e)
        with open('datasets\csvTransicao\temperaturaC.csv', 'w') as arquivoTemperaturaC:
            arquivoTemperaturaC = self.unloadVet(arquivoTemperaturaC, a)
        with open('datasets\csvTransicao\VoltageC.csv', 'w') as arquivoVoltageC:
            arquivoVoltageC = self.unloadVet(arquivoVoltageC, b)
        with open('datasets\csvTransicao\gpsLatitudeC.csv', 'w') as arquivoGpsLatitudeC:
            arquivoGpsLatitudeC = self.unloadVet(arquivoGpsLatitudeC, c)
        with open('datasets\csvTransicao\gpsLongitudeC.csv', 'w') as arquivoGpsLongitudeC:
            arquivoGpsLongitudeC = self.unloadVet(arquivoGpsLongitudeC, d)
        with open('datasets\csvTransicao\GpsAlturaC.csv', 'w') as arquivoGpsAlturaC:
            arquivoGpsAlturaC = self.unloadVet(arquivoGpsAlturaC, f)
        with open('datasets\csvTransicao\Counter.csv', 'w') as arquivoPackageType:
            arquivoPackageType = self.unloadVet(arquivoPackageType, g)
        with open('datasets\csvTransicao\AltitudeP.csv', 'w') as arquivoAltitudeP:
            arquivoAltitudeP = self.unloadVet(arquivoAltitudeP, h)
        with open('datasets\csvTransicao\TemperaturaP.csv', 'w') as arquivoTemperaturaP:
            arquivoTemperaturaP = self.unloadVet(arquivoTemperaturaP, i)
        with open('datasets\csvTransicao\VoltageP.csv', 'w') as arquivosetVoltageP:
            arquivosetVoltageP = self.unloadVet(arquivosetVoltageP, j)
        with open('datasets\csvTransicao\GiroscopioR.csv', 'w') as arquivoGiroscopioR:
            arquivoGiroscopioR = self.unloadVet(arquivoGiroscopioR, l)
        with open('datasets\csvTransicao\GiroscopioP.csv', 'w') as arquivoGiroscopioP:
            arquivoGiroscopioP = self.unloadVet(arquivoGiroscopioP, k)
        with open('datasets\csvTransicao\GiroscopioY.csv', 'w') as arquivoGiroscopioY:
            arquivoGiroscopioY = self.unloadVet(arquivoGiroscopioY, o)
        with open('datasets\csvTransicao\AcelerometroR.csv', 'w') as arquivoAcelerometroR:
            arquivoAcelerometroR = self.unloadVet(arquivoAcelerometroR, p)
        with open('datasets\csvTransicao\AcelerometroP.csv', 'w') as arquivoAcelerometroP:
            arquivoAcelerometroP = self.unloadVet(arquivoAcelerometroP, q)
        with open('datasets\csvTransicao\AcelerometroY.csv','w') as arquivoAcelerometroY:
            arquivoAcelerometroY = self.unloadVet(arquivoAcelerometroY, r)
        with open('datasets\csvTransicao\MagnetometroR.csv','w') as arquivoMagnetometroR:
            arquivoMagnetometroR = self.unloadVet(arquivoMagnetometroR, s)
        with open('datasets\csvTransicao\MagnetometroP.csv','w') as arquivoMagnetometroP:
            arquivoMagnetometroP = self.unloadVet(arquivoMagnetometroP, t)
        with open('datasets\csvTransicao\MagnetometroY.csv','w') as arquivoMagnetometroY:
            arquivoMagnetometroY = self.unloadVet(arquivoMagnetometroY, u)
        
        self.unifyData(self, a, b, c, d, e, f, g, h, i, j, l, o, q, r, s, t, u)
            
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