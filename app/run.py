from flask import Flask, render_template
import paho.mqtt.client as mqtt
import threading
import time

broker="ec2-184-73-26-207.compute-1.amazonaws.com"
port=1883
name="website"
secret="4444"

app = Flask(__name__,template_folder='templates')

_Time=time.ctime(time.time())
_Date=11/15/24
_Temp=34
_AHumid=22
_SHumid=22
_CO2=25
_Light=50

    
@app.route('/')
def home():
    global _Time
    global _Date
    global _Temp
    global _AHumid
    global _CO2
    global _Light
    global _SHumid
    
    while True:
        time.sleep(5)
        _Time=time.ctime(time.time())
        #turbo.push(turbo.replace(render_template('template-new.html',time=_Time,date=_Date,temp=_Temp,humid=_Humid,co2=_CO2,light=_Light),target='card'))
        #return turbo.stream(turbo.append(render_template('template-new.html', time=_Time,date=_Date,temp=_Temp,humid=_Humid,co2=_CO2,light=_Light), 'card'))
        return render_template('template-new.html', time=_Time,date=_Date,temp=_Temp,ahumid=_AHumid,co2=_CO2,light=_Light,shumid=_SHumid)

def on_connect(client, userdata, flags, rc): # func for making connection
    print("Connected to MQTT")
    print("Connection return result: " +str(rc))
    client.subscribe([("Air Humidity",0),("Celsius Temperature",0),("Soil Humidity",0),("Light Level",0),("CO2",0)])
    
def on_message(client, userdata, msg): # Func for sending msg
    global _Time
    global _Date
    global _Temp
    global _AHumid
    global _CO2
    global _Light
    global _SHumid
    
    _TIME = time.ctime(time.time())
    
    if str(msg.topic)==str("Air Humidity"):
        _AHumid=float(msg.payload)
        
    if str(msg.topic)==str("Celsius Temperature"):
        _Temp=float(msg.payload)
        
    if str(msg.topic)==str("Soil Humidity"):
        _SHumid=float(msg.payload)
        
    if str(msg.topic)==str("Light Level"):
        _Light=float(msg.payload)
        
    if str(msg.topic)==str("CO2"):
        _CO2=float(msg.payload)

homeThread = threading.Thread(target = home)
homeThread.start()

_ard_one_client = mqtt.Client()
_ard_one_client.username_pw_set(username=name,password=secret)

try:
    _ard_one_client.on_connect = on_connect
    _ard_one_client.on_message = on_message
    _ard_one_client.connect(broker, port)
    _ard_one_client.loop_forever()
except:
    print("Error Connecting")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
