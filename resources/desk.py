from flask import Flask
from flask_restful import Api, Resource, reqparse
import RPi.GPIO as GPIO
import time

height = 50
maxHeight = 200
minHeight = 50


def getHeight():
    global height
    # Read value from height sensor here using RPi.GPIO
    return height


class Desk(Resource):
    def get(self):
        return f"Height is {getHeight()}", 200

    def post(self, direction):
        global height
        parser = reqparse.RequestParser()
        parser.add_argument('pin', type=int, required=False)
        parser.add_argument('state', type=int, required=False)
        args = parser.parse_args()
        GPIO.setmode(GPIO.BCM)
        gpioPin = -1
        gpioState = GPIO.LOW
        if args['pin'] == 0 or args['pin'] == 1 and args['state'] == 0 or args['state'] == 1:
            if args['pin'] == 0:
                gpioPin = 17
            elif args['pin'] == 1:
                gpioPin = 18

            if args['state'] == 1:
                gpioState = GPIO.HIGH
                print("Hello")
            if gpioPin != -1:
                GPIO.setup(gpioPin, GPIO.OUT)
                GPIO.output(gpioPin, gpioState)
                print(f"GPIO state is {GPIO.input(gpioPin)}")

            if direction.lower() == 'up':
                if height >= maxHeight:
                    return "Already at max height.", 500
                else:
                    while height < maxHeight:
                        # Standing height here
                        height += 1
                        # Fire relay up here
                    return f"Moved desk {direction} to {height}.", 200
            elif direction.lower() == 'down':
                if height <= minHeight:
                    return "Already at min height.", 500
                else:
                    while height > minHeight:
                        # Sitting height here
                        height -= 1
                        # Fire relay down here
                    return f"Moved desk {direction} to {height}.", 200
            else:
                return f"{direction} is not a valid direction.", 500
        else:
            return "Invalid pin or state value.", 500
