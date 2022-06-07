# -*- coding: utf-8 -*-
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