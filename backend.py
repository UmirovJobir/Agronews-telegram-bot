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
 ##### Translate

    text_message = {'uz':"""💬 Ўзингиз гувоҳи бўлган:\n
    🔹 Йўл транспорт ҳодисалари
    🔹 Спорт тадбирлари ва
    🔹 Бошқа қизиқарли ҳодисаларни\n\nтасвирга олиб, вақти, жойи куни, каби маълумотлари билан биргаликда бизга юборинг.""", 
    'ru': """💬 Если вы были свидетелями:\n
    🔹 Дорожно-транспортные происшествия
    🔹 Спортивные мероприятия и
    🔹 Записывайте другие интересные события и присылайте их нам вместе с информацией: время, место, день и т. д."""}

    xurmatli = {'uz':"Ҳурматли", 'ru':"Уважаемый"}

    phone_text = {'uz':'Телефон рақамингизни +9989** *** ** **\nшаклда юборинг,ёки "📱 Рақам юбориш"\nтугмасини босинг:', 
    'ru': 'Отправьте свой номер телефона в форме +9989** *** ** **\ или нажмите кнопку "📱 Отправить номер"\n'}
