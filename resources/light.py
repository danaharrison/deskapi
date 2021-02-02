from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_caching import Cache
import ..config as config
import board
import neopixel
import time
import webcolors

stripLength = config.leds['length']

class LightStats():
    def __init__(self, colour, brightness):
        self.colour = colour
        self.brightness = brightness

class Light(Resource):

    cache = Cache()

    def changeLight(colour, brightness):
        global stripLength
        pixels = neopixel.NeoPixel(board.D21, stripLength, brightness=brightness)

        if colour == 'rainbow':
            print("Nope, you disabled that.")
        elif colour is not None and brightness is not None:
            if colour == 'off' or brightness == 0.00:
                pixels.deinit()
                Light.cache.set('ledstrip', LightStats('off', 0.00))
            else:
                if type(colour) is not webcolors.IntegerRGB:
                    colourName = webcolors.name_to_rgb(colour)
                    pixels.fill(colourName)
                    Light.cache.set('ledstrip', LightStats(colourName, brightness))
                else:
                    pixels.fill(colour)
                    Light.cache.set('ledstrip', LightStats(webcolors.rgb_to_name(colour), brightness))

    def getLight():
        return Light.cache.get('ledstrip')

    def post(self):
        #Pull in colour and/or brightness from query parameters
        parser = reqparse.RequestParser()
        parser.add_argument('colour', type=str, required=False)
        parser.add_argument('brightness', type=str, required=False)
        args = parser.parse_args()

        #Set default values if none provided
        brightness = 0.5
        colour = 'white'

        #If neither are provided, return 400
        if args['brightness'] is None and args['colour'] is None:
            return f"Please specify either a brightness or colour.", 400

        if args['colour'] is not None:
            colour = args['colour']

        if args['brightness'] is not None:
            try:
                brightness = float(args['brightness'])
                if brightness < 0.00 or brightness > 1.00:
                    brightness = 0.5
            except:
                #Brightness of 0 will turn the strip off, as will colour 'off'
                return f"Brightness value {args['brightness']} not allowed; provide a value from 0.00 to 1.00", 400

        Light.changeLight(colour, brightness)

        return f"Colour: {colour} | Brightness: {brightness}", 200
