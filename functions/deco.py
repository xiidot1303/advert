from telegram import ReplyKeyboardMarkup
from app.models import *
from telegram.ext import ConversationHandler
from bot.conversationList import *
from functions.bot import *


def is_start_registr(func):
    def func_arguments(*args, **kwargs):
        bot = args[1].bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ""
        except:
            update = args[0].callback_query
            data = update.data
        id = update.message.chat.id
        if update.message.text == "/start":
            update.message.reply_text(
                "🤖 Xush kelibsiz!\n Bot tilini tanlang  🌎 \n\n ➖➖➖➖➖➖➖➖➖➖➖➖\n\n 👋 Добро пожаловать \n \U0001F1FA\U0001F1FF Выберите язык бота \U0001F1F7\U0001F1FA",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[["UZ 🇺🇿", "RU 🇷🇺"]], resize_keyboard=True
                ),
            )
            return SELECT_LANG

        else:
            return func(*args, **kwargs)

    return func_arguments


def is_start(func):  # This deco break registration if user send /start.
    def func_arguments(*args, **kwargs):
        bot = args[1].bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ""
        except:
            update = args[0].callback_query
            data = update.data
        id = update.message.chat.id
        if (
            update.message.text == "/start"
            or data == "main_menu"
            or update.message.text == get_word("main menu", update)
        ):
            user = get_user_by_update(update)
            for a in Answer.objects.filter(user=user, end=False):
                if not Statement.objects.filter(answer=a):
                    for q in BackupQuestion.objects.filter(answer=a.pk):
                        q.delete()
                    a.delete()
                else:
                    a.end = True
                    a.save()
            main_menu(args[0], args[1])
            return ConversationHandler.END
        else:
            return func(*args, **kwargs)

    return func_arguments
