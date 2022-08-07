# -*- coding: utf-8 -*-

import pandas as pd

class Gera_dataset:
    def __init__(self, ct, pay):
        self.container= ct
        self.payload= pay
        print(self.carrega())

    def getContainer(self):
        return self.container
    
    def getPayload(self):
        return self.payload

    def carrega(self):
        # fileContainer= '/home/wendel/Área de Trabalho/aux/LtSat/tst/GUI_2022/datasets/flight_1038_C.csv'
        # filePayload= '/home/wendel/Área de Trabalho/aux/LtSat/tst/GUI_2022/datasets/flight_1038_T.csv'
        # dfCont= pd.read_csv(fileContainer, sep=",", encoding="utf-8")
        # dfPay= pd.read_csv(filePayload, sep=",", encoding="utf-8")

        container= self.getContainer()
        payload= self.getPayload()

        return container[0]

        # dfCont['TEAM_ID']= container[[0]]
        # dfCont['MISSION_TIME']= container[[1]]
        # dfCont['PACKET_COUNT']= container[[2]]
        # dfCont['PACKET_TYPE']= container[[3]]
        # dfCont['MODE']= container[[4]]
        # dfCont['TP_RELEASED']= container[[5]]
        # dfCont['ALTITUDE']= container[[6]]
        # dfCont['TEMP']= container[[7]]
        # dfCont['VOLTAGE']= container[[8]]
        # dfCont['GPS_TIME']= container[[9]]
        # dfCont['GPS_LATITUDE']= container[[10]]
        # dfCont['GPS_LONGITUDE']= container[[11]]
        # dfCont['GPS_ALTITUDE']= container[[12]]
        # dfCont['GPS_SATS']= container[[13]]
        # dfCont['SOFTWARE_STATE']= container[[14]]
        # dfCont['CMD_ECHO']= container[[15]]

        # dfPay['TEAM_ID']= payload[[0]]
        # dfPay['MISSION_TIME']= payload[[1]]
        # dfPay['PACKET_COUNT']= payload[[2]]
        # dfPay['PACKET_TYPE']= payload[[3]]
        # dfPay['TP_ALTITUDE']= payload[[4]]
        # dfPay['TP_TEMP']= payload[[5]]
        # dfPay['TP_VOLTAGE']= payload[[6]]
        # dfPay['GYRO_R']= payload[[7]]
        # dfPay['GYRO_P']= payload[[8]]
        # dfPay['GYRO_Y']= payload[[9]]
        # dfPay['ACCEL_R']= payload[[10]]
        # dfPay['ACCEL_P']= payload[[11]]
        # dfPay['ACCEL_Y']= payload[[12]]
        # dfPay['MAG_R']= payload[[13]]
        # dfPay['MAG_P']= payload[[14]]
        # dfPay['MAG_Y']= payload[[15]]
        # dfPay['POINTING_ERROR']= payload[[16]]
        # dfPay['TP_SOFTWARE_STATE']= payload[[17]]

    
