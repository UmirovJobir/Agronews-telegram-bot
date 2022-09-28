from email import message
from telegram import Update, MessageEntity
from telegram.ext import CallbackContext, MessageHandler, Updater, CommandHandler, ConversationHandler, Filters
from datetime import date

from backend import DB
from buttons import buttons
data = DB()
button = buttons()

STATE_BEGIN = 1
STATE_PHONE = 2
STATE_MESSAGE = 3
STATE_CHECK = 4
STATE_TEXT = 5

 

def start(update: Update, context: CallbackContext):
    context.bot.send_photo(chat_id = update.effective_message.chat_id, photo = open('img/agronews.jpg','rb'), 
        caption = f'🇺🇿 Ассалому алайкум! Келинг, аввал хизмат \nкўрсатиш тилини танлаб олайлик.'
                "\n-------------------\n"
                f'🇷🇺 Здраствуйте! Давайте для начала выбераем\n язык обслуживаниия.', reply_markup=button.b_button())
    
    return STATE_BEGIN

def phone(update:Update, context:CallbackContext):
    b_name = update.message.text
    
    if b_name == button.b1:
        context.chat_data.update({'til':'uz'})
        update.message.reply_html(f'Телефон рақамингизни +9989** *** ** **\nшаклда юборинг, '
                                    f'ёки "📱 Рақам юбориш"\nтугмасини босинг:',
                                    reply_markup=button.t_button_uz())
    elif b_name == button.b2:
        context.chat_data.update({'til':'ru'})
        update.message.reply_html(f"{data.phone_text['ru']}",
                                    reply_markup=button.t_button_ru())
    
    context.chat_data.update({'first_name': update.effective_user.first_name})
    
    return STATE_PHONE
 
def resent_lang(update: Update, context: CallbackContext):
    update.message.reply_html(f'Ассалому алайкум! Келинг, аввал хизмат кўрсатиш тилини танлаб олайлик.'
                              f'\n\nЗдраствуйте! Давайте для начала выбераем язык обслуживаниия.  ',
                              reply_markup=button.b_button())


def phone_entity_handler(update: Update, context: CallbackContext):
    pne = list(filter(lambda e: e.type == 'phone_number', update.message.entities))[0]
    phone_number = update.message.text[pne.offset : pne.offset + pne.length]
    context.chat_data.update({'phone_number': phone_number})
    til = context.chat_data['til']
    update.message.reply_html(f"{data.xurmatli[f'{til}']} <b>{update.effective_user.first_name} !</b>\n\n<i>{data.text_message[f'{til}']}</i>\n\n")

    return STATE_MESSAGE

def phone_contact_handler(update: Update, context: CallbackContext):
    phone_number = update.message.contact
    context.chat_data.update({'phone_number': phone_number['phone_number']})
    til = context.chat_data['til']
    update.message.reply_html(f"{data.xurmatli[f'{til}']} <b>{update.effective_user.first_name} !</b>\n\n<i>{data.text_message[f'{til}']}</i>\n\n")

    return STATE_MESSAGE


def phone_resent_handler(update: Update, context: CallbackContext):
    if context.chat_data['til'] == 'uz':
        btn = button.t_button_uz()
    else:
        btn = button.t_button_ru()
    
    update.message.reply_html(f'Телефон рақамингизни +9989** *** ** **\nшаклда юборинг, '
                                  f'ёки "📱 Рақам юбориш"\nтугмасини босинг:',
                                  reply_markup=btn)

def forward(update:Update, context:CallbackContext):
    til = context.chat_data['til']
    if update.message.text != '/start':
        msg = (f"👤 {update.effective_user.full_name}\n"
                f"📲 {context.chat_data['phone_number']}\n"
                f"🔗 {update.effective_user.link}\n\n"
                f"💬 Юборилган ҳабар  👇👇")
        context.bot.send_message(chat_id=314722445, text=msg)
        context.bot.forward_message(
            chat_id=314722445, 
            from_chat_id=update.effective_chat.id, 
            message_id=update.message.message_id
        )        
        update.message.reply_html(f'{data.yana_habar_yuboring[f"{til}"]}')

        if data.chack_user(chat_id=update.message.chat_id):
            user = data.select_user(chat_id=update.message.chat_id)
        else:
            data.insert_user_db(
                chat_id=update.effective_chat.id, 
                name=update.effective_user.full_name, 
                phone=context.chat_data['phone_number'], 
                link=update.effective_user.link
            )
            user = data.select_user(chat_id=update.message.chat_id)
        data.insert_post_db(text=update.message.text, user_id=user)
    else:
        update.message.reply_html(f'{data.yana_habar_yuboring[f"{til}"]}')



def statistics(update:Update, context:CallbackContext):
    context.bot.send_photo(chat_id = update.effective_message.chat_id,
                           photo = open('img/diogramma.jpg','rb'),
                           caption =  (f"🇺🇿 Барча фойдаланувчилар сони: <b>{data.count_users()}</b>\n"
                                      f"Бот ишга тушьганига <b>{(date.today() - date(2022, 9, 28)).days}</b> кун бўлди.\n"
                                      f"-----------------------------\n"
                                      f"🇷🇺 Общее количество пользователей: <b>{data.count_users()}</b>\n"
                                      f"Дней работы бота: <b>{(date.today() - date(2022, 9, 28)).days}</b>"),
                           parse_mode="HTML")

def help(update:Update, context:CallbackContext):
    update.message.reply_html("🇺🇿 Ушбу Telegram бот agrozamin.uz билан боғланишингиз,"
                                    f"расм, видео ҳамда аудиоёзувларни «Agrozamin мухбири» га юборишингиз учун яратилди.\n\n{data.text_message['uz']}\n\n"
                                    "------------------------------\n\n"
                                "🇷🇺 Этот Telegram-бот создан для того, чтобы вы могли"
                                    f"связаться с agrozamin.uz, ​​отправить фото, видео и аудиозаписи «Корреспонденту Агрозамин».\n\n{data.text_message['ru']}")


updater = Updater("5794102410:AAFfM6IBWUbaMs0UyFXHcnyPPbxOQKEZ2Eo", use_context=True)
updater.dispatcher.add_handler(CommandHandler('statistics', statistics))
updater.dispatcher.add_handler(CommandHandler('help', help))
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        STATE_BEGIN:[
            MessageHandler(Filters.text, phone),
            MessageHandler(Filters.all, resent_lang)],
        STATE_PHONE: [
            MessageHandler(Filters.text & Filters.entity(MessageEntity.PHONE_NUMBER), phone_entity_handler),
            MessageHandler(Filters.contact, phone_contact_handler),
            MessageHandler(Filters.all, phone_resent_handler)
        ],
        STATE_MESSAGE:[
            MessageHandler(Filters.all, forward)
        ],
    },
    fallbacks=[]
)

updater.dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()