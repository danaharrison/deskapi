from flask import Flask
from flask_restful import Api, Resource, reqparse
from resources.desk import Desk
from resources.quotes import Quote
#import RPi.GPIO as GPIO
import random

app = Flask(__name__)
api = Api(app)

api.add_resource(Quote, "/ai-quotes", "/ai-quotes/", "/ai-quotes/<int:id>")
api.add_resource(Desk, "/desk", "/desk/", "/desk/<string:direction>")

if __name__ == '__main__':
	#app.run(debug=True)
	app.run(host = '0.0.0.0')
