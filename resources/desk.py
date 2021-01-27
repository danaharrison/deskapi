from flask import Flask
from flask_restful import Api, Resource, reqparse
import RPi.GPIO as GPIO
import time

height = 0

def getHeight():
        global height
        #Read value from height sensor here using RPi.GPIO
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
                if args['pin'] == 0 or args['pin'] == 1:
                        GPIO.setmode(GPIO.BCM)
                        GPIO.setup(18, GPIO.OUT)
                        GPIO.output(18, GPIO.HIGH)
                        time.sleep(5)
                        GPIO.output(18, GPIO.LOW)
                print(args)
                if direction.lower() == 'up':
                        while height <= 100: 
                                #Standing height here                        
                                height += 50
                                #Fire relay up here
                        return f"Moved desk {direction} to {height}.", 200
                elif direction.lower() == 'down':       
                        while height >= 50:
                                #Sitting height here                 
                                height -= 50
                                #Fire relay down here
                        return f"Moved desk {direction} to {height}.", 200
                else:
                        return f"{direction} is not a valid direction.", 500
