from common.db import db
from sqlalchemy import desc


class StockModel(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.String(80))
    date = db.Column(db.String(80))
    open_price = db.Column(db.Float)
    max_price = db.Column(db.Float)
    min_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    decline = db.Column(db.Float)
    volume = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    def __init__(self,
                 stock_id,
                 date,
                 open_price,
                 max_price,
                 min_price,
                 close_price,
                 decline,
                 volume,
                 amount
                 ):
        self.stock_id = stock_id
        self.date = date
        self.open_price = open_price
        self.max_price = max_price
        self.min_price = min_price
        self.close_price = close_price
        self.decline = decline
        self.volume = volume
        self.amount = amount

    def json(self):
        return {
            'stock_id': self.stock_id,
            'date': self.date,
            'open_price': self.open_price,
            'max_price': self.max_price,
            'min_price': self.min_price,
            'close_price': self.close_price,
            'decline': self.decline,
            'volume': self.volume,
            'amount': self.amount
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
