#include <Servo.h>  

//RECONHECIMENTO
int ledVerde=41;
int ledVermelho=40;

//SALA
int ledSala=9;

//ACADEMIA
const int pinoReleCh2 = 10;

//COZINHA
int ledCozinha=5;

// ALARME
int buzzerAlarme = 53; 

//ENERGIA 
float ldrEsq = A14;
float ldrDir = A15; 
Servo ServoSolar;

//QUARTO
int ledQuarto = 11;

//PISCINA
int ledRed = 1;
int ledYellow = 2;
int ledGreen = 3;

void setup() {
  //RECONHECIMENTO
  pinMode (ledVermelho, OUTPUT);
  pinMode (ledVerde, OUTPUT);
  
  //SALA
  pinMode (ledSala, OUTPUT);
  
  //Academia
  pinMode(pinoReleCh2, OUTPUT); //DEFINE O PINO COMO SAÍDA
  digitalWrite(pinoReleCh2, HIGH); //MÓDULO RELÉ INICIA DESLIGADO

  //COZINHA
  pinMode (ledCozinha, OUTPUT);
  digitalWrite(ledCozinha, LOW);
  
  //ALARME
  pinMode(buzzerAlarme, OUTPUT);
  
  //ENERGIA
  ServoSolar.attach(51);
  pinMode(A14, INPUT);
  pinMode(A15, INPUT);
  ServoSolar.write(90);

  //QUARTO
  pinMode(ledQuarto, OUTPUT);

  //PISCINA
  pinMode (ledRed, OUTPUT);
  pinMode (ledYellow, OUTPUT);
  pinMode (ledGreen, OUTPUT);

  Serial.begin(9600);
}

void loop() {
    char command = Serial.read();
      switch (command) {
        case '1':
          digitalWrite(ledVerde, HIGH);
          digitalWrite(ledVermelho, LOW);
          break;
        case '2':
          digitalWrite(ledVerde, LOW);
          digitalWrite(ledVermelho, HIGH);
          break;
        case '3':
          digitalWrite(ledSala, HIGH);
          break;
        case '4':
          digitalWrite(ledSala, LOW);
          break;
        case '5'://ligar ventilador
            digitalWrite(pinoReleCh2, LOW);
            break;
        case '6'://desligar ventilador
            digitalWrite(pinoReleCh2, HIGH);
            break;
        case '7':
          digitalWrite(ledCozinha, HIGH);
          break;
        case '8':
          digitalWrite(ledCozinha, LOW);
          break;
        case '9' :
          for(int tom=600; tom<1200 ; tom ++){
            delay(5);
            tone(buzzerAlarme, tom);
          }
          for(int tom=1200; tom>600 ; tom --){
            delay(5);
            tone(buzzerAlarme, tom);
          }
          break; 
        case 'C':
          digitalWrite(ledQuarto, HIGH);
          break;

        case 'D':
          digitalWrite(ledQuarto, LOW);
          break;
         
        case '0':
          noTone(buzzerAlarme); 
          break;
        default:
          printf("opcao inválido");
          break;
      }

      //PISCINA SEMPRE ATIVA
      int value = analogRead(A0);
      if (value > 650){
        digitalWrite(ledGreen, HIGH);
        digitalWrite(ledYellow, HIGH);
        digitalWrite(ledRed, HIGH);

      }
      if ((value >= 400 && value <= 500)) {
        digitalWrite(ledGreen, LOW);
        digitalWrite(ledYellow, HIGH);
        digitalWrite(ledRed, HIGH);  

      }
      if (value < 300){
        digitalWrite(ledGreen, LOW);
        digitalWrite(ledYellow, LOW);
        digitalWrite(ledRed, HIGH);
      }

      // ENERGIA SOLAR SEMPRE ATIVA
      ldrEsq = analogRead(A14);
      ldrDir = analogRead(A15);
      if(ldrEsq >= 200){
          ServoSolar.write(135);
          delay(1000);
      }
      else if(ldrDir >= 200){
          ServoSolar.write(45);
          delay(1000);
      }
}
