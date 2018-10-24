from common.ma import ma
from marshmallow import validate
from models.user import UserModel


class UserSchema(ma.Schema):
    class Mate:
        model = UserModel
    id = ma.Int()
    name = ma.Str()
    email = ma.Email(required=True)
    password = ma.Str(required=True, validate=[
                      validate.Length(min=6, max=36)],)
