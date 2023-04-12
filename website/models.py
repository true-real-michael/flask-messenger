from flask_login import UserMixin
from sqlalchemy.sql import func

from .services import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))
    name = db.Column(db.String(150))
    chats = db.relationship('Chat')


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship('Message')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_data = db.Column(db.String(10000))
    message_date = db.Column(db.DateTime(timezone=True), default=func.now())
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
