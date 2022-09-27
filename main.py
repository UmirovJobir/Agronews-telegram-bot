from email import message
from telegram.bot import Bot
from telegram import Update, MessageEntity
from telegram.ext import CallbackContext, MessageHandler, Updater, CommandHandler, ConversationHandler, Filters

from backend import DB
from buttons import buttons
data = DB()
button = buttons()

STATE_BEGIN = 1
STATE_PHONE = 2
STATE_MESSAGE = 3
STATE_CHECK = 4
STATE_TEXT = 5

text = """💬 Ўзингиз гувоҳи бўлган:\n
       🔹 Йўл транспорт ҳодисалари
       🔹 Спорт тадбирлари ва
       🔹 Бошқа қизиқарли ҳодисаларни\n\nтасвирга олиб, вақти, жойи куни, каби маълумотлари билан биргаликда бизга юборинг."""



def start(update:Update, context:CallbackContext):
    update.message.reply_html(f'Телефон рақамингизни +9989** *** ** **\nшаклда юборинг, '
                                  f'ёки "📱 Рақам юбориш"\nтугмасини босинг:',
                                  reply_markup=button.t_button())
    context.chat_data.update({'first_name': update.effective_user.first_name})
    
    return STATE_PHONE
 
def phone_entity_handler(update: Update, context: CallbackContext):
    pne = list(filter(lambda e: e.type == 'phone_number', update.message.entities))[0]
    phone_number = update.message.text[pne.offset : pne.offset + pne.length]
    print(update.message.text, update.message.entities[0], phone_number)
    context.chat_data.update({'phone_number': phone_number})
    
    update.message.reply_html(f"Ҳурматли <b>{update.effective_user.first_name} !</b>\n\n<i>{text}</i>")

    return STATE_MESSAGE

def phone_contact_handler(update: Update, context: CallbackContext):
    phone_number = update.message.contact
    context.chat_data.update({'phone_number': phone_number['phone_number']})
    
    update.message.reply_html(f"Ҳурматли <b>{update.effective_user.first_name} !</b>\n\n<i>{text}</i>")

    return STATE_MESSAGE


def phone_resent_handler(update: Update, context: CallbackContext):
    update.message.reply_html(f'Телефон рақамингизни +9989** *** ** **\nшаклда юборинг, '
                                  f'ёки "📱 Рақам юбориш"\nтугмасини босинг:',
                                  reply_markup=button.t_button())

def forward(update:Update, context:CallbackContext):
    if update.message.text != '/start':
        msg = f"""👤 {update.effective_user.full_name}\n📲 {context.chat_data['phone_number']}\n🔗 {update.effective_user.link}\n\n💬 Юборилган ҳабар  👇👇"""
        context.bot.send_message(chat_id=314722445, text=msg)
        context.bot.forward_message(chat_id=314722445, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)        
        update.message.reply_html("🤖 Ҳабарингиз мухбирга жўнатдим.\n\n✍️ Яна ҳабар юборишингиз мумкин ...")
        if data.chack_user(chat_id=update.message.chat_id):
            user = data.select_user(chat_id=update.message.chat_id)
        else:
            data.insert_user_db(chat_id=update.effective_chat.id, name=update.effective_user.full_name, phone=context.chat_data['phone_number'], link=update.effective_user.link)
            user = data.select_user(chat_id=update.message.chat_id)
        data.insert_post_db(text=update.message.text, user_id=user)



updater = Updater("5794102410:AAFfM6IBWUbaMs0UyFXHcnyPPbxOQKEZ2Eo", use_context=True)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        STATE_BEGIN:[
            MessageHandler(Filters.all, forward)],
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