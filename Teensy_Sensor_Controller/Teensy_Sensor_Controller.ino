#include "DHT.h"
#include <Arduino.h>
#include <SensirionI2CScd4x.h>
#include <Wire.h>

//Soilmoisture analog and power pins
#define soilPower 2
#define soilMoisture A1

//Photoresistor pin number
#define photoResistor A2

//Air humidity and heat
#define DHTPIN 21      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
#define LEDPIN 11
DHT dht(DHTPIN, DHTTYPE);
SensirionI2CScd4x scd4x;

//Define LED pins.
#define blue 3
#define yellow 1
#define red 0

//RX and TX pins
#define rxPin 7
#define txPin 8

bool waitingToStart = true;

//String value;
String codes[10] = {"Low Air", "High Air", "Low Soil", "High Soil", "Low Light", "High Light","Low Temp","High Temp","Low CO2","High CO2"};
int lengthOfCodesArray = 10;

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

  // Setup DHT Sensor
  pinMode(DHTPIN, INPUT);
  dht.begin();
}

void loop()
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

  //Reads/holds humidity and temperature data and converts heat data between fahrenheit and celsius
  float h = dht.readHumidity();
  float t = dht.readTemperature();

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
  delay(600000);
}

void LightChanger(int indexValue)
{
  if (indexValue == 0) {
    digitalWrite(red, LOW);
    //low air
  }
  else if (indexValue == 1) {
    digitalWrite(red, HIGH);
    //high air
  }
  else if (indexValue == 2) {
    digitalWrite(blue, LOW);
    //low soil
  }
  else if (indexValue == 3) {
    digitalWrite(blue, HIGH);
    //high soil
  }
  else if (indexValue == 4) {
    digitalWrite(yellow, LOW);
    //low light
  }
  else if (indexValue == 5) {
    digitalWrite(yellow, HIGH);
    //high light
  }
  else if (indexValue == 6) {
    digitalWrite(yellow, LOW);
    //low temp
  }
  else if (indexValue == 7) {
    digitalWrite(yellow, HIGH);
    //high temp
  }
  else if (indexValue == 8) {
    digitalWrite(yellow, LOW);
    //low co2
  }
  else if (indexValue == 9) {
    digitalWrite(yellow, HIGH);
    //high co2
  }
  Serial.println("Value Running " + codes[indexValue]);
}
