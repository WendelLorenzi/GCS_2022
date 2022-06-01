import pandas as pd
import numpy as np
#from src.utils.pathArquivos import File

class dataframe:
    # def __init__(self, altitudeCdf, temperaturaCdf, voltageCdf, gpsLatitudeCdf, gpsLongitudeCdf, gpsAlturaCdf, altitudePdf, temperaturaPdf, voltagePdf, giroscopioRdf, giroscopioPdf, giroscopioYdf, acelerometroRdf, acelerometroPdf, acelerometroYdf, magnetometroRdf, magnetometroPdf, magnetometroYdf):
    #             self.__altitudeC= altitudeCdf
    #             self.__temperaturaC= temperaturaCdf
    #             self.__voltageC= voltageCdf
    #             self.__gpsLatitudeC= gpsLatitudeCdf
    #             self.__gpsLongitudeC= gpsLongitudeCdf
    #             self.__gpsAlturaC= gpsAlturaCdf
    #             self.__altitudeP= altitudePdf
    #             self.__temperaturaP= temperaturaPdf
    #             self.__voltageP= voltagePdf
    #             self.__giroscopioR= giroscopioRdf
    #             self.__giroscopioP= giroscopioPdf
    #             self.__giroscopioY= giroscopioYdf
    #             self.__acelerometroR= acelerometroRdf
    #             self.__acelerometroP= acelerometroPdf
    #             self.__acelerometroY= acelerometroYdf
    #             self.__magnetometroR= magnetometroRdf
    #             self.__magnetometroP= magnetometroPdf
    #             self.__magnetometroY= magnetometroYdf
    
    def filter(self, df: pd) -> pd:
        df.replace('', np.nan, inplace=True)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        return df
                
    def getAltitudeCdf(self):
        dfAltitudeC= pd.read_csv('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/txtTransicao/altitudeC.csv')
        dfFilter = self.filter(dfAltitudeC)
        #self.__altitudeC= dfAltitudeC[0].values.tolist()
        #dfAltitudeC.to_records(index=False)
        #dfAltitudeC.to_dict('records')
        #print(dfAltitudeC.iloc[0].to_list())
        #aux = eval(str(dfFilter.iloc[0].to_numpy()).lstrip('["').rstrip('"]'))
        print(dfAltitudeC[0].to_numpy(dtype ='float32'))
        #return set(dfFilter[1:])
    
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
    
if __name__ == '__main__':
    a = dataframe()
    a.getAltitudeCdf()
    print()
    #print(a.getTemperaturaCdf())
    #print(serialC.getAltitudeC())
    