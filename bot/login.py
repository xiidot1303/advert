from app.models import *
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot.conversationList import *
from telegram.ext import ConversationHandler
from functions.bot import *


def select_lang(update, context):
    text = update.message.text
    if 'UZ' in text:
        Bot_user.objects.get_or_create(user_id=update.message.chat.id, lang='uz')
        update.message.reply_text(get_word('type name', update), reply_markup=ReplyKeyboardMarkup([[get_word('back', update)]], resize_keyboard=True))
        return SEND_NAME
    elif 'RU' in text:
        Bot_user.objects.get_or_create(user_id=update.message.chat.id, lang='ru')
        update.message.reply_text(get_word('type name', update), reply_markup=ReplyKeyboardMarkup([[get_word('back', update)]], resize_keyboard=True))
        return SEND_NAME
    else:
        update.message.reply_text('Bot tilini tanlang\n\nВыберите язык бота', update)



