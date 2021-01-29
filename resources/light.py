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

        colour = args['colour']
        if args['brightness'] is not None:
            brightnessArg = float(args['brightness'])
            if 0.10 <= brightnessArg <= 1.00:
                brightness = brightnessArg

        #print( f"Colour is {colour} and brightness is {brightness}" )
        pixels = neopixel.NeoPixel(board.D21, 60, brightness=brightness)
        #print( f"Brightness argument is {brightnessArg}")

        #pixels = neopixel.NeoPixel(board.D21, 60, brightness = 0.2)
        #print(colour)
        if colour is not None:
            if colour == 'off':
                pixels.deinit()
            else:
                pixels.fill(webcolors.name_to_rgb(colour))
        else:
            return "No colour specified.", 400
