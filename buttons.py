from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardMarkup,MessageEntity
from telegram import Update,KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from backend import DB
data = DB()

class buttons:
    data.__init__()
    def __init__(self):
        self.t1, self.t2 = ("📱Raqam yuborish","📱 Отправить номер")
        self.b1, self.b2 = ("🇺🇿 Ўзбекча", "🇷🇺 Руский")
        

    def t_button_uz(self):
        return ReplyKeyboardMarkup([[KeyboardButton(self.t1, request_contact=True)]], resize_keyboard=True, one_time_keyboard=True)
    
    def t_button_ru(self):
        return ReplyKeyboardMarkup([[KeyboardButton(self.t2, request_contact=True)]], resize_keyboard=True, one_time_keyboard=True)

    def b_button(self):
        return ReplyKeyboardMarkup([[self.b1], [self.b2]],
                                   resize_keyboard=True, one_time_keyboard=True)
