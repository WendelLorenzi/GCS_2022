# -*- coding: utf-8 -*-

class ConectionS:
    def __init__(self, altitudeC=[], temperaturaC=[], voltageC=[], gpsLatitudeC=[], gpsLongitudeC=[], gpsAlturaC=[], altitudeP= [], temperaturaP=[], voltageP=[], giroscopioR=[], giroscopioP=[], giroscopioY=[], acelerometroR=[], acelerometroP=[], acelerometroY=[], magnetometroR=[], magnetometroP=[], magnetometroY=[]):
        self.__altitudeC= altitudeC
        self.__temperaturaC= temperaturaC
        self.__voltageC= voltageC
        self.__gpsLatitudeC= gpsLatitudeC
        self.__gpsLongitudeC= gpsLongitudeC
        self.__gpsAlturaC= gpsAlturaC
        self.__altitudeP= altitudeP
        self.__temperaturaP= temperaturaP
        self.__voltageP= voltageP
        self.__giroscopioR= giroscopioR
        self.__giroscopioP= giroscopioP
        self.__giroscopioY= giroscopioY
        self.__acelerometroR= acelerometroR
        self.__acelerometroP= acelerometroP
        self.__acelerometroY= acelerometroY
        self.__magnetometroR= magnetometroR
        self.__magnetometroP= magnetometroP
        self.__magnetometroY= magnetometroY

    def setAltitudeC(self, altitudeC):
        self.__altitudeC.append(altitudeC)

    def setTemperaturaC(self, temperaturaC):
        self.__temperaturaC.append(temperaturaC)

    def setVoltageC(self, voltageC):
        self.__voltageC.append(voltageC)

    def setGpsLatitudeC(self, gpsLatitudeC):
        self.__gpsLatitudeC.append(gpsLatitudeC)

    def setGpsLongitudeC(self, gpsLongitudeC):
        self.__gpsLongitudeC.append(gpsLongitudeC)

    def setGpsAlturaC(self, gpsAlturaC):
        self.__gpsAlturaC.append(gpsAlturaC)

    def setAltitudeP(self, altitudeP):
        self.__altitudeP.append(altitudeP)

    def setTemperaturaP(self, temperaturaP):
        self.__temperaturaP.append(temperaturaP)
    
    def setVoltageP(self, voltageP):
        self.__voltageP.append(voltageP)
    
    def setGiroscopioR(self, giroscopioR):
        self.__giroscopioR.append(giroscopioR)
    
    def setGiroscopioP(self, giroscopioP):
        self.__giroscopioP.append(giroscopioP)
    
    def setGiroscopioY(self, giroscopioY):
        self.__giroscopioY.append(giroscopioY)
    
    def setAcelerometroR(self, acelerometroR):
        self.__acelerometroR.append(acelerometroR)

    def setAcelerometroP(self, acelerometroP):
        self.__acelerometroP.append(acelerometroP)
    
    def setAcelerometroY(self, acelerometroY):
        self.__acelerometroY.append(acelerometroY)
    
    def setMagnetometroR(self, magnetometroR):
        self.__magnetometroR.append(magnetometroR)
        
    def setMagnetometroP(self, magnetometroP):
        self.__magnetometroP.append(magnetometroP)

    def setMagnetometroY(self, magnetometroY):
        self.__magnetometroY.append(magnetometroY)
    
    def getAltitudeC(self):
        return self.__altitudeC

    def getTemperaturaC(self):
        return self.__temperaturaC

    def getVoltageC(self):
        return self.__voltageC

    def getGpsLatitudeC(self):
        return self.__gpsLatitudeC

    def getGpsLongitudeC(self):
        return self.__gpsLongitudeC

    def getGpsAlturaC(self):
        return self.__gpsAlturaC

    def getAltitudeP(self):
        return self.__altitudeP

    def getTemperaturaP(self):
        return self.__temperaturaP

    def getVoltageP(self):
        return self.__voltageP
    
    def getGiroscopioR(self):
        return self.__giroscopioR

    def getGiroscopioP(self):
        return self.__giroscopioP
    
    def getGiroscopioY(self):
        return self.__giroscopioY

    def getAcelerometroR(self):
        return self.__acelerometroR

    def getAcelerometroP(self):
        return self.__acelerometroP
    
    def getAcelerometroY(self):
        return self.__acelerometroY

    def getMagnetometroR(self):
        return self.__magnetometroR
    
    def getMagnetometroP(self):
        return self.__magnetometroP

    def getMagnetometroY(self):
        return self.__magnetometroY