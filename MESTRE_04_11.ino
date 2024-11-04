#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);  // pinos CE e CSN

// Endereços de comunicação para diferentes servos
const byte address1[6] = "00001";
const byte address2[6] = "00002";
const byte address3[6] = "00003";
const byte address4[6] = "00004";
const byte address5[6] = "00005";

char command = 'aji';  // comando para enviar
int servoNumber = 1;   // Número do servo que deve receber o comando (1 a 5)

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.setPALevel(RF24_PA_MIN);
  setAddress(servoNumber);  // Configura o endereço de acordo com o servo
  radio.stopListening();  
}

void loop() {
  // Envia o comando para o servo selecionado
  radio.write(&command, sizeof(command)); 

  // Aguarda uma resposta do servo (número de segundos)
  radio.startListening();
  unsigned long startTime = millis();
  bool received = false;

  while (millis() - startTime < 5000) {  // Aguarda até 5 segundos por uma resposta
    if (radio.available()) {
      int countTime = 0;
      radio.read(&countTime, sizeof(countTime));
      Serial.print("Tempo de reação: ");
      Serial.print(countTime);
      Serial.println(" segundos.");
      received = true;
      break;
    }
  }

  radio.stopListening();
  delay(5000);  // Aguarda antes de enviar o próximo comando
}

// Função para definir o endereço de comunicação baseado no número do servo
void setAddress(int servoNum) {
  switch (servoNum) {
    case 1:
      radio.openWritingPipe(address1);
      break;
    case 2:
      radio.openWritingPipe(address2);
      break;
    case 3:
      radio.openWritingPipe(address3);
      break;
    case 4:
      radio.openWritingPipe(address4);
      break;
    case 5:
      radio.openWritingPipe(address5);
      break;
    default:
      Serial.println("Número de servo inválido. Selecionando servo 1 por padrão.");
      radio.openWritingPipe(address1);
      break;
  }
}



