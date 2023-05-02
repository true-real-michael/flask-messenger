from flask_login import UserMixin
import sqlite3
from .init import Connection


class User(UserMixin):
    def __init__(self, user_id, email, password_hash, name):
        self.id = user_id
        self.email = email
        self.password_hash = password_hash
        self.name = name

    @property
    def friends(self):
        with Connection('instance/data.db') as conn:
            cur = conn.cursor()
            cur.execute(f"select * from friendship where user_a_id = {self.id} or user_b_id = {self.id}")
            fetch = cur.fetchall()
        return [find_user_by_id(fr[0] if fr[0] != self.id else fr[1]) for fr in fetch]

    def befriend(self, user):
        with Connection('instance/data.db') as conn:
            cur = conn.cursor()
            try:
                cur.execute(f"insert into friendship values ({self.id}, {user.id})")
            except Exception as e:
                print(e)
            conn.commit()

    def chat_with(self, user_id):
        pass


def find_user_by_id(user_id):
    with Connection('instance/data.db') as conn:
        cur = conn.cursor()
        cur.execute(f"select * from user where user_id = {user_id}")
        fetch = cur.fetchall()
    return None if len(fetch) == 0 else User(int(user_id), fetch[0][1], fetch[0][2], fetch[0][3])


def find_user_by_email(email):
    with Connection('instance/data.db') as conn:
        cur = conn.cursor()
        cur.execute(f"select * from user where email = '{email}'")
        fetch = cur.fetchall()
    return None if len(fetch) == 0 else User(int(fetch[0][0]), fetch[0][1], fetch[0][2], fetch[0][3])


def all_users():
    with Connection('instance/data.db') as conn:
        cur = conn.cursor()
        cur.execute("select * from user")
        fetch = cur.fetchall()
    return [User(int(user_fetch[0]), user_fetch[1], user_fetch[2], user_fetch[3]) for user_fetch in fetch]


user_id_incr = len(all_users()) - 1


def create_user(email, password_hash, name):
    global user_id_incr
    user_id_incr += 1

    with Connection('instance/data.db') as conn:
        cur = conn.cursor()
        cur.execute(f"insert into user values ({user_id_incr}, '{email}', '{password_hash}', '{name}')")
        conn.commit()
    return User(user_id_incr, email, password_hash, name)


class Friendship:
    def __init__(self, user_a_id, user_b_id):
        self.user_a_id = user_a_id
        self.user_b_id = user_b_id

    def chat_messages(self):
        pass


class Message:
    def __init__(self, user_src_id, user_dst_id, content, datetime):
        self.user_src_id = user_src_id
        self.user_dst_id = user_dst_id
        self.content = content
        self.datetime = datetime
