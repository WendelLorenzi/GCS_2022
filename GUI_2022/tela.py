# coding=utf-8

from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
#from drawnow import *
from src.dataframes.index import dataframe

class Tela:
    def renderTela(self, dataframe):
        #Construção da tela começa aqui
        self.containerMaster= Tk()
        self.containerMaster.geometry("1200x800")
        self.containerMaster.title("LtSat")
        self.containerMaster.configure(background='#696969')


        self.MensagemIni= Message(self.containerMaster)
        self.MensagemIni.place(relx=0.00, rely=0.00, relheight=0.1, relwidth=1.0)
        self.MensagemIni.configure(text='''GCS software''')
        self.MensagemIni.configure(font=("Times New Roman", 18, "bold"))
        self.MensagemIni.configure(width=250)
        self.MensagemIni.configure(background='#696969', foreground='#FF0000')

        self.BotaoStart= Button(self.containerMaster)
        self.BotaoStart.place(relx=0.005, rely=0.10, height=40, width=100)
        self.BotaoStart.configure(pady='0')
        self.BotaoStart.configure(text=''' START ''')
        self.BotaoStart.configure(font=("Times New Roman", 10, "bold"))

        self.BotaoStop= Button(self.containerMaster)
        self.BotaoStop.place(relx=0.09, rely=0.10, height=40, width=100)
        self.BotaoStop.configure(pady='0')
        self.BotaoStop.configure(text=''' STOP and Save ''')
        self.BotaoStop.configure(font=("Times New Roman", 10, "bold"))

        self.BotaoSimEnable= Button(self.containerMaster)
        self.BotaoSimEnable.place(relx=0.025, rely=0.20, height=30, width=150)
        self.BotaoSimEnable.configure(pady='0')
        self.BotaoSimEnable.configure(text=''' SIMULATION ENABLE ''')
        self.BotaoSimEnable.configure(font=("Times New Roman", 8, "bold"))

        self.BotaoSimActivate= Button(self.containerMaster)
        self.BotaoSimActivate.place(relx=0.025, rely=0.26, height=30, width=150)
        self.BotaoSimActivate.configure(pady='0')
        self.BotaoSimActivate.configure(text=''' SIMULATION ACTIVATE ''')
        self.BotaoSimActivate.configure(font=("Times New Roman", 8, "bold"))

        self.LabelMissionTime= Label(self.containerMaster)
        self.LabelMissionTime.place(relx=0.005, rely=0.35, relheight=0.05, relwidth=0.15)
        self.LabelMissionTime.configure(font=("Times New Roman", 12, "bold"))
        self.LabelMissionTime.configure(text='Mission Time: ')
        self.LabelMissionTime.configure(background='#696969')

        self.LabelGPSTime= Label(self.containerMaster)
        self.LabelGPSTime.place(relx=0.005, rely=0.40, relheight=0.05, relwidth=0.15)
        self.LabelGPSTime.configure(font=("Times New Roman", 12, "bold"))
        self.LabelGPSTime.configure(text='GPS Time: ')
        self.LabelGPSTime.configure(background='#696969')

        self.LabelPackets= Label(self.containerMaster)
        self.LabelPackets.place(relx=0.005, rely=0.45, relheight=0.05, relwidth=0.15)
        self.LabelPackets.configure(font=("Times New Roman", 12, "bold"))
        self.LabelPackets.configure(text='Packets Recived: ')
        self.LabelPackets.configure(background='#696969')

        self.BotaoEnableMQTT= Button(self.containerMaster)
        self.BotaoEnableMQTT.place(relx=0.005, rely=0.58, height=25, width=100)
        self.BotaoEnableMQTT.configure(pady='0')
        self.BotaoEnableMQTT.configure(text=''' MQTT ENABLE ''')
        self.BotaoEnableMQTT.configure(font=("Times New Roman", 8, "bold"))

        self.BotaoDisableMQTT= Button(self.containerMaster)
        self.BotaoDisableMQTT.place(relx=0.09, rely=0.58, height=25, width=100)
        self.BotaoDisableMQTT.configure(pady='0')
        self.BotaoDisableMQTT.configure(text=''' MQTT DISABLE ''')
        self.BotaoDisableMQTT.configure(font=("Times New Roman", 8, "bold"))

        self.LabelTerminal= Label(self.containerMaster)
        self.LabelTerminal.place(relx=0.005, rely=0.70, relheight=0.25, relwidth=0.15)
        self.LabelTerminal.configure(background='#000000')
        self.LabelTerminaltext= Label(self.containerMaster)
        self.LabelTerminaltext.place(relx=0.005, rely=0.70, relheight=0.03, relwidth=0.15)
        self.LabelTerminaltext.configure(text='Terminal')
        self.LabelTerminaltext.configure(font=("Times New Roman", 10, "bold"))
        self.LabelTerminaltext.configure(background='#000000', foreground='#00FF00')


        self.ContainerPlot= Frame(self.containerMaster)
        self.ContainerPlot.place(relx=0.18, rely=0.1, relheight=0.88, relwidth=0.81)
        self.ContainerPlot.configure(width=1000)
        self.ContainerPlot.configure(background='#696969')

        #Criando a figure
        figura= plt.figure(figsize= (17,10), dpi=60)
        ax= figura.subplots(4, 2)
        #Temperatura
        #ax[0, 0].plot(str(dataframe.getTemperaturaCdf()), 'r', label= 'Container') #row= 0 col= 0 -> Container
        #ax[0, 0].plot(self.temperaturaP, 'g', label= 'Payload') #-> Payload
        ax[0, 0].set_title('Temperature')
        ax[0, 0].set_ylabel('Degrees (ºC)')
        ax[0, 0].set_ylim(0, 50)
        ax[0, 0].legend()
        #Altitude
        ax[0, 1].plot(str(dataframe.getAltitudeCdf()), 'r', label='Container') #row= 0 col=1
        #ax[0, 1].plot(self.altitudeP, 'g', label='Payload')
        ax[0, 1].set_title('Altitude')
        ax[0, 1].set_xlabel('Time (s)')
        ax[0, 1].set_ylabel('Meters (m)')
        ax[0, 1].set_ylim(0, 800)
        ax[0, 1].legend()
        #Voltage
        #ax[1, 0].plot(self.voltageC, 'r', label='Container') #row=1 col= 0
        #ax[1, 0].plot(self.voltageP, 'g', label='Payload')
        ax[1, 0].set_title('Voltage')
        ax[1, 0].set_xlabel('Tempo (s)')
        ax[1, 0].set_ylabel('Tensão (V)')
        ax[1, 0].set_ylim(0, 15)
        ax[1, 0].legend()
        #Coordenadas GPS container
        #ax[1, 1].plot(self.gpsLatitudeC, 'r', label='Latitude') #row=1 col=1
        #ax[1, 1].plot(self.gpsLongitudeC, 'g', label='Longitude')
        ax[1, 1].set_title('Coordinates GPS container')
        ax[1, 1].set_xlabel('Latitude (Leste/East)')
        ax[1, 1].set_ylabel('Longitude (Oeste/West)')
        ax[1, 1].set_ylim(-80, 80)
        ax[1, 1].set_xlim(-100, 100)
        ax[1, 1].legend()
        #Altitude GPS container
        #ax[2, 0].plot(self.gpsAlturaC, 'r') #row=2 col=0
        ax[2, 0].set_title('GPS altitude')
        ax[2, 0].set_xlabel('Time (s)')
        ax[2, 0].set_ylabel('Meters (m)')
        ax[2, 0].set_ylim(0, 800)
        #Giroscopio Payload
        #ax[2, 1].plot(self.giroscopioP, 'blue', label='X') #row= 2 col=1
        #ax[2, 1].plot(self.giroscopioY, 'g', label='Y')
        #ax[2, 1].plot(self.giroscopioR, 'r', label='Z')
        ax[2, 1].set_title('Gyroscope Payload')
        ax[2, 1].set_xlabel('Time (s)')
        ax[2, 1].set_ylabel('Rotation (°/s)')
        ax[2, 1].set_ylim(-2000, 2000)
        ax[2, 1].legend()
        #Acelerometro Payload
        #ax[3, 0].plot(self.acelerometroP, 'b', label='X') #row=3 col=0
        #ax[3, 0].plot(self.acelerometroY, 'g', label='Y')
        #ax[3, 0].plot(self.acelerometroR, 'r', label='Z')
        ax[3, 0].set_title('Accelerometer payload')
        ax[3, 0].set_xlabel('Time (s)')
        ax[3, 0].set_ylabel('Acceleration (a)')
        ax[3, 0].set_ylim(-10, 10)
        ax[3, 0].legend()
        #Magnetometro Payload
        #ax[3, 1].plot(self.magnetometroP, 'b', label='X') #row=3 col=1
        #ax[3, 1].plot(self.magnetometroY, 'g', label='Y')
        #ax[3, 1].plot(self.magnetometroR, 'r', label='Z')
        ax[3, 1].set_title('Magnetometer payload')
        ax[3, 1].set_xlabel('Time (s)')
        ax[3, 1].set_ylabel('Gauss (G)')
        ax[3, 1].set_ylim(-150, 150)
        ax[3, 1].legend()

        figura.tight_layout() 

        self.canva= FigureCanvasTkAgg(figura, self.ContainerPlot)
        self.canva.get_tk_widget().grid(row=0, column=0)

        self.containerMaster.mainloop()

if __name__ == '__main__':
    tela = Tela()
    tela.renderTela(dataframe())


