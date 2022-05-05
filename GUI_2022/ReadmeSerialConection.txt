é transmitido uma string do arduino para o PC, após, a mesma é devidamente divida de acordo com seus atributos onde cada parte da divisão corresponde a uma posição do vetor.
Em seguida o vetor de chegada popula as listas de atributos. Uma analogia seria, o vetor de chegada poderia ser linhas enquanto cada lista seria uma coluna.
As listas são descarregadas em um arquivo csv de transição de 5 em 5 segundos.
O arquivo de transição é processado pelo software, onde, os atributos são divididos em dois outros arquivos
MSP.bytesize > 0:

, voltageP=[], giroscopioR=[], giroscopioP=[], giroscopioY=[], acelerometroR=[], acelerometroP=[], acelerometroY=[], magnetometroR=[], magnetometroP=[], magnetometroY=[]

        self.temperaturaC= temperaturaC
        self.voltageC= voltageC
        self.gpsLatitudeC= gpsLatitudeC
        self.gpsLongitudeC= gpsLongitudeC
        self.gpsAlturaC= gpsAlturaC
        self.altitudeP= altitudeP
        self.temperaturaP= temperaturaP
        self.voltageP= voltageP
        self.giroscopioR= giroscopioR
        self.giroscopioP= giroscopioP
        self.giroscopioY= giroscopioY
        self.acelerometroR= acelerometroR
        self.acelerometroP= acelerometroP
        self.acelerometroY= acelerometroY
        self.magnetometroR= magnetometroR
        self.magnetometroP= magnetometroP
        self.magnetometroY= magnetometroY

