from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardMarkup,MessageEntity
from telegram import Update,KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from backend import DB
data = DB()

class buttons:
    data.__init__()
    def __init__(self):
        self.t1 = ("📱Raqam yuborish /📱 Отправить номер")

    def t_button(self):
        return ReplyKeyboardMarkup([[KeyboardButton(self.t1, request_contact=True)]], resize_keyboard=True, one_time_keyboard=True)
