import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('models/db.sqlite3', check_same_thread=False)
        self.cur = self.conn.cursor()

    def chack_user(self, chat_id):
        sql = f"select * from app_user where chat_id = {chat_id}"
        self.cur.execute(sql)
        b = 0
        for i in self.cur:
            if i:
                b = b + 1
        return b
    
    def count_users(self):
        sql = "select count(chat_id) from app_user"
        self.cur.execute(sql)
        for i in self.cur:
            return i[0]

    def select_user(self, chat_id):
        sql = f"select * from app_user where chat_id = {chat_id}"
        self.cur.execute(sql)
        for i in self.cur:
            return i[0]
    
    def insert_user_db(self, chat_id, name, phone, link):
        sql = f"insert into app_user (chat_id, name, phone, link, date) values({chat_id}, '{name}','{phone}','{link}', datetime('now', 'localtime'))"
        self.cur.execute(sql)
        self.conn.commit()

    def insert_post_db(self, text, user_id):
        sql = f"insert into app_post (text, user_id) values('{text}', {user_id})"
        self.cur.execute(sql)
        self.conn.commit()
 