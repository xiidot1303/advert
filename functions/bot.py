from telegram import ReplyKeyboardMarkup, KeyboardButton
import telegram
from bot.uz_ru import lang_dict
from app.models import *
from telegram.ext import ConversationHandler
from datetime import date, datetime
from bot.conversationList import *

def main_menu(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www= 0 # do nothing
    
    bot = context.bot
    keyboard=[[get_word('seller', update)], [get_word('buyer', update)], [get_word('settings', update)]]
    bot.send_message(update.message.chat.id, get_word('main menu', update), reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
    check_username(update)

    
def make_button_settings(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www= 0 # do nothing
    bot = context.bot
    keyboard=[[get_word('change lang', update)], [get_word('change name', update)], [get_word('change phone number', update)], [get_word('main menu', update)]]
    bot.send_message(update.message.chat.id, get_word('settings desc', update), reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))



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

def get_user_by_update(update):
    user = Bot_user.objects.get(user_id=update.message.chat.id)
    return user

def check_username(update):
    user = get_user_by_update(update)
    
    if user.username != update.message.chat.username:
        user.username = update.message.chat.username
        user.save()
    if user.firstname != update.message.chat.first_name:
        user.firstname = update.message.chat.first_name
        user.save()
    

def get_variants_for_buttons(text):
    l = list(str(text).split('//'))
    try:
        l.remove('')
    except:
        ok = True
    r_list = [[i] for i in l]
    return r_list

def split_by_slash(text):
    l = list(str(text).split('//'))
    try:
        l.remove('')
    except:
        ok = True
    return l

def compress_by_slash(l):
    text_ = ''
    for i in l:
        text_ += i+'//'
    return text_



def get_current_answer_by_update(update):
    user = get_user_by_update(update)
    obj = Answer.objects.get(user=user, end=False)
    return obj

def get_backup_question(index, answer_pk):
    obj = Backup_question.objects.get(index = index, answer = answer_pk)
    return obj


# make text photo 
def photo():
    return 'Po0enOIIJBUGERrftesUhio'
