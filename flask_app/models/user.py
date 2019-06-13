from common.db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self):
        db.session.commit()

    @classmethod
    def get_user(cls, name):
        return cls.query.filter_by(name=name).first()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_user(cls):
        return cls.query.all()
