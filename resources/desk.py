from flask import Flask
from flask_restful import Api, Resource, reqparse

class Desk(Resource):
        def get(self):
                return "Get method", 200

        def post(self, direction):
		if direction.lower() == 'up' or direction.lower() == 'down':
                        return f"Moved desk in {direction}.", 200
		else:
                        return f"{direction} is not a valid direction.", 500
