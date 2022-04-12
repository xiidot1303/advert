from operator import imod
from typing import Text
from django.db.models.base import ModelState
from telegram import Bot
from telegram.ext import Dispatcher, ConversationHandler, PicklePersistence
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from dotenv import load_dotenv
import os
from config import TELEGRAM_BOT_API_TOKEN, ENVIRONMENT
import requests

from bot.main import *
from bot.login import *
from bot.conversationList import *
from bot.settings import *
from bot.answering import *
from bot.post_info import *
from bot.vacancy import *
from bot.only_text import *

bot_obj = Bot(TELEGRAM_BOT_API_TOKEN)
persistence = PicklePersistence(filename='persistencebot')

if ENVIRONMENT != 'local': # in production
    updater = 1213
    dp = Dispatcher(bot_obj, None, workers=0, use_context=True, persistence=persistence)
else: # in local computer
    updater = Updater(token=TELEGRAM_BOT_API_TOKEN, use_context=True, persistence=persistence)
    dp = updater.dispatcher


login_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states = {
        SELECT_LANG: [MessageHandler(Filters.text(['UZ 🇺🇿', 'RU 🇷🇺']), select_lang)],
        SEND_NAME: [MessageHandler(Filters.text, send_name)],
        SEND_CONTACT: [MessageHandler(Filters.all, send_contact)],
    },
    fallbacks= [],
    name='login',
    persistent=True,
)



settings_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(lang_dict['settings']), settings)],
    states = {
        ALL_SETTINGS: [MessageHandler(Filters.text, all_settings)],
        LANG_SETTINGS: [CallbackQueryHandler(lang_settings), CommandHandler('start', lang_settings)],
        PHONE_SETTINGS: [MessageHandler(Filters.all, phone_settings)],
        NAME_SETTINGS: [MessageHandler(Filters.text, name_settings)],
    }, 
    fallbacks=[],
    name='settings',
    persistent=True,
)


seller_handler = ConversationHandler(
    entry_points = [MessageHandler(Filters.text(lang_dict['seller']), seller)],
    states = {
        ANSWERING: [MessageHandler(Filters.text, loop_answering), MessageHandler(Filters.photo, loop_answering)],
        ASK_PAYMENT: [MessageHandler(Filters.text, ask_payment), MessageHandler(Filters.photo, ask_payment)],
    },
    fallbacks=[],
    name = 'seller',
    persistent=True,
)


buyer_handler = ConversationHandler (
    entry_points = [MessageHandler(Filters.text(lang_dict['buyer']), buyer)],
    states= {
        TYPE_POST_NUMBER: [MessageHandler(Filters.text, send_post)]
    },
    fallbacks=[],
    name = 'buyer',
    persistent=True,
)

vacancy_handler = ConversationHandler (
    entry_points = [MessageHandler(Filters.text(lang_dict['my vacancies']), vacancies)],
    # entry_points = [CommandHandler('q', vacancies)],
    states = {
        VACANCY_ACTIONS: [CallbackQueryHandler(vacancy_actions), MessageHandler(Filters.text, vacancy_actions)],
        # CHANING
        CHANGING: [MessageHandler(Filters.text, loop_changing), MessageHandler(Filters.photo, loop_changing)],
        CHANGE_PAYMENT: [MessageHandler(Filters.text, change_payment), MessageHandler(Filters.photo, change_payment)],
        GET_TEXT_VACANCY: [MessageHandler(Filters.text, get_text_vacancy2)],
        # CREATING
        ANSWERING: [MessageHandler(Filters.text, loop_answering2), MessageHandler(Filters.photo, loop_answering2)],
        ASK_PAYMENT: [MessageHandler(Filters.text, ask_payment2), MessageHandler(Filters.photo, ask_payment2)],

    },
    fallbacks=[],
    name = 'vacancy',
    persistent=True,

)



only_text_handler = ConversationHandler (
    entry_points = [MessageHandler(Filters.text(lang_dict['send by text']), only_text)],
    states = {
        GET_TEXT_VACANCY: [MessageHandler(Filters.text, get_text_vacancy)],
    },
    fallbacks=[],
    name='only_text',
    persistent=True,
)



dp.add_handler(only_text_handler)
dp.add_handler(vacancy_handler)
dp.add_handler(buyer_handler)
dp.add_handler(seller_handler)
dp.add_handler(settings_handler)
dp.add_handler(login_handler)

