import pandas as pd
import numpy as np
#from src.utils.pathArquivos import File


class dataframe:
    def filter(self, df: pd) -> pd:
        df.replace('', np.nan, inplace=True)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        return df
    
    def unifyData(self, dfAltitudeC, dfTemperaturaC, dfVoltageC, gpsLatitudeCdf, dfGpsLongitudeCdf, dfAlturaCdf , dfAltitudePdf, dfTemperaturaP):
        dfC = pd.read_csv('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/flight_1038_C.csv', skiprows=1)
        dfT = pd.read_csv('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/flight_1038_T.csv', skiprows=1)
        dfC['TEMP'] = dfTemperaturaC.iloc[0:]
        dfC['VOLTAGE'] = dfVoltageC.iloc[0:]
        dfC['GPS_LATITUDE'] = gpsLatitudeCdf.iloc[0:]
        dfC['GPS_LONGITUDE'] = dfGpsLongitudeCdf.iloc[0:]
        dfC['GPS_ALTITUDE'] = dfAltitudeC.iloc[0:]
        dfC['ALTITUDE'] = dfAlturaCdf.iloc[0:]
        dfT['TP_ALTITUDE'] = dfAltitudePdf.iloc[0:]
        dfT['TP_TEMP'] = dfTemperaturaP.iloc[0:]
        dfT['TP_VOLTAGE']
        dfT['GYRO_R']
        dfT['GYRO_P']
        dfT['GYRO_Y']
        dfT['ACCEL_R']
        dfT['ACCEL_P']
        dfT['ACCEL_Y']
        dfT['MAG_R']
        dfT['MAG_P']
        dfT['MAG_Y']

    def getAltitudeCdf(self):
        dfAltitudeC = pd.read_csv(
            '/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/altitudeC.csv')
        dfFilter = self.filter(dfAltitudeC)
        return (dfFilter.iloc[0:].to_numpy())
        
    # def getTemperaturaCdf(self):
    #     dfTemperaturaC= pd.read_csv('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/temperaturaC.csv', sep=',', encoding="utf-8")
    #     try:
    #         dfTemperaturaC.to_records(index=False)
    #         print(dfTemperaturaC[0])
    #         return dfTemperaturaC[0]
    #     except:
    #         print('error')

    # def getVoltageCdf(self):
    #     dfVoltageC= pd.read_csv(File.VOLTAGEC, sep=',', encoding="utf-8")
    #     try:
    #         self.__voltageC= dfVoltageC[0]
    #         return self.__voltageC
    #     except:
    #         print(error)

    # def getGpsLatitudeCdf(self):
    #     gpsLatitudeCdf= pd.read_csv('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/gpsLatitudeC.csv', sep=',', encoding="utf-8")
    #     try:
    #         self.__gpsLatitudeC= gpsLatitudeCdf[0]
    #         return self.__gpsLatitudeC
    #     except:
    #         print(error)

    # def getGpsLongitudeCdf(self):
    #     dfGpsLongitudeCdf= pd.read_csv(File.GPSLONGITUDE, sep=',', encoding="utf-8")
    #     try:
    #         self.__gpsLongitudeC= dfGpsLongitudeCdf[0]
    #         return self.__gpsLongitudeC
    #     except:
    #         print(error)

    # def getGpsAlturaCdf(self):
    #     dfAlturaCdf= pd.read_csv(File.GPSALTURAC, sep=',', encoding="utf-8")
    #     try:
    #         self.__gpsAlturaC= dfAlturaCdf[0]
    #         return self.__gpsAlturaC
    #     except:
    #         print(error)

    # def getAltitudePdf(self):
    #     dfAltitudePdf= pd.read_csv(File.ALTITUDEP, sep=',', encoding="utf-8")
    #     try:
    #         self.__altitudeP= dfAltitudePdf[0]
    #         return self.__altitudeP
    #     except:
    #         print(error)

    # def getTemperaturaPdf(self):
    #     dfTemperaturaP= pd.read_csv(File.TEMPERATURAP, sep=',', encoding="utf-8")
    #     try:
    #         self.__temperaturaP= dfTemperaturaP[0]
    #         return self.__temperaturaP
    #     except:
    #         print(error)


# if __name__ == '__main__':
#     a = dataframe()
#     a.getAltitudeCdf()
#     # print(a.getTemperaturaCdf())
#     # print(serialC.getAltitudeC())
