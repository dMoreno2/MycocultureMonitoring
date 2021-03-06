import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import threading as thread
import serial
import time
import string
import sys

broker=""
port=443
name=""
secret=""

messaging = True
waitingForStart = True
message_Queue= []

_ard_Serial=serial.Serial("/dev/rfcomm1", 9600)
#_ard_Serial.write(str.encode('Restart'))

def on_connect(client, userdata, flags, rc): # func for making connection
    print("Connected to MQTT")
    print("Connection return result: " +str(rc))
    client.subscribe([("Air Humidity",0),("Celsius Temperature",0),("Soil Humidity",0),("Light Level",0),("CO2 Level",0)])

def PublishLoop():
    global waitingForStart
    global messaging
    global _ard_Serial
    #_ard_Serial.write(str.encode('Restart'))
    #_ard_Serial.write(str.encode('Start'))
    while messaging:
        while waitingForStart:
            _ard_Serial.write(str.encode('Start'))
            encodedSerial = _ard_Serial.readline()
            decodedSerial = encodedSerial.decode('utf-8').strip('\r\n')
            if decodedSerial == "Start":
                waitingForStart = False
            else:
                time.sleep(0.001)
                _ard_Serial.write(str.encode('Start'))
                print('txt')
                
        encodedSerial = _ard_Serial.readline()
        decodedSerial = encodedSerial.decode('utf-8').strip('\r\n')
        print(decodedSerial)
        
        #Split the decoded input at the ,
        x = decodedSerial.strip().split(',')
        
        #Split already split values and take numbers after the =
        airHumidity = x[0].split('=')
        tempC = x[1].split('=')
        co2 = x[2].split('=')
        soilHumidity = x[3].split('=')
        lum = x[4].split('=')

        #Publish numbers to topics.
        _ard_one_client.publish("CSV",encodedSerial)
        _ard_one_client.publish("Air Humidity", (float(airHumidity[1])))
        _ard_one_client.publish("Celsius Temperature", (float(tempC[1])))
        _ard_one_client.publish("CO2 Level", (float(co2[1])))
        _ard_one_client.publish("Soil Humidity", (float(soilHumidity[1])))
        _ard_one_client.publish("Light Level", (float(lum[1])))
        #Publish numbers to topics.
#         publish.single("CSV",encodedSerial,hostname=broker)
#         publish.single("Air Humidity", (float(airHumidity[1])), hostname=broker)
#         publish.single("Celsius Temperature", (float(tempC[1])), hostname=broker)
#         publish.single("CO2 Level", (float(co2[1])), hostname=broker)
#         publish.single("Soil Humidity", (float(soilHumidity[1])), hostname=broker)
#         publish.single("Light Level", (float(lum[1])), hostname=broker)
        waitingForStart = True
        time.sleep(4)
        MessageOut()

def on_message(client, userdata, msg): # Func for sending msg
    global message_Queue
    
    if str(msg.topic)==str("Air Humidity"):
        if float(msg.payload)>=float(50):
            #print("Air Humidity is high!")
            message_Queue.append('High Air')
        else:
            #print("Air Humidity is low!")
            message_Queue.append('Low Air')
            
    time.sleep(0.1)
    if str(msg.topic)==str("Soil Humidity"): 
        if float(msg.payload)>=float(50):
            #print("Soil Humidity is high!")
            message_Queue.append('High Soil')
        else:
            #print("Soil Humidity is low!")
            message_Queue.append('Low Soil')

    time.sleep(0.1)
    if str(msg.topic)==str("Celsius Temperature"):
        if float(msg.payload)>=float(50):
            #print("Soil Humidity is high!")
            message_Queue.append('High Temp')
        else:
            #print("Soil Humidity is low!")
            message_Queue.append('Low Temp')
            
    time.sleep(0.1)
    if str(msg.topic)==str("Light Level"):
        if float(msg.payload)>=float(50):
            #print("Light level is high!")
            message_Queue.append('High Light')
        else:   
            #print("Light level is low!")
            message_Queue.append('Low Light')
            
    time.sleep(0.1)
    if str(msg.topic)==str("CO2 Level"):
        if float(msg.payload)>=float(50):
            #print("Light level is high!")
            message_Queue.append('High CO2')
        else:   
            #print("Light level is low!")
            message_Queue.append('Low CO2')

def MessageOut():
    global messaging
    global message_Queue
    global _ard_Serial
    while len(message_Queue)>0:
        time.sleep(4)
        messageText = str.encode(message_Queue.pop(0))
        _ard_Serial.write(messageText)
        print(messageText)
        time.sleep(4)
    _ard_Serial.write(str.encode('Restart'))
    time.sleep(2)
    print('ReStart')
        
def OnKeyExit():
    global messaging
    global waitingToStart
    global message_Queue
    global publishThread
    while messaging == True:
        userInput = input()
        if userInput =='q':
            print("Program Execution Ended")
            messaging = False
            exit()

_ard_one_client = mqtt.Client()
_ard_one_client.username_pw_set(username=name,password=secret)

publishThread = thread.Thread(target = PublishLoop)
publishThread.start()

exitThread = thread.Thread(target = OnKeyExit)
exitThread.start()

try:
    _ard_one_client.on_connect = on_connect
    _ard_one_client.on_message = on_message
    _ard_one_client.connect(broker, port)
    _ard_one_client.loop_forever()
except:
    print("Error Connecting")
