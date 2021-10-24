import time
import string
import threading as thread
import csv

messaging = True

header = ["Time","Air Humidity","Celsius Temperature","Soil Humidity","Light Level,CO2 Level"]
f = open('Results.CSV','w', newline='')
writer = csv.writer(f)
writer.writerow(header)

_TIME #time recived
_AirHumiddity #air humiddity value
_Temp #air temp
_SoilHumid #soil humiddity
_LightLvl #photosensitive level
_CO2 #co2 level

def OnKeyExit():
    global messaging
    global OnKeyExit
    while messaging == True:
        userInput = input()
        if userInput =='q':
            messaging = False
            f.close()
            print("Program Execution Ended")

def CSVOutput():
    global _TIME #time recived
    global _AirHumiddity #air humiddity value
    global _Temp #air temp
    global _SoilHumid #soil humiddity
    global _LightLvl #photosensitive level
    global _CO2 #co2 level

    writer.writerow([_TIME,_AirHumiddity,_Temp,_SoilHumid,_LightLvl,_CO2])

def on_connect(client, userdata, flags, rc): # func for making connection
    print("Connected to MQTT")
    print("Connection return result: " +str(rc))
    client.subscribe([("Air Humidity",0),("Celsius Temperature",0),("Soil Humidity",0),("Light Level",0),("CO2",0)])
    
def on_message(client, userdata, msg): # Func for sending msg
    global _TIME #time recived
    global _AirHumiddity #air humiddity value
    global _Temp #air temp
    global _SoilHumid #soil humiddity
    global _LightLvl #photosensitive level
    global _CO2 #co2 level

    _TIME = time.ctime(time.time())
    
    if str(msg.topic)==str("Air Humidity"):
        _AirHumiddity=float(msg.payload)
        
    if str(msg.topic)==str("Celsius Temperature"):
        _Temp=float(msg.payload)
        
    if str(msg.topic)==str("Soil Humidity"):
        _SoilHumid=float(msg.payload)
        
    if str(msg.topic)==str("Light Level"):
        _LightLvl=float(msg.payload)
        
    if str(msg.topic)==str("CO2"):
        _CO2=float(msg.payload)

    time.sleep(1)
    CSVOutput()
    
OnKeyExit = thread.Thread(target = OnKeyExit)
OnKeyExit.start()

try:
    _ard_one_client.on_connect = on_connect
    _ard_one_client.on_message = on_message
    _ard_one_client.connect("localhost", 1883, 60)
    _ard_one_client.loop_forever()
except:
    print("Error Connecting")
    
f.close()

