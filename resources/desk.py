from flask import Flask
from flask_restful import Api, Resource, reqparse

height = 0
class Desk(Resource):
        def get(self):
                return "Get method", 200

        def post(self, direction):
                global height
                if direction.lower() == 'up':                        
                        height += 50
                        return f"Moved desk {direction} to {height}.", 200
                elif direction.lower() == 'down':                        
                        height -= 50
                        return f"Moved desk {direction} to {height}.", 200
                else:
                        return f"{direction} is not a valid direction.", 500
