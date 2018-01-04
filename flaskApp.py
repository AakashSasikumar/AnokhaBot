from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import Bot
app = Flask(__name__)
api = Api(app)

class getResponse(Resource):
    def get(self, query):
        reply = Bot.response(query)
        dc = {}
        dc['reply'] = reply
        return dc
        
api.add_resource(getResponse, '/getResponse/<query>')


if __name__ == '__main__':
     app.run(port=3128)