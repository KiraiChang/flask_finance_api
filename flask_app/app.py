# pylint:disable=E1101
# for ignore app.logger no method of addHandler
import os
import logging
from flask import Flask
from flask_restful import Api
from resource.golds import Golds
from resource.funds import Funds
from resource.stocks import Stocks
from resource.exchanges import Exchanges
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
api = Api(app)

api.add_resource(Golds, '/golds/<string:date>')
api.add_resource(Funds, '/funds/<string:date>')
api.add_resource(Stocks, '/stocks/<string:date>')
api.add_resource(Exchanges, '/exchanges/<string:date>')

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'SuperSecretKey'

    # logging
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # run
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 5000)))
