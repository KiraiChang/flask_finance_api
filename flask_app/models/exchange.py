from common.db import db
from sqlalchemy import desc


class ExchangeModel(db.Model):
    __bind_key__ = 'finance'
    __tablename__ = 'exchanges'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80))
    usd_twd = db.Column(db.Float)
    eur_usd = db.Column(db.Float)
    gbp_usd = db.Column(db.Float)
    aud_usd = db.Column(db.Float)
    nzd_usd = db.Column(db.Float)

    def __init__(self,
                 date,
                 usd_twd,
                 eur_usd,
                 gbp_usd,
                 aud_usd,
                 nzd_usd,
                 ):
        self.date = date
        self.usd_twd = usd_twd
        self.eur_usd = eur_usd
        self.gbp_usd = gbp_usd
        self.aud_usd = aud_usd
        self.nzd_usd = nzd_usd

    def json(self):
        return {
            'date': self.date,
            'usd_twd': self.usd_twd,
            'eur_usd': self.eur_usd,
            'gbp_usd': self.gbp_usd,
            'aud_usd': self.aud_usd,
            'nzd_usd': self.nzd_usd
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
