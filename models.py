from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    # def __repr__(self):
    #     """Define a base way to print models"""
    #     return '%s(%s)' % (self.__class__.__name__, {
    #         column: value
    #         for column, value in self._to_dict().items()
    #     })
    #     print('SELF : ', self)

    # def json(self):
    #     """
    #             Define a base way to jsonify models, dealing with datetime objects
    #     """
    #     return {
    #         column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
    #         for column, value in self.to_dict().items()
    #     }


class Users(BaseModel, db.Model):
    """Model for the stations table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def to_json(self):
        return {
            "id": int(self.id),
            "name": self.name
        }
class Address(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
