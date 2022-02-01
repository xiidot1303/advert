from typing import Text
from django.db.models.base import ModelState
from telegram import Bot
from telegram.ext import Dispatcher, ConversationHandler, PicklePersistence
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from dotenv import load_dotenv
import os
from config import TELEGRAM_BOT_API_TOKEN, ENVIRONMENT
import requests

bot_obj = Bot(TELEGRAM_BOT_API_TOKEN)
persistence = PicklePersistence(filename='persistencebot')

if ENVIRONMENT != 'local': # in production
    updater = 1213
    dp = Dispatcher(bot_obj, None, workers=0, use_context=True, persistence=persistence)
else: # in local computer
    updater = Updater(token=TELEGRAM_BOT_API_TOKEN, use_context=True, persistence=persistence)
    dp = updater.dispatcher


