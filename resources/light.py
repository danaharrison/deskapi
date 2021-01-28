from flask import Flask
from flask_restful import Api, Resource, reqparse
import board
import neopixel
import time
import webcolors

class Light(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('colour', type=str, required=True)
        args = parser.parse_args()
        colour = args['colour']
        print(colour)

        pixels = neopixel.NeoPixel(board.D21, 60, brightness=0.2)
        
        #pixels.setBrightness(50)
        pixels.fill(webcolors.name_to_rgb(colour))
        time.sleep(2)
        #pixels.fill((255, 0, 0))
        #time.sleep(2)
        #pixels.fill((0, 0, 255))
        #time.sleep(2)
        pixels.fill((255, 255, 255))
        time.sleep(2)
        pixels.deinit()
