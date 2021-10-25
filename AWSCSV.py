import time
import paho.mqtt.client as mqtt
import string
import threading as thread
import csv

messaging = True
_Time="TIME"#time recived
_CSV=""


#f = open('Results.CSV','w', newline='')
#writer = csv.writer(f)
#writer.writerow(header)

writer = open('Results.CSV','a')
writer.seek(0,2)
writer.writelines("\r")
writer.writelines( (',').join([_Time,_CSV,]))

def OnKeyExit():
    global messaging
    global OnKeyExit
    while messaging == True:
        userInput = input()
        if userInput =='q':
            messaging = False
            writer.close()
            print("Program Execution Ended")

def CSVOutput():
    global _Time#time recived
    global _CSV

    
    writer = open('Results.CSV','a')
    writer.seek(0,2)
    writer.writelines("\r")
    writer.writelines( (',').join([_Time,_CSV]))

def on_connect(client, userdata, flags, rc): # func for making connection
    print("Connected to MQTT")
    print("Connection return result: " +str(rc))
    client.subscribe("CSV")
 
def on_message(client, userdata, msg): # Func for sending msg
    global _Time#time recived
    global _CSV
    _Time= time.ctime(time.time())
    
  
    _CSV=str(msg.payload)
    print(msg.payload)
    print(_Time)

    time.sleep(1)
    CSVOutput()
    
OnKeyExit = thread.Thread(target = OnKeyExit)
OnKeyExit.start()

_ard_one_client = mqtt.Client()
_ard_one_client.username_pw_set(username="", password="")
try:
    _ard_one_client.on_connect = on_connect
    _ard_one_client.on_message = on_message
    _ard_one_client.connect("", , 60)
    _ard_one_client.loop_forever()
except:
    print("Error Connecting")
    
writer.close()
