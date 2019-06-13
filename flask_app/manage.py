import os

from flask import Flask
from common.db import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models.gold import GoldModel
from models.fund import FundModel
from models.stock import StockModel
from models.exchange import ExchangeModel
from models.user import UserModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['PG_DATABASE_URL']
# app.config['SQLALCHEMY_BINDS'] = {
#    'finance': os.environ['PG_DATABASE_URL'],
#    'userdb': os.environ['PG_DATABASE_URL']
#}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db) # this

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()