from flask import Flask
from flask_restful import Api, Resource, reqparse
#from flask_caching import Cache
from resources.desk import Desk
from resources.light import Light
import random

app = Flask(__name__)
api = Api(app)
Light.cache.init_app(app, config={'CACHE_TYPE': 'simple'})
Light.changeLight('white', 0.5)

api.add_resource(Desk, "/desk", "/desk/", "/desk/<string:direction>")
api.add_resource(Light, "/light", "/light/", "/light/<string:colour>")

if __name__ == '__main__':
	#app.run(debug=True)
	app.run(host = '0.0.0.0')
