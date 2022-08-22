from gino import Gino
from sqlalchemy.dialects.postgresql import UUID

db = Gino()


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)
    registration_time = db.Column(db.DateTime, server_default=db.func.now())

    _idx1 = db.Index('app_user_name', 'user_name', unique=True)

    def to_dict(self):
        return {
            'user_name': self.user_name,
            'password': self.password,
            'salt': self.salt,
            'registration_time': int(self.registration_time.timestamp()),
            'id': self.id,
        }


class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(UUID, primary_key=True)
    creation_time = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'user_name': self.user_id,
            'id': str(self.id),
            'registration_time': int(self.creation_time.timestamp()),
        }


class AdsModel(db.Model):
    __tablename__ = "ads"
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    _idx1 = db.Index('app_ads_head', 'head', unique=False)

    def to_dict(self):
        return {
            'head': self.head,
            'body': self.body,
            'creation_time': int(self.creation_time.timestamp()),
            'id': self.id,
            'user_id': self.user_id
        }
