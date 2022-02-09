
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler

from app.models import *
from bot.conversationList import SELECT_LANG
from functions.bot import *

def start(update, context):
    if is_registered(update.message.chat.id):
        main_menu(update, context)
    else:
        hello_text = '🤖 Xush kelibsiz!\n Bot tilini tanlang  🌎 \n\n ➖➖➖➖➖➖➖➖➖➖➖➖\n\n 👋 Добро пожаловать \n \U0001F1FA\U0001F1FF Выберите язык бота \U0001F1F7\U0001F1FA'
        update.message.reply_text(hello_text, reply_markup=ReplyKeyboardMarkup(keyboard=[['UZ 🇺🇿', 'RU 🇷🇺']], resize_keyboard=True))
        return SELECT_LANG

def settings(update, context):
    make_button_settings(update, context)
    return ALL_SETTINGS

def seller(update, context):
    user = get_user_by_update(update)

    #create an answer object
    Answer.objects.get_or_create(user = user, answer='', end = False)
    answer = Answer.objects.get(user = user, end = False)
    
    #back up questions
    for q in Question.objects.filter(lang=user.lang).order_by('index'):
        Backup_question.objects.create(user = user, question = q.question, variants = q.variants, index = q.index, req_photo = q.req_photo, answer = answer.pk)

    question_obj = Question.objects.filter(lang=user.lang).order_by('index')[0]
    text = question_obj.question
    if question_obj.variants:
        keyboards = get_variants_for_buttons(question_obj.variants)
    else:
        keyboards = []

    keyboards.append([get_word('back', update)])
    update.message.reply_text(text, reply_markup = ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True))
    return ANSWERING
    

def buyer(update, context):
    text = get_word('type post number', update)
    keyboards = [[get_word('back', update)]]
    update.message.reply_text(text, reply_markup = ReplyKeyboardMarkup(keyboard = keyboards, resize_keyboard=True))
    return TYPE_POST_NUMBER