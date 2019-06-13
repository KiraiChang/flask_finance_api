# pylint:disable=E1101
# for ignore app.logger no method of addHandler
import os
import logging
from flask import Flask
from flask_restful import Api
from resource.golds import GoldsResource
from resource.funds import FundsResource
from resource.stocks import StocksResource
from resource.exchanges import ExchangesResource
from resource.user import UserResource, UsersResource
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['PG_DATABASE_URL']
# app.config['SQLALCHEMY_BINDS'] = {
#    'finance': os.environ['PG_DATABASE_URL'],
#    'userdb': os.environ['PG_DATABASE_URL']
#}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(GoldsResource, '/golds/<string:date>')
api.add_resource(FundsResource, '/funds/<string:date>')
api.add_resource(StocksResource, '/stocks/<string:date>')
api.add_resource(ExchangesResource, '/exchanges/<string:date>')
api.add_resource(UserResource, '/user/<string:name>')
api.add_resource(UsersResource, '/users/')


class printMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        for key, value in environ.items():
            app.logger.debug('{0}={1}'.format(key, value))

        return self.app(environ, start_response)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    from common.db import db
    from common.ma import ma
    db.init_app(app)
    ma.init_app(app)
    app.debug = True
    app.secret_key = 'SuperSecretKey'
    # app.wsgi_app = printMiddleware(app.wsgi_app)

    # logging
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    # run
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 5000)))
