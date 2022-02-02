from telegram import ReplyKeyboardMarkup, KeyboardButton
import telegram
from bot.uz_ru import lang_dict
from app.models import *
from telegram.ext import ConversationHandler
from datetime import date, datetime


def main_menu(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www= 0 # do nothing
    
    bot = context.bot
    bot.send_message(update.message.chat.id, get_word('main menu', update), reply_markup=ReplyKeyboardMarkup(keyboard=[[get_word('', update)], [get_word('', update)]], resize_keyboard=True))



def get_word(text, update):
    user = Bot_user.objects.get(user_id=update.message.chat.id)
    if user.lang == 'uz':
        return lang_dict[text][0]
    else:
       return lang_dict[text][1]

def is_registered(id):
    if Bot_user.objects.filter(user_id=id):
        return True
    else:
        return False

def get_user_by_id(id):
    user = Bot_user.objects.get(user_id=id)
    return user



def is_start(func):
    def func_arguments(*args, **kwargs):
        bot = args[1].bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ''
        except:
           update = args[0].callback_query
           data = update.data  
        id = update.message.chat.id
        if update.message.text == '/start' or data == 'main_menu' or update.message.text == get_word('main menu', update):
            try:
                a_index = Answer_index.objects.get(end=False, user_id = id)
                a_index.delete()
                for a in Answer.objects.filter(date=None, user__user_id = id):
                    a.delete()
            except:
                csf = 0
            if data == 'main_menu' or update.message.text == '/start':
                try:
                    bot.delete_message(id, update.message.message_id)
                    bot.delete_message(id, update.message.message_id-1)
                except:
                    sth = 0
            main_menu(args[0], args[1])
            return ConversationHandler.END
        else:
            return func(*args, **kwargs)
    return func_arguments



def is_start_registr(func):    # This deco break registration if user send /start.
    def func_arguments(*args, **kwargs):
        bot = args[1].bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ''
        except:
           update = args[0].callback_query
           data = update.data  
        id = update.message.chat.id
        if update.message.text == '/start':
            try:
                a_index = Answer_index.objects.get(end=False, user_id = id)
                a_index.delete()
                for a in Answer.objects.filter(date=None, user__user_id = id):
                    a.delete()
            except:
                csf = 0
            if data == 'main_menu' or update.message.text == '/start':
                try:
                    bot.delete_message(id, update.message.message_id)
                    bot.delete_message(id, update.message.message_id-1)
                except:
                    sth = 0
            main_menu(args[0], args[1])
            return ConversationHandler.END
        else:
            return func(*args, **kwargs)
    return func_arguments

