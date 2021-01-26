from flask import Flask
from flask_restful import Api, Resource, reqparse

ai_quotes = [
    {
        "id": 0,
        "author": "Kevin Kelly",
        "quote": "The business plans of the next 10,000 startups are easy to forecast: " +
                 "Take X and add AI." 
    },
    {
        "id": 1,
        "author": "Stephen Hawking",
        "quote": "The development of full artificial intelligence could " +
                 "spell the end of the human race. " +
                 "It would take off on its own, and re-design " +
                 "itself at an ever increasing rate. " +
                 "Humans, who are limited by slow biological evolution, " + 
                 "couldn't compete, and would be superseded."
    }
]

class Quote(Resource):

	def get(self, id=0):
		if id == 0:
			return random.choice(ai_quotes), 200

		for quote in ai_quotes:
			if(quote["id"] == id):
				return quote, 200
		return "Quote not found", 404

	def post(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument("author")
		parser.add_argument("quote")
		params = parser.parse_args()

		for quote in ai_quotes:
			if(id == quote["id"]):
				return f"Quote with id {id} already exists", 400

		quote = {
			"id": int(id),
			"author": params["author"],
			"quote": params["quote"]
		}

		ai_quotes.append(quote)
		return quote, 201

	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument("author")
		parser.add_argument("quote")
		params = parser.parse_args()

		for quote in ai_quotes:
			if(id == quote["id"]):
				quote["author"] = params["author"]
				quote["quote"] = params["quote"]
				return quote, 200

		quote = {
			"id": id,
			"author": params["author"],
			"quote": params["quote"]
		}

		ai_quotes.append(quote)
		return quote, 201

	def delete(self, id):
		global ai_quotes
		ai_quotes = [quote for quote in ai_quotes if quote["id"] != id]
		return f"Quote with id {id} is deleted.", 200