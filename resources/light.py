from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_caching import Cache
import board
import neopixel
import time
import webcolors

def wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait, pixels, num_pixels):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

stripLength = 60

class Light(Resource):

    cache = Cache()

    def changeLight(colour, brightness):
        global stripLength
        pixels = neopixel.NeoPixel(board.D21, stripLength, brightness=brightness)

        if colour == 'rainbow':
            rainbow_cycle(1, pixels, stripLength)
            Light.cache.set('colour', 'rainbow')
        elif colour is not None and brightness is not None:
            if colour == 'off' or brightness == 0.00:
                pixels.deinit()
                Light.cache.set('colour', 'off')
            else:
                if type(colour) is not webcolors.IntegerRGB:
                    colourName = webcolors.name_to_rgb(colour)
                    pixels.fill(colourName)
                    Light.cache.set('colour',colourName)
                else:
                    pixels.fill(colour)
                    Light.cache.set('colour',webcolors.rgb_to_name(colour))

    def getColour():
        return Light.cache.get('colour')

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
