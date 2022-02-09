from telegram import ReplyKeyboardMarkup, KeyboardButton
import telegram
from bot.uz_ru import lang_dict
from app.models import *
from telegram.ext import ConversationHandler
from datetime import date, datetime
from bot.conversationList import *
from functions.bot import *
from functions.deco import *


def send_post(update, context):
    
    answer = update.message.text
    if answer == get_word('back', update):
        main_menu(update, context)
        return ConversationHandler.END
    try:
        st_obj = Statement.objects.get(pk=int(answer), status='confirmed')
    except:
        update.message.reply_text(get_word('incorrect post number', update))
        return TYPE_POST_NUMBER
    answer_obj = st_obj.answer
    user = answer_obj.user
    return_text = '{name}\n{phone}\n{username}'
    name = user.name
    phone = user.phone
    if user.username:
        username = '@' + user.username
    else:
        username = '<a href="tg://user?id={}">{}</a>'.format(user.user_id, user.firstname)
    update.message.reply_text(return_text.format(name=name, phone=phone, username=username))
    main_menu(update, context)
    return ConversationHandler.END