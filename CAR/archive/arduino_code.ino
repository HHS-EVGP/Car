#include <SoftwareSerial.h>

#define tempSensor1 A0
#define tempSensor2 A1

#define brake A2

#define rxPin 3  // should be connected to ring of connector (tx from CA)
#define txPin 4  // should be connected to tip of connector (rx into CA)



SoftwareSerial SUART(rxPin, txPin);  //defines a second serial communication for the CA

String output;
int dataType = 0;       // keeps track of which type of data is being recieved
String fullValue = "";  // collects all the digits of a data point
String output_bp;
String output_temp;


void setup() {
  Serial.begin(9600);

  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);

  pinMode(tempSensor1, INPUT);
  pinMode(tempSensor2, INPUT);

  SUART.begin(9600);

}


void loop() {
  temperatures();

  Serial.println("BP,"+String(analogRead(brake)));

  suart();
  
  delay(250);
}

void suart(){
  Serial.println("IGNORE");
  if (SUART.available()){
    char data = SUART.read();
    Serial.print(data);
  }
  Serial.println("");
  Serial.println("IGNORE-END");
}

void temperatures() {

  Serial.println("temps,"+String(convert_tmp36(analogRead(tempSensor1)))+","+String(convert_tmp36(analogRead(tempSensor2))));

}

double convert_tmp36(int in) { 
  if(in <= 1){
    return -5;
  }
  if(in >= 270){
    return -6;
  }
  return ((((double)in/1024)*5-0.5)*100);
}
