from common.db import db
from sqlalchemy import desc


class GoldModel(db.Model):
    __bind_key__ = 'finance'
    __tablename__ = 'golds'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80))
    buy = db.Column(db.Float)
    sell = db.Column(db.Float)

    def __init__(self,
                 date,
                 buy,
                 sell,
                 ):
        self.date = date
        self.buy = buy
        self.sell = sell

    def json(self):
        return {
            'date': self.date,
            'buy': self.buy,
            'sell': self.sell,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def save_list_to_db(cls, list):
        for item in list:
            db.session.add(item)
        db.session.commit()

    @classmethod
    def get_by_date(cls, date):
        return cls.query.filter(cls.date >= date).order_by(desc(cls.date))

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_max_date(cls):
        return cls.query.order_by(desc(cls.date)).limit(1).first().date
