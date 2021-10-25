#include <Arduino.h>
#include <SensirionI2CScd4x.h>
#include <Wire.h>

//Soilmoisture analog and power pins
#define soilPower 2
#define soilMoisture A1

//Photoresistor pin number
#define photoResistor A2

//Air humidity and heat
#define LEDPIN 11
SensirionI2CScd4x scd4x;

//Define LED pins.
#define blue 3
#define yellow 1
#define red 0
#define green 4

//RX and TX pins
#define rxPin 7
#define txPin 8

bool waitingToStart = true;

//String value;
String codes[10] = {"Low Air", "High Air", "Low Soil", "High Soil", "Low Light", "High Light", "Low Temp", "High Temp", "Low CO2", "High CO2"};
int lengthOfCodesArray = 10;

int timeInterval=40000;

bool flashYellow = false;
bool flashRed = false;
bool flashBlue = false;
bool flashGreen = false;
bool yellowOn = false;
bool redOn = false;
bool blueOn = false;
bool greenOn = false;

void setup()
{
  //Start serial monitor on laptop and bluetooth device.
  Serial.begin(9600);
  Serial1.begin(9600);

  Wire.begin();
  scd4x.begin(Wire);
  scd4x.startPeriodicMeasurement();

  //Setup output and input pins for various sensor, lights, and buzzer.
  pinMode (soilMoisture, INPUT);
  pinMode (photoResistor, INPUT);
  pinMode (blue, OUTPUT);
  pinMode (yellow, OUTPUT);
  pinMode (red, OUTPUT);
  pinMode (green, OUTPUT);
}

void loop()
{
    sensorDataOut();
    delay(100);
    int startTime = millis();
    int currentTime;
    while ((currentTime - startTime )< timeInterval)
    {
        currentTime = millis();
        lightFlasher();
    }
    
    flashYellow = false;
    flashRed = false;
    flashBlue = false;
    flashGreen = false;
    yellowOn = false;
    redOn = false;
    blueOn = false;
    greenOn = false;
}

void sensorDataOut()
{
  String startCommand = "Words";
  while (waitingToStart == true)
  {
    if (Serial1.available())
    {
      startCommand = Serial1.readString();
      if (startCommand == "Start")
      {
        Serial1.println("Start");
        waitingToStart = false;
      }
    }
  }

  String messageText;
  //Powers the sensors
  digitalWrite(LEDPIN, HIGH); ///could be placed at the bottom to turn off the sensor after data has been collected.
  digitalWrite(soilPower, HIGH);

  //Reads/holds soil moisture data
  float soil = analogRead(soilMoisture);

  //Reads/holds photoresistor data
  float lumStatus = analogRead(photoResistor);

  uint16_t co2;
  float temperature;
  float humidity;
  scd4x.readMeasurement(co2, temperature, humidity);

  //Add to message
  messageText += "Air Humidity=";
  messageText += humidity;
  messageText += ", Celsius temperature=";
  messageText += temperature;
  messageText += ", CO2=";
  messageText += co2;
  messageText += ", Soil humidity=";
  messageText += soil;
  messageText += ", Light Sensor value=";
  messageText += lumStatus;

  Serial1.println(messageText);
  waitingToStart = true;

  //response loop
  while (waitingToStart == true)
  {
    String value = Serial1.readString();
    if (value == "Restart")
    {
      waitingToStart = false;
    }
    for (int i = 0; i < lengthOfCodesArray; i++)
    {
      if (value == codes[i])
      {
        LightChanger(i);
      }
    }
  }
  Serial.println("Restarting");
  waitingToStart = true;
}

void LightChanger(int indexValue)
{ if (indexValue == 0) {
    //digitalWrite(blue, LOW);
    //low air
  }
  else if (indexValue == 1) {
    //digitalWrite(blue, HIGH);
    //hgih air
  }
  else if (indexValue == 2) {
    //digitalWrite(blue, LOW);
    //low soil
  }
  else if (indexValue == 3) {
    //digitalWrite(blue, HIGH);
    //high soil
  }
  else if (indexValue == 4) {
    //digitalWrite(yellow, LOW);
    //low light
    flashYellow = true;
  }
  else if (indexValue == 5) {
    //digitalWrite(yellow, HIGH);
    //high light
    yellowOn = true;
  }

  else if (indexValue == 6) {
    //digitalWrite(red, LOW);
    //low temp
    flashRed = true;
  }
  else if (indexValue == 7) {
    //digitalWrite(red, HIGH);
    //high temp
    redOn = true;
  }
  else if (indexValue == 8) {
    //digitalWrite(green, LOW);
    //low co2
    flashGreen = true;
  }
  else if (indexValue == 9) {
    //digitalWrite(green, HIGH);
    //high co2
    greenOn = true;
  }
  Serial.println("Value Running " + codes[indexValue]);
}

void lightFlasher()
{
  if (flashYellow)
  {
    //low light
    digitalWrite(yellow, HIGH);
    delay(300);
    digitalWrite(yellow, LOW);
  }
  if (flashRed)
  {
    //low temp
    digitalWrite(red, HIGH);
    delay(300);
    digitalWrite(red, LOW);
  }
  if (flashBlue)
  {
    //UNSURE
    digitalWrite(blue, HIGH);
    delay(300);
    digitalWrite(blue, LOW);
  }
  if (flashGreen)
  {
    //low co2
    digitalWrite(green, HIGH);
    delay(300);
    digitalWrite(green, LOW);
  }
  if (yellowOn)
  {
    //high light
    digitalWrite(yellow, HIGH);
  }
  if (redOn)
  {
    // high temp
    digitalWrite(red, HIGH);
  }
  if (blueOn)
  {
    //UNSURE
    digitalWrite(blue, HIGH);
  }
  if (greenOn)
  {
    //high co2
    digitalWrite(green, HIGH);
  }
}
