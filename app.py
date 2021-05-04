from flask import Flask, url_for, jsonify
from flask_cors import CORS
import time

import RPi.GPIO as GPIO
from hx711 import HX711
from w1thermsensor import W1ThermSensor

app = Flask(__name__)
CORS(app)

beerPin = 25
vodkaPin = 26


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO.setup(4, GPIO.IN)  # Temp sensor DS18B20
GPIO.setup(2, GPIO.IN)  # HX711 load sensor DT
GPIO.setup(3, GPIO.OUT)  # HX711 load sensor SDK
GPIO.setup(beerPin, GPIO.OUT)  # Output pin to solenoid BEER valve
GPIO.output(beerPin, GPIO.HIGH)  # Start off
GPIO.setup(vodkaPin, GPIO.OUT)  # Output pin to solenoid VODKA valve
GPIO.output(vodkaPin, GPIO.HIGH)  # Start off

try:
    hx = HX711(dout=2, pd_sck=3)
    hx.set_offset(8234508)  # This gets calibrated to zero the sensor
    hx.set_scale(-20.9993)
except Exception as e:
    print(e)
try:
    sensor = W1ThermSensor()
except Exception as e:
    print(e)


@app.route('/api/sensors', methods=['GET'])
def readSensors():
    sensorData = {
        'temp': 'err',
        'grams': 'err'
    }
    try:
        sensorData['temp'] = sensor.get_temperature()
    except Exception as e:
        sensorData['temp'] = e
        # sensorData['temp'] = 9999

        # TODO MOVE THE EQUATION BELOW TO FRONTEND
        # pintConversion = int((grams - 4250)*0.002)  # dry weight of keg is ca. 4250g
        # if pintConversion < 0:
        #     pintConversion = 0
    try:
        sensorData['grams'] = hx.get_grams(times=1)
    except Exception as e:
        print(e)
    return jsonify(sensorData)


@app.route('/api/dispenseBeer', methods=['GET'])
def dispenseBeer():
    try:
        GPIO.output(beerPin, GPIO.LOW)
        # Adjust sleep time to reach desired volume.
        time.sleep(10)
        GPIO.output(beerPin, GPIO.HIGH)
        return "SUCCESS"
    except:
        return "FAIL"


@app.route('/api/dispenseVodka', methods=['GET'])
def dispenseVodka():
    try:
        GPIO.output(vodkaPin, GPIO.LOW)
        # Adjust sleep time to reach desired volume.
        time.sleep(2)
        GPIO.output(vodkaPin, GPIO.HIGH)
        return "SUCCESS"
    except:
        return "FAIL"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    GPIO.cleanup()
