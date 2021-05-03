#!/usr/bin/env python3
from flask import Flask, url_for
from flask_cors import CORS
import time

try:
    import RPi.GPIO as GPIO
    from hx711 import HX711
    from w1thermsensor import W1ThermSensor
except:
    print("No compatible SBC detected!")
    print("GPIO, hx711, w1thermsensor are NOT imported.")

app = Flask(__name__)
CORS(app)

beerPin = 37
vodkaPin = 38

try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.IN)  # Temp sensor DS18B20
    GPIO.setup(3, GPIO.IN)  # HX711 load sensor DT
    GPIO.setup(5, GPIO.IN)  # HX711 load sensor SDK
    GPIO.setup(beerPin, GPIO.OUT)  # Output pin to solenoid BEER valve
    GPIO.setup(vodkaPin, GPIO.OUT)  # Output pin to solenoid VODKA valve
except:
    class GPIO():
        def output(pin, status):
            print("Simulating gpio{}, status: {}".format(pin, status))
        HIGH = "GPIO.HIGH"
        LOW = "GPIO.LOW"

        def cleanup():
            print("Simulating GPIO.cleanup()")

try:
    hx = HX711(dout=3, pd_sck=5)
    hx.set_offset(8234508)  # This gets calibrated to zero the sensor
    hx.set_scale(-20.9993)
except:
    class hx():
        def get_grams(times=1):
            return "n/a"
try:
    sensor = W1ThermSensor()
except:
    class sensor():
        def get_temperature():
            return "n/a"




@app.route('/api/temp', methods=['GET'])
def getTemp():
    try:
        tempRead = sensor.get_temperature()
        temp = "{:.1f}".format(tempRead)
    except:
        temp = 999
    return "{}".format(temp)

@app.route('/api/pints', methods=['GET'])
def getPints():
    try:
        grams = hx.get_grams(times=1)
        pints = int((grams - 4250)*0.002)  # dry weight of keg is ca. 4250g
        if pints < 0:
            pints = 0
    except:
        pints = 999
    return "{}".format(pints)


@app.route('/api/dispenseBeer', methods=['POST'])
def dispenseBeer():
    try:
      GPIO.output(beerPin, GPIO.HIGH)
      # Adjust sleep time to reach desired volume.
      time.sleep(10)
      GPIO.output(beerPin, GPIO.LOW)
      return 1
    except:
      return 99


@app.route('/api/dispenseVodka', methods=['POST'])
def dispenseVodka():
    try:
      GPIO.output(vodkaPin, GPIO.HIGH)
      # Adjust sleep time to reach desired volume.
      time.sleep(2)
      GPIO.output(vodkaPin, GPIO.LOW)
      return 1
    except:
      return 99


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    GPIO.cleanup()
