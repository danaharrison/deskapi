from flask import Flask
from flask_restful import Api, Resource, reqparse

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
