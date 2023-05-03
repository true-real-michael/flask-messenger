from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, email, password_hash, name):
        self.id = user_id
        self.email = email
        self.password_hash = password_hash
        self.name = name


class Friendship:
    def __init__(self, user_a_id, user_b_id):
        self.user_a_id = user_a_id
        self.user_b_id = user_b_id


class Message:
    def __init__(self, message_id, user_src, user_dst, content, timestamp):
        self.message_id = message_id
        self.user_src = user_src
        self.user_dst = user_dst
        self.content = content
        self.timestamp = timestamp
