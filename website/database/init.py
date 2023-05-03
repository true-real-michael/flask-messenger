import sqlite3
from pathlib import Path


class Connection:
    def __init__(self, path=Path('instance/data.db')):
        self.path = path

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def init():
    if not Path('instance/data.db').exists():
        Path('instance').mkdir(exist_ok=True)
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute("create table user ("
                        "user_id integer primary key,"
                        "email text not null,"
                        "password_hash text not null,"
                        "name text not null"
                        ")")
            cur.execute("create table friendship("
                        "user_a_id integer,"
                        "user_b_id integer,"
                        "primary key (user_a_id, user_b_id),"
                        "foreign key (user_a_id) references user(user_id),"
                        "foreign key (user_b_id) references user(user_id)"
                        ")")
            cur.execute("create table message ("
                        "message_id integer primary key,"
                        "user_src_id integer not null,"
                        "user_dst_id integer not null,"
                        "content text not null,"
                        "timestamp datetime not null,"
                        "foreign key (user_src_id) references user(user_id),"
                        "foreign key (user_dst_id) references user(user_id)"
                        ")")
            conn.commit()


if __name__ == '__main__':
    init()
