from flask import Flask
from flask_restful import Api, Resource, reqparse
from multiprocessing import Process
import RPi.GPIO as GPIO
import time

maxHeight = 125
minHeight = 50


def getHeight():

    try:
        #GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        PIN_TRIGGER = 5
        PIN_ECHO = 6

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        print("Waiting for sensor to settle")
        time.sleep(0.05)

        print("Calculating distance...")
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO) == 1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time

        distance = round(pulse_duration * 17150, 2)

        print(f"Distance: {distance} cm")

    finally:
        #GPIO.cleanup()
        return distance

def moveDesk(direction):
    gpioPin = -1

    if direction == 'up':
        gpioPin = 17
    elif direction == 'down':
        gpioPin = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpioPin, GPIO.OUT)
    #gpioState = GPIO.HIGH

    if direction == 'up':
        upHeight = getHeight()
        GPIO.output(gpioPin, GPIO.LOW)
        while upHeight < maxHeight - 2:
            upHeight = getHeight()
        GPIO.output(gpioPin, GPIO.HIGH)
    elif direction == 'down':
        downHeight = getHeight()
        GPIO.output(gpioPin, GPIO.LOW)
        while downHeight > minHeight + 2:
            downHeight = getHeight()
        GPIO.output(gpioPin, GPIO.HIGH)

    print(f"Moved desk {direction}")
    GPIO.cleanup()


class Desk(Resource):
    def get(self):
        return f"Height is {getHeight()}", 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('direction', type=str, required=False)
        #parser.add_argument('state', type=int, required=False)
        args = parser.parse_args()
        direction = args['direction']

        move_desk = Process(
            target=moveDesk,
            args=(direction,),
            daemon=True
        )
        move_desk.start()

        return f"Preparing to move desk in direction: {args['direction']}", 202
