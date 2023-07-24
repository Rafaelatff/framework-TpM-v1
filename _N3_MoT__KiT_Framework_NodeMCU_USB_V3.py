# Python para o Radiuino over Arduino
import serial
import math
import time
import struct
import socket
from time import localtime, strftime
import os
import pandas as pd # To work with csv file with different types

# Configura a serial
# para COM# o número que se coloca é n-1 no primeiro parâmetrso. Ex COM9  valor 8
n_serial = input("Digite o número da serial = ") #seta a serial
n_serial1 = int(n_serial) - 1
ser = serial.Serial("COM"+str(n_serial), 115200, timeout=0.5,parity=serial.PARITY_NONE) # serial Windows
ser.reset_input_buffer()
ser.reset_output_buffer()

#============= Arquivos da dados
#apaga os arquivos temporários que foram gerados na rodada de testes anteriores
if os.path.exists("N4_Temp_RSSI.txt"):
   os.remove("N4_Temp_RSSI.txt")
if os.path.exists("N4_Temp_luminosidade.txt"):
   os.remove("N4_Temp_luminosidade.txt")


# ======== Arquivos Nível 4 que armazenam as medidas realizadas
Arquivo_log_Luminosidade_RSSI = strftime("N4_Log_dados_%Y_%m_%d_%H-%M-%S.txt") # Arquivo de log

# Arquivos temporários
Arquivo_temporário_RSSI = "N4_Temp_RSSI.txt"
Arquivo_temporário_Luminosidade = "N4_Temp_luminosidade.txt"

print ("Arquivo de log: %s" % Arquivo_log_Luminosidade_RSSI)
N4_Log_dados = open(Arquivo_log_Luminosidade_RSSI, 'w') # mode=r for writing on file

# Cria o vetor Pacote
PacoteDL = {}
PacoteUL= {}

perda_PK_UL = 0

# Cria Pacote de 52 bytes com valor zero em todas as posições
for i in range(52): # faz um array com 52 bytes
   PacoteDL[i] = 0
   PacoteUL[i] = 0

print(type(PacoteDL)) # To check the Pacote type (IT RETURNED AS <dict> DICTIONARY)

#inicializa variáveis auxiliares
Numero_medidas = 1000000 # Realiza 1 milhão de medidas

try:
   # ============ Camada Física - Transmite o pacote        
   for j in range(1,Numero_medidas): # Similar to for in C, range(start, stop, step)
     
   # ============= Comandos e valores para serem enviados para o nó sensor

        # Trabalhando com csv
      arquivo_csv = pd.read_csv('._N4_Comandos_N3_para_N1.csv',index_col=1)
     
      PacoteDL[34] = int(arquivo_csv.loc[:,["Tempo_LED_vermelho-in_verde-out"]])
      PacoteDL[37] = int(arquivo_csv.loc[:,["LED_amarelo"]])

         # Trabalhando com txt
      #arquivo = open('._N4_Comandos_N3_para_N1.txt', 'r') # leitura do arquivo comandos_oficina.txt que estão nas linhas
      #np.loadtxt(arquivo)
      #PacoteDL[34] = int(arquivo.readline())  # Tempo de pisca dos LEDs na PK2 sendo vermelho quando chega pacote e verde quando transmite pacote
      #PacoteDL[37] = int(arquivo.readline())  # Acende ou apaga LED amarelo
      #arquivo.close()
      
# ============= TRANSMITE O PACOTE            
                  
      for k in range(52): # transmite pacote
         Pacote_DL_Byte = chr(PacoteDL[k])
         ser.write(Pacote_DL_Byte.encode('latin1')) # If no specified, UTF-8 is used. Should it be 'latin-1' instead?       
      
      # Aguarda a resposta do sensor
      time.sleep(0.5)

# ============= RECEBE O PACOTE

      PacoteUL = ser.read(52) # faz a leitura de 52 bytes do buffer que rec

      if len(PacoteUL) == 52:
         
         # Potência de recepção rádio (RSSI) pelo nó sensor
         byte_RSSI_DL = PacoteUL[2]

         RSSI_DL = (-1)*byte_RSSI_DL # A RSSI enviada é positiva e deve ser multiplicado por -1

   # ============= Luminosidade                
         Luminosidade = PacoteUL[17]*256+ PacoteUL[18]

         # ======imprime no shell do IDLE do Python
         print ('Cont = ', j,' RSSI DL = ', RSSI_DL,' Luminosidade = ', Luminosidade)

         # Salva no arquivo de log e arquivo temporário para exibição
         print (time.asctime(),';',j,';',RSSI_DL,';',Luminosidade,file=N4_Log_dados)

   # Arquivos temporários
         N4_Temp_RSSI = open(Arquivo_temporário_RSSI, 'a+')
         print (RSSI_DL,file=N4_Temp_RSSI)
         N4_Temp_RSSI.close()

         N4_Temp_luminosidade = open(Arquivo_temporário_Luminosidade, 'a+')
         print (Luminosidade,file=N4_Temp_luminosidade)
         N4_Temp_luminosidade.close()
#=======================LOOP DE 1000000
   print ('Pacotes enviados = ',j)
   N4_Log_dados.close()
   #Medidas.close()
   ser.close()
   print ('Fim da Execução')  # escreve na tela

except KeyboardInterrupt:
   ser.close()
   N4_Log_dados.close()
   N4_Temp_RSSI.close()
   N4_Temp_luminosidade.close()


