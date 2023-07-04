// Nível 1 com o protocolo MoT Kit framework NodeMCU com USB
// Objetivo: código básico genérico usando o pacote de 52 bytes

// 1 - Bibliotecas
#include "ESP8266WiFi.h"

// 2 - Variáeis
byte PacoteDL[52]; // Pacote de 52 bytes que será recebido pelo nó sensor
byte PacoteUL[52]; // Pacote de 52 bytes que será transmitido pelo nó sensor
int Luminosidade; // Valor da luminosidade na saída do ADC. Número de 0 a 1023 
int Inteiro; // Variável que armazena o valor inteiro da divisão da luminosidade por 256
int Resto; // Variável que amarzena o resto da divisão da luminosidade por 256
int tempo_pisca; // Tempo que os LEDs vermelho e verde piscam. 
int contadorUL; // contador de pacotes transmitidos pelo nó sensor
int contadorDL; // contador de pacotes recebidos pelo nó sensor
int RSSI_DL; // Intensidade de sinal simulada

// 3 - Void setup - comandos executados uma única vez quando liga a PK2
void setup() {
  Serial.begin(115200);
  pinMode (D3, OUTPUT); // LED vermelho
  pinMode (D4, OUTPUT); // LED verde
  pinMode (D7, OUTPUT); // LED amarelo

  contadorUL = 0; // contador de pacotes de up link
  contadorDL = 0; // contador de pacotes de down link
}

// 4 - Loop
void loop() {

// ===================================SÓ PARA TESTE DO ADC - COMENTAR PARA USAR RADIUINOTEST==============
// ESSA PARTE DO CÓDIGO É SÓ PARA TESTAR SE A MEDIDA DE LUMINOSIDADE ESTÁ FUNCIONANDO
// IMPORTANTE: tem que comentar essa parte quando for usar o RadiuinoTest
//  Luminosidade = analogRead(A0);
//  Serial.println(Luminosidade);
// ===================================================================================

        // Verifica se existem 52 bytes no buffer da serial
	if (Serial.available() == 52)   // recebe pacote de 52 bytes de down link vindo do computador
	{
    contadorDL = contadorDL + 1; // contador de pacotes recebidos
    
   // Leitura do buffer da serial para ler o pacote recebido e zera pacote de transmissão
      for (int i = 0; i < 52; i++) // PacoteUL[#] é preenchido com zero e PacoteDL[#] recebe os bytes do buffer
		  {
			    PacoteUL[i] = 0; // Zera o pacote de transmissão
			    PacoteDL[i] = Serial.read();  // Faz a leitura dos bytes do pacote que estão no buffer da serial
          delay(1); // Intervalo de 1 ms para cada ciclo do for para estabilidade
		  }

    // Para piscar o LED deve ter o valor no byte 34 
    tempo_pisca = PacoteDL[34]; // byte 34 tem o tempo em mili segundosque os LEDs verde e vermelho piscam

    // LED vermelho pisca quando recebe o pacote no Nível 1 vindo do Nível 3 com duração do valor que está no 34
    digitalWrite (D3, HIGH); // Liga led vermelho
    delay (tempo_pisca); // espera o tempo de pisca do byte 34
    digitalWrite (D3, LOW); // Desliga led vermelhO
   
    // Acende o LED amarelo se byte 37 estiver 1
    if (PacoteDL[37] == 1)  // PK2 LED amarelo
   {
      digitalWrite (D7, HIGH);
    }
    else 
    {
      digitalWrite (D7, LOW);
    }

// Sensores de temperatura, luminosidade e botão
    Luminosidade = 1024 - analogRead(A0); // pega o complemento de 1023 em função de como o LDR capta a luz na PK2
    Inteiro = (byte) ((int)(Luminosidade)/256); // Valor inteiro será colocado no byte 17 do pacote
    Resto = (byte) ((int)(Luminosidade)%256); // Resto da divisão será colocado no byte 18 do pacote

// Coloca a luminosidade no pacote de up link
    PacoteUL[16] = 16; // Pode ser utilizado para indicar o tipo de sensor no byte 16
    PacoteUL[17] = Inteiro; // aloca no pacote byte 17 o valor inteiro da divisão por 256
    PacoteUL[18] = Resto; // aloca no pacote byte 18 o valor do resto da divisão por 256

// ============== contador de pacotes de up link
    contadorUL = contadorUL + 1; // contador de pacotes transmitidos up link

// =============== Simula potência recebida pelo nó sensor
    RSSI_DL = random(70, 90); // simulação da potência de rádio recebida (RSSI - Radio Signal Strengh Indicator) pelo sensor que varia entre 70 e 90 com distribuição uniforme
    // No Pyhton será multiplicado por -1 para representar uma variação de potência rádio recebida de -70 a -90 dBm
    
// =================Informações de gerência do pacote
          PacoteUL[2] = RSSI_DL; // aloca no byte 2 do pacote a RSSI simulada
          PacoteUL[12] = contadorDL;
          PacoteUL[13] = contadorUL;

// Transmissão do pacote pela serial do Arduino que vai ser enviado para o ScadaBR via USB         
         for (int i = 0; i < 52; i++)
        			{
        			Serial.write(PacoteUL[i]);
        			}
// LED verde pisca para represntar a transmissão do pacote do Nível 1 para o Nível 3 com duração no byte 34
        digitalWrite (D4, HIGH); // Liga led verde
        delay (tempo_pisca);
        digitalWrite (D4, LOW); // Liga led verde
	} // if do recebimento do pacote
} // fim do lopp()

    

       		
 
     
