import pandas as pd
import numpy as np
from src.serialCom.index import File


class dataframe:
    def filter(self, df: pd) -> pd:
        df.replace('', np.nan, inplace=True)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        return df
    
    def unifyData(self):
        dfC = pd.read_csv('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/flight_1038_C.csv', skiprows=1)
        dfT = pd.read_csv('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/flight_1038_T.csv', skiprows=1)
        dfC['TEMP'] = self.getTemperaturaCdf()
        dfC['VOLTAGE'] = self.getVoltageCdf()
        dfC['GPS_LATITUDE'] = self.getAltitudeCdf()
        dfC['GPS_LONGITUDE'] = self.getGpsLongitudeCdf()
        dfC['GPS_ALTITUDE'] = self.getAltitudeCdf()
        dfC['ALTITUDE'] = self.getAltitudeCdf()
        dfT['TP_ALTITUDE'] = self.getAltitudePdf()
        dfT['TP_TEMP'] = self.getTemperaturaPdf()
        dfT['TP_VOLTAGE'] = self.getVoltageP()
        dfT['GYRO_R'] = self.getGiroscopioR()
        dfT['GYRO_P'] = self.getGiroscopioP()
        dfT['GYRO_Y'] = self.getGiroscopioY()
        dfT['ACCEL_R'] = self.getAcelerometroR()
        dfT['ACCEL_P'] = self.getAcelerometroP()
        dfT['ACCEL_Y'] = self.getAcelerometroY()
        dfT['MAG_R'] = self.getMagnetometroR()
        dfT['MAG_P'] = self.getAcelerometroP()
        dfT['MAG_Y'] = self.getMagnetometroY()
        dfT['PACKET_TYPE'] = self.getPakageType()
        dfC['PACKET_TYPE'] = self.getPakageType()
        dfT['PACKET_COUNT'].set_index('PACKET_TYPE') 
        dfC['PACKET_COUNT'].set_index('PACKET_TYPE')

    def getAltitudeCdf(self):
        dfAltitudeC = pd.read_csv(str(File.ALTITUDEC))
        dfFilter = self.filter(dfAltitudeC)
        return (dfFilter.iloc[0:].to_numpy())
        
    def getTemperaturaCdf(self):
        dfTemperaturaC= pd.read_csv(str(File.TEMPERATURAC))
        dfFilter = self.filter(dfTemperaturaC)
        return (dfFilter.iloc[0:].to_numpy())

    def getVoltageCdf(self):
        dfVoltageC= pd.read_csv(str(File.VOLTAGEC))
        dfFilter = self.filter(dfVoltageC)
        return (dfFilter.iloc[0:].to_numpy())

    def getGpsLatitudeCdf(self):
        gpsLatitudeCdf= pd.read_csv(str(File.GPSLATITUDE))
        dfFilter = self.filter(gpsLatitudeCdf)
        return (dfFilter.iloc[0:].to_numpy())

    def getGpsLongitudeCdf(self):
        dfGpsLongitudeCdf= pd.read_csv(str(File.GPSLONGITUDE))
        dfFilter = self.filter(dfGpsLongitudeCdf)
        return (dfFilter.iloc[0:].to_numpy())

    def getGpsAlturaCdf(self):
        dfAlturaCdf= pd.read_csv(str(File.GPSALTURAC))
        dfFilter = self.filter(dfAlturaCdf)
        return (dfFilter.iloc[0:].to_numpy())

    def getAltitudePdf(self):
        dfAltitudePdf= pd.read_csv(str(File.ALTITUDEP))
        dfFilter = self.filter(dfAltitudePdf)
        return (dfFilter.iloc[0:].to_numpy())

    def getTemperaturaPdf(self):
        dfTemperaturaP= pd.read_csv(str(File.TEMPERATURAP))
        dfFilter = self.filter(dfTemperaturaP)
        return (dfFilter.iloc[0:].to_numpy())

    def getVoltageP(self):
        dfVoltageP = pd.read_csv(str(File.VOLTAGEP))
        dfFilter = self.filter(dfVoltageP)
        return (dfFilter.iloc[0:].to_numpy())

    def getGiroscopioR(self):
        dfGiroscopioR= pd.read_csv(str(File.GIROSCOPIOR))
        dfFilter = self.filter(dfGiroscopioR)
        return (dfFilter.iloc[0:].to_numpy())

    def getGiroscopioP(self):
        dfGiroscopioP=  pd.read_csv(str(File.GIROSCOPIOP))
        dfFilter = self.filter(dfGiroscopioP)
        return (dfFilter.iloc[0:].to_numpy())
    
    def getGiroscopioY(self):
        dfGiroscopioY= pd.read_csv(str(File.GIROSCOPIOY))
        dfFilter = self.filter(dfGiroscopioY)
        return (dfFilter.iloc[0:].to_numpy())
    
    def getAcelerometroR(self):
        dfAcelerometroR= pd.read_csv(str(File.ACELEROMETROR))
        dfFilter = self.filter(dfAcelerometroR)
        return (dfFilter.iloc[0:].to_numpy())

    def getAcelerometroP(self):
        dfAcelerometroP= pd.read_csv(str(File.ACELEROMETROP))
        dfFilter = self.filter(dfAcelerometroP)
        return (dfFilter.iloc[0:].to_numpy())
    
    def getAcelerometroY(self):
        dfAcelerometroY= pd.read_csv(str(File.ACELEROMETROY))
        dfFilter = self.filter(dfAcelerometroY)
        return (dfFilter.iloc[0:].to_numpy())

    def getMagnetometroR(self):
        dfMagnetometroR = pd.read_csv(str(File.MAGNETOMETROR))
        dfFilter = self.filter(dfMagnetometroR)
        return (dfFilter.iloc[0:].to_numpy())

    def getMagnetometroP(self):
        dfMagnetometroP = pd.read_csv(str(File.MAGNETOMETROP))
        dfFilter = self.filter(dfMagnetometroP)
        return (dfFilter.iloc[0:].to_numpy())

    def getMagnetometroY(self):
        dfMagnetometroY = pd.read_csv(str(File.MAGNETOMETROY))
        dfFilter = self.filter(dfMagnetometroY)
        return (dfFilter.iloc[0:].to_numpy())
    
    def getPakageType(self):
        dfPackageType = pd.read_csv(str(File.PACKAGETYPE))
        dfFilter = self.filter(dfPackageType)
        return (dfFilter.iloc[0:].to_numpy())
