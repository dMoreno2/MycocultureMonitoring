from flask import Flask, render_template
from flask_mqtt import Mqtt
import threading
import time


app = Flask(__name__,template_folder='templates')

app.config['MQTT_BROKER_URL'] = 'ec2-54-156-152-164.compute-1.amazonaws.com'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = 'website'  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = '4444'  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # se

_Time=time.ctime(time.time())
_Date='1'
_Temp='1'
_AHumid='1'
_SHumid='1'
_CO2 = '1'
_Light='1'

mqtt = Mqtt()

def create_app():
    app = Flask(__name__)
    mqtt.init_app(app)
    
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
        _Time=time.ctime(time.time())
        #turbo.push(turbo.replace(render_template('template-new.html',time=_Time,date=_Date,temp=_Temp,humid=_Humid,co2=_CO2,light=_Light),target='card'))
        #return turbo.stream(turbo.append(render_template('template-new.html', time=_Time,date=_Date,temp=_Temp,humid=_Humid,co2=_CO2,light=_Light), 'card'))
        return render_template('template-new.html', time=_Time,temp=_Temp,ahumid=_AHumid,co2=_CO2,light=_Light,shumid=_SHumid)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc): # func for making connection
    print("Connected to MQTT")
    print("Connection return result: " +str(rc))
    mqtt.subscribe([("Air Humidity",0),("Celsius Temperature",0),("Soil Humidity",0),("Light Level",0),("CO2",0)])

@mqtt.on_message()  
def handle_mqtt_message(client, userdata, msg): # Func for sending msg
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)