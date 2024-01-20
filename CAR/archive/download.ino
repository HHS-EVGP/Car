#include <string.h>
#include <SoftwareSerial.h>
#include <SPI.h>
#include <RH_RF95.h>
// #include <Arduino_LSM6DSOX.h>
#include <SD.h>

//sensors_event_t accel_event;
//sensors_vec_t orientation;

//Tempature Sensor(s)
#define tempSensor1 A0
#define tempSensor2 A1
// #define tempSensor3 A2

#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 2

#define rxPin 3  // should be connected to ring of connector (tx from CA)
#define txPin 4  // should be connected to tip of connector (rx into CA)

RH_RF95 rf95(RFM95_CS, RFM95_INT);

File myFile;

// How long between each data send (milliseconds)
int period = 500;
unsigned long time_now = 0;
unsigned long time_now_IMU = 0;

float xA, yA, zA, xG, yG, zG;

int dataType = 0;       // keeps track of which type of data is being recieved
String fullValue = "";  // collects all the digits of a data point

//String columns = "";
String output = "";
String IMUoutput = "";

bool imuFail = false;
bool firstRun = true;

int16_t packetnum = 0;

//String dataTypesCA[5] = { "\"AmpHrs\", ", "\"Voltage\", ", "\"Current\", ", "\"Speed\", ", "\"Miles\", " };



SoftwareSerial SUART(rxPin, txPin);  //defines a second serial communication for the CA

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);

  pinMode(10, OUTPUT);

  pinMode(tempSensor1, INPUT);
  pinMode(tempSensor2, INPUT);
  // pinMode(tempSensor3, INPUT);

  SUART.begin(9600);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    imuFail = true;
  }

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }

  if (!SD.begin(8)) {
    Serial.println("SD initialization failed!");
    while (1);
  }

  myFile = SD.open("data.txt", FILE_WRITE);

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(433.00)) {
    Serial.println("setFrequency failed");
    while (1);
  }

  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);

}



void loop() {
  if (millis() >= time_now + period) {
    time_now += period;

    temperature_math();

    output = output + String(IMUoutput);
    Serial.println(IMUoutput);
    IMUoutput = "";

    byte n = SUART.available();
    for (int i = 0; i<n; i++)
    {
      char x = SUART.read();

      if (x >= 45 && x <= 57) // '-', '.', '/', or 0..9
      {
        fullValue.concat(x);
      }
      else // assume delimiter
      {
        //if (fullValue =! "") {
        output = output + fullValue + ", ";
        //}
        //columns = columns + dataTypesCA[dataType];
        fullValue = "";
        dataType++;
        if (dataType == 5)
        {
          dataType = -1; // This is what was working last year; maybe there's an extra delimiter character for a new line?
          break;
        }
      }
    }
  

    // columns = columns + "\"accX\"";
    output = output + "NULL";

  //   //Serial.println(columns);
  //   Serial.println(output);
  //   // Serial.println("");
    // columns = "";

    Serial.println(" - - ");
    Serial.println(output);
    
    char radiopacket[20] = "Hello World #      ";
    itoa(packetnum++, radiopacket+13, 10);
    Serial.print("Sending "); Serial.println(radiopacket);
    radiopacket[19] = 0;
    Serial.println(" -1- ");
  
    Serial.println("Sending..."); //delay(10);
    rf95.send((uint8_t *)radiopacket, 20);
    Serial.println(" -2- ");

    if (myFile) {
      Serial.print("Writing to data.txt...");
      myFile.println(output);
      // close the file:
      myFile.close();
      Serial.println("done.");
    } else {
      // if the file didn't open, print an error:
      Serial.println("error opening data.txt");
    }
    
    Serial.println(" -3- ");

    Serial.println(output);

    output = "";
  }

  if (millis() >= time_now_IMU + period*5) {
    time_now_IMU += period*5;
    imu();
  }

}

void temperature_math() {

  output = output + convert_tmp36(analogRead(tempSensor1)) + ", ";
  //columns = columns + "\"TMP36_1\", ";

  output = output + convert_tmp36(analogRead(tempSensor2)) + ", ";
  //columns = columns + "\"TMP36_2\", ";

  // int tempInput3 = analogRead(tempSensor3);
  // temp = tempInput3 * 5.0 / 1024.0;  //convert to voltage
  // temp = (temp * 1000) / (5.0 - temp);
  // temp = -0.0000237 * pow(temp, 2) + 0.181 * temp - 136;
  // output = output + temp + ", ";
  //columns = columns + "\"KTY83\", ";
}

void imu() {
  // delay(100);
  if (imuFail == true) {
    xA = 9999;
    yA = 9999;
    zA = 9999;
    xG = 9999;
    yG = 9999;
    zG = 9999;
    firstRun = false;
  } else {
    if (IMU.gyroscopeAvailable()) {
      IMU.readGyroscope(xG, yG, zG);
    } else if (firstRun == true) {
      xG = 9999;
      yG = 9999;
      zG = 9999;
    }
    if (IMU.accelerationAvailable()) {
      IMU.readAcceleration(xA, yA, zA);
    } else if (firstRun == true) {
      xA = 9999;
      yA = 9999;
      zA = 9999;
    }
    firstRun = false;
  }
  String liveData = "";

  

  // liveData += "xG:";
  liveData += xG;
  // liveData += "yG:";
  liveData += yG;
  // liveData += "zG:";
  liveData += zG;
  // liveData += "xA:";
  liveData += xA;
  // liveData += "yA:";
  liveData += yA;
  // liveData += "zA:";
  liveData += zA;
  // liveData += "END,";
  IMUoutput = IMUoutput + liveData;
  // Serial.println(IMUoutput);
  // IMUoutput = IMUoutput + "A--  ";
  // IMUoutput = "";
}

String float2string(float f){
  String s, s1, s2;
  String out;
  int sl;
  
  s = f;
  sl = s.length();
  // Serial.println();
  // Serial.println(s);
  s1 = s.substring(0,sl-3);
  s2 = s.substring(sl-2,sl);
  s = s1 + s2;
  // Serial.println(s1);
  // Serial.println(s2);
  // Serial.println(s);

  sl = s.length(); 

  if(f < 0){
    s = s.substring(1,sl);
    if(sl == 4){
      out = "1000" + s; // + "0"
    }else if(sl == 5){
      out = "100" + s; // + "0"
    }else if(sl == 6){
      out = "10" + s; // + "0"
    }else if(sl == 7){
      out = "1" + s; // + "0"
    }
  }else{
    if(sl == 3){
      out = "0000" + s;
    }else if(sl == 4){
      out = "000" + s;
    }else if(sl == 5){
      out = "00" + s;
    }else if(sl == 6){
      out = "0" + s;
    }
  }

  out = "9" + out;
  return out;

}

//calculations to convert input from tmp 36 sensorto temperature. Sensor outputs 0-1.75 volts from -50 - 125 C, with .01 V = 1 degree C
double convert_tmp36(int in) {
  double converted;
  converted = (double)in / 1024;  // what percentage of the total input range (5V) is the input
  converted = converted * 5;      // multiply by 5V for voltage
  converted = converted - 0.5;    // offset to line up 0V and 0 degrees (not error)
  converted = converted * 100;    // convert to degrees
  return converted;
}
