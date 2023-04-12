from flask_login import UserMixin
from sqlalchemy.sql import func

from .services import db

friendship = db.Table('friends',
                      db.Column('user_1_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('user_2_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))
    name = db.Column(db.String(150))
    chats = db.relationship('Chat')
    friends = db.relationship("User", secondary=friendship,
                              primaryjoin=id == friendship.c.user_1_id,
                              secondaryjoin=id == friendship.c.user_2_id)

    def befriend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            friend.friends.append(self)

    def unfriend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            friend.friends.remove(self)


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
