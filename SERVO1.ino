#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);  // pinos CE e CSN 

const byte address[6] = "00001";  // endereço de comunicação
const int ledPin = 4;             // LED
const int buttonPin = 7;          // botão

bool counting = false;            // para verificar se está contando
unsigned long startTime = 0;      // tempo inicial
unsigned long countTime = 0;      // tempo contado

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);  // botão com resistor pull-up
  Serial.begin(9600);

  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();  // servo escuta os sinais do mestre
}

void loop() {
  if (radio.available()) {
    char command = 0;
    radio.read(&command, sizeof(command));

    if (command == 'aji' && !counting) {
      // recebe o sinal e começa a contagem
      digitalWrite(ledPin, HIGH);  // liga o LED
      counting = true;
      startTime = millis();  // início da contagem
      Serial.println("Iniciando contagem...");
    }
  }

  if (counting) {
    // verifica se o botão foi pressionado
    if (digitalRead(buttonPin) == LOW) {
      digitalWrite(ledPin, LOW);  // desliga o LED
      countTime = (millis() - startTime) / 1000;  // calcula o tempo em segundos
      counting = false;
      Serial.print("Contagem parada: ");
      Serial.print(countTime);
      Serial.println(" segundos.");

      // envia o tempo de volta para o mestre
      radio.stopListening();
      radio.write(&countTime, sizeof(countTime));
      radio.startListening();
    }
  }
}
