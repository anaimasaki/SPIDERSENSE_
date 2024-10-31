#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);  // pinos CE e CSN

const byte address[6] = "00001";  // endereço de comunicação
char command = 'aji';  // comando para enviar

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();  
}

void loop() {
  // envia o comando para o servo 
  radio.write(&command, sizeof(command)); 

  // aguarda uma resposta do servo (número de segundos)
  radio.startListening();
  unsigned long startTime = millis();
  bool received = false;

  while (millis() - startTime < 5000) {  // aguarda até 5 segundos por uma resposta
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

