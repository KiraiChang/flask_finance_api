from common.db import db
from sqlalchemy import desc


class FundModel(db.Model):
    __bind_key__ = 'finance'
    __tablename__ = 'funds'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80))
    price = db.Column(db.Float)

    def __init__(self,
                 date,
                 price,
                 ):
        self.date = date
        self.price = price

    def json(self):
        return {
            'date': self.date,
            'price': self.price,
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
