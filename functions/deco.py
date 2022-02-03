from telegram import ReplyKeyboardMarkup, KeyboardButton
import telegram
from bot.uz_ru import lang_dict
from app.models import *
from telegram.ext import ConversationHandler
from datetime import date, datetime
from bot.conversationList import *


def is_start_registr(func):
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
            update.message.reply_text('🤖 Xush kelibsiz!\n Bot tilini tanlang  🌎 \n\n ➖➖➖➖➖➖➖➖➖➖➖➖\n\n 👋 Добро пожаловать \n \U0001F1FA\U0001F1FF Выберите язык бота \U0001F1F7\U0001F1FA', reply_markup=ReplyKeyboardMarkup(keyboard=[['UZ 🇺🇿', 'RU 🇷🇺']], resize_keyboard=True))
            return SELECT_LANG

 
        else:
            return func(*args, **kwargs)
    return func_arguments



# def is_start(func):    # This deco break registration if user send /start.
#     def func_arguments(*args, **kwargs):
#         bot = args[1].bot
#         try:
#             lalal = args[0].message.text
#             update = args[0]
#             data = ''
#         except:
#            update = args[0].callback_query
#            data = update.data  
#         id = update.message.chat.id
#         if update.message.text == '/start':
#             try:
#                 a_index = Answer_index.objects.get(end=False, user_id = id)
#                 a_index.delete()
#                 for a in Answer.objects.filter(date=None, user__user_id = id):
#                     a.delete()
#             except:
#                 csf = 0
#             if data == 'main_menu' or update.message.text == '/start':
#                 try:
#                     bot.delete_message(id, update.message.message_id)
#                     bot.delete_message(id, update.message.message_id-1)
#                 except:
#                     sth = 0
#             main_menu(args[0], args[1])
#             return ConversationHandler.END
#         else:
#             return func(*args, **kwargs)
#     return func_arguments

