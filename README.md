# HMI_2022
## GCS CanSat competition 2022 - LtSat
### Missão
[Mission Guide](https://www.cansatcompetition.com/docs/CanSat_Mission_Guide_2022.pdf)
#### Objetivos da missão:
- A carga útil deve ser presa ao contêiner por um cabo de 10 metros de comprimento.
- O Cansat será lançado a uma altitude que varia de 670 metros a 725 metros
- Uma vez que o Cansat é lançado do foguete, o Cansat deve descer usando um pára-quedas a uma taxa de 15 m/s. A 400 metros, o Cansat deverá lançar um pára-quedas maior para reduzir a razão de descida para 5 m/s. A 300 metros, a carga útil deve ser lançada do contêiner. 
- Depois que a carga é liberada, ela deve descer a distância de 10 metros em 20 segundos. Durante esse tempo, a carga útil deve manter a orientação de uma câmera de vídeo apontando para o sul. A câmera de vídeo deve ser apontada 45 graus para baixo.

![missao](https://user-images.githubusercontent.com/38894557/179631533-d23d1bf5-d1b0-4a0b-a535-b012e1dd91a2.png) || ![mission](https://user-images.githubusercontent.com/38894557/179634803-fdbcb834-6fcc-49a8-8bb3-fde9a02b60b4.png)

#### Transmissão da telemetria:
- O container deve transmitir a sua telemetria a 1Hz no formato descrito pela competição.
- O contanier deve sondar a telemetria da carga util e a retransmitir a uma velocidade de 4Hz no formato descrito pela competição.
##### Sensores que compoem a telemetria: 
- Temperatura, Gps, Giroscopio, Acelerometro, Magnetometro
- ![arquitetura-embarcado](https://user-images.githubusercontent.com/38894557/179634854-79174437-40c6-4f5e-8747-4d69fad71783.png)


##### LISTA DE ATRIBUTOS E POSIÇÃO NO VETOR SERIAL   
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


![tela_LtSat](https://user-images.githubusercontent.com/38894557/167059631-af16e0d4-5320-4732-9799-02a736a92e47.png)
