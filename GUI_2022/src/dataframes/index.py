from distutils.log import error
import pandas as pd
from utils.pathArquivos import File

class dataframe:
    def __init__(self, altitudeCdf, temperaturaCdf, voltageCdf, gpsLatitudeCdf, gpsLongitudeCdf, gpsAlturaCdf, altitudePdf, temperaturaPdf, voltagePdf, giroscopioRdf, giroscopioPdf, giroscopioYdf, acelerometroRdf, acelerometroPdf, acelerometroYdf, magnetometroRdf, magnetometroPdf, magnetometroYdf):
                self.__altitudeC= altitudeCdf
                self.__temperaturaC= temperaturaCdf
                self.__voltageC= voltageCdf
                self.__gpsLatitudeC= gpsLatitudeCdf
                self.__gpsLongitudeC= gpsLongitudeCdf
                self.__gpsAlturaC= gpsAlturaCdf
                self.__altitudeP= altitudePdf
                self.__temperaturaP= temperaturaPdf
                self.__voltageP= voltagePdf
                self.__giroscopioR= giroscopioRdf
                self.__giroscopioP= giroscopioPdf
                self.__giroscopioY= giroscopioYdf
                self.__acelerometroR= acelerometroRdf
                self.__acelerometroP= acelerometroPdf
                self.__acelerometroY= acelerometroYdf
                self.__magnetometroR= magnetometroRdf
                self.__magnetometroP= magnetometroPdf
                self.__magnetometroY= magnetometroYdf
                
    def getAltitudeCdf(self):
        dfAltitudeC= pd.read_csv(File.ALTITUDEC, sep=',', encoding="utf-8")
        try:
            self.__altitudeCdf= dfAltitudeC[0]
            return self.__altitudeCdf
        except:
            print(error)
    
    def getTemperaturaCdf(self):
        dfTemperaturaC= pd.read_csv(File.TEMPERATURAC, sep=',', encoding="utf-8")
        try:
            self.__temperaturaC= dfTemperaturaC[0]
            return self.__temperaturaC
        except:
            print(error)
    
    def getVoltageCdf(self):
        dfVoltageC= pd.read_csv(File.VOLTAGEC, sep=',', encoding="utf-8")
        try:
            self.__voltageC= dfVoltageC[0]
            return self.__voltageC
        except:
            print(error)
    
    def getGpsLatitudeCdf(self):
        gpsLatitudeCdf= pd.read_csv(File.GPSLATITUDE, sep=',', encoding="utf-8")
        try:
            self.__gpsLatitudeC= gpsLatitudeCdf[0]
            return self.__gpsLatitudeC
        except:
            print(error)
    
    def getGpsLongitudeCdf(self):
        dfGpsLongitudeCdf= pd.read_csv(File.GPSLONGITUDE, sep=',', encoding="utf-8")
        try:
            self.__gpsLongitudeC= dfGpsLongitudeCdf[0]
            return self.__gpsLongitudeC
        except:
            print(error)
    
    