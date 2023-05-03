from pathlib import Path
import time

from .models import User, Message, Friendship
from .connection import Connection


class Database:
    def __init__(self, path: Path = Path('/instance/data.db')):
        self.path = path.resolve()
        if not self.path.exists():
            self.path.parent.mkdir(exist_ok=True)
            with Connection(self.path) as conn:
                cur = conn.cursor()
                cur.execute("""create table user (user_id       integer primary key,
                                                      email         text    not null,
                                                      password_hash text    not null,
                                                      name          text    not null)""")

                cur.execute("""create table friendship (user_a_id integer,
                                                            user_b_id integer,
                                                            primary key (user_a_id, user_b_id),
                                                            foreign key (user_a_id) references user(user_id),
                                                            foreign key (user_b_id) references user(user_id))""")

                cur.execute("""create table message (message_id  integer  primary key,
                                                         user_src_id integer  not null,
                                                         user_dst_id integer  not null,
                                                         content     text     not null,
                                                         timestamp   datetime not null,
                                                         foreign key (user_src_id) references user(user_id),
                                                         foreign key (user_dst_id) references user(user_id))""")
                conn.commit()

        with Connection(self.path) as conn:
            cur = conn.cursor()
            cur.execute("select count(*) from user")
            self.number_of_users = cur.fetchall()[0][0]
            cur.execute("select count(*) from message")
            self.number_of_messages = cur.fetchall()[0][0]

    def find_user_by_id(self, user_id):
        with Connection(self.path) as conn:
            cur = conn.cursor()
            cur.execute(f"select * from user where user_id = {user_id}")
            fetch = cur.fetchall()
        return None if len(fetch) == 0 else User(int(user_id), fetch[0][1], fetch[0][2], fetch[0][3])

    def find_user_by_email(self, email):
        with Connection(self.path) as conn:
            cur = conn.cursor()
            cur.execute(f"select * from user where email = '{email}'")
            fetch = cur.fetchall()
        return None if len(fetch) == 0 else User(int(fetch[0][0]), fetch[0][1], fetch[0][2], fetch[0][3])

    def all_users(self):
        with Connection(self.path) as conn:
            cur = conn.cursor()
            cur.execute("select * from user")
            fetch = cur.fetchall()
        return [User(int(user_fetch[0]), user_fetch[1], user_fetch[2], user_fetch[3]) for user_fetch in fetch]

    def create_user(self, email, password_hash, name):
        with Connection(self.path) as conn:
            cur = conn.cursor()
            cur.execute(f"insert into user values ({self.number_of_users}, '{email}', '{password_hash}', '{name}')")
            conn.commit()
        new_user = User(self.number_of_users, email, password_hash, name)
        self.number_of_users += 1
        return new_user

    def send_message(self, user_src_id, user_dst_id, content):
        timestamp = time.time()

        with Connection(self.path) as conn:
            cur = conn.cursor()
            cur.execute(f"insert into message values"
                        f"({self.number_of_messages},{user_src_id}, {user_dst_id}, '{content}', {timestamp})")
            conn.commit()

        self.number_of_messages += 1

    def friends_of(self, user_id):
        with Connection(self.path) as conn:
            cur = conn.cursor()
            cur.execute(f"select * from friendship where user_a_id = {user_id}")
            fetch = cur.fetchall()
        return [self.find_user_by_id(fr[1]) for fr in fetch]

    def follow(self, follower_id, followee_id):
        with Connection(self.path) as conn:
            cur = conn.cursor()
            cur.execute(f"insert into friendship values ({follower_id}, {followee_id})")
            conn.commit()

    def unfollow(self, follower_id, followee_id):
        with Connection(self.path) as conn:
            cur = conn.cursor()
            cur.execute(f"delete from friendship where user_a_id = {follower_id} and user_b_id = {followee_id}")
            conn.commit()

    def get_messages(self, user_a_id, user_b_id):
        with Connection(self.path) as conn:
            cur = conn.cursor()
            cur.execute(f"select * from message where user_dst_id = {user_a_id} and user_src_id = {user_b_id} "
                        f"or user_dst_id = {user_b_id} and user_src_id = {user_a_id}")
            fetch = cur.fetchall()
        return sorted([Message(msg[0],
                               self.find_user_by_id(msg[1]),
                               self.find_user_by_id(msg[2]),
                               msg[3],
                               msg[4]) for msg in fetch], key=lambda m: m.timestamp)
