#!/usr/bin/python3
from flask import Flask, url_for, jsonify
from flask_cors import CORS
import time
import random

# import RPi.GPIO as GPIO
# from hx711 import HX711
# from w1thermsensor import W1ThermSensor

app = Flask(__name__)
CORS(app)

beerPin = 26
vodkaPin = 29


# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(7, GPIO.IN)  # Temp sensor DS18B20
# GPIO.setup(3, GPIO.IN)  # HX711 load sensor DT
# GPIO.setup(5, GPIO.OUT)  # HX711 load sensor SDK
# GPIO.setup(beerPin, GPIO.OUT, initial=GPIO.LOW)  # Output pin to solenoid BEER valve
# GPIO.setup(vodkaPin, GPIO.OUT, initial=GPIO.LOW)  # Output pin to solenoid VODKA valve

# try:
#     hx = HX711(3, 5)
#     hx.set_offset(8234508)  # This gets calibrated to zero the sensor
#     hx.set_reference_unit(-20.9993)
# except:
#     print("Load sensor error")
# try:
#     sensor = W1ThermSensor()
# except:
#     print("Temp sensor error")


@app.route('/api/temp', methods=['GET'])
def readGrams():
    temp = "{}".format(random.randrange(100,1000))
    return temp

@app.route('/api/pints', methods=['GET'])
def readPints():
    pints = "{}".format(random.randrange(100,1000))
    return pints


@app.route('/api/openBeer', methods=['GET'])
def dispenseBeer():
    try:
        GPIO.output(beerPin, GPIO.HIGH)
        # Adjust sleep time to reach desired volume.
        time.sleep(10)
        GPIO.output(beerPin, GPIO.LOW)
        return "SUCCESS"
    except:
        return "FAIL"

@app.route('/api/closeBeer', methods=['GET'])
def closeBeer():
    try:
        GPIO.output(beerPin, GPIO.HIGH)
        # Adjust sleep time to reach desired volume.
        time.sleep(10)
        GPIO.output(beerPin, GPIO.LOW)
        return "SUCCESS"
    except:
        return "FAIL"


@app.route('/api/openVodka', methods=['GET'])
def openVodka():
    try:
        GPIO.output(vodkaPin, GPIO.HIGH)
        # Adjust sleep time to reach desired volume.
        time.sleep(2)
        GPIO.output(vodkaPin, GPIO.LOW)
        return "SUCCESS"
    except:
        return "FAIL"


@app.route('/api/closeVodka', methods=['GET'])
def closeVodka():
    try:
        GPIO.output(vodkaPin, GPIO.HIGH)
        # Adjust sleep time to reach desired volume.
        time.sleep(2)
        GPIO.output(vodkaPin, GPIO.LOW)
        return "SUCCESS"
    except:
        return "FAIL"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    GPIO.cleanup()
