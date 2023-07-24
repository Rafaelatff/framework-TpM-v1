# Python para o Radiuino over Arduino
import serial
import math
import time
import struct
import socket
from time import localtime, strftime
import os
import pandas as pd # To work with csv file with different types

        # Trabalhando com csv
arquivo_csv = pd.read_csv('._N4_Comandos_N3_para_N1.csv')#,usecols=['Tempo_ms_vermelho_recebe_verde_transmite'])
print(type(arquivo_csv)) # <class 'pandas.core.frame.DataFrame'>

     
#PacoteDL = int(arquivo_csv.loc[:,[0]])
PacoteDL = arquivo_csv.loc[:,['Tempo_ms_vermelho_recebe_verde_transmite']].fillna(0).astype(int)
#PacoteDL2 = arquivo_csv.loc[:,['Status_LED_amarelo']]

#print(arquivo_csv)

print(PacoteDL)
#print(type(PacoteDL2))
#print(PacoteDL2)
#show(pacoteDL)
      
