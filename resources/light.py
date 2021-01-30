from flask import Flask
from flask_restful import Api, Resource, reqparse
import board
import neopixel
import time
import webcolors

class Light(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('colour', type=str, required=False)
        parser.add_argument('brightness', type=str, required=False)
        args = parser.parse_args()
        brightness = 0.5

        if args['brightness'] is None and args['colour'] is None:
            return f"Please specify either a brightness or colour.", 400

        colour = args['colour']
        if args['brightness'] is not None:
            try:
                brightnessArg = float(args['brightness'])
                if 0.10 <= brightnessArg <= 1.00:
                    brightness = brightnessArg
            except:
                return f"Brightness value {args['brightness']} not allowed; provide a value from 0.10 to 1.00", 400

        pixels = neopixel.NeoPixel(board.D21, 60, brightness=brightness)

        if colour is not None:
            if colour == 'off':
                pixels.deinit()
            else:
                pixels.fill(webcolors.name_to_rgb(colour))
        else:
            return "No colour specified.", 400
        
        return "Good stuff.", 200