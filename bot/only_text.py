from datetime import datetime
from telegram import ReplyKeyboardMarkup, KeyboardButton
import telegram
from bot.uz_ru import lang_dict
from app.models import *
from telegram.ext import ConversationHandler
from datetime import date, datetime
from bot.conversationList import *
from functions.bot import *
from functions.deco import *



@is_start
def get_text_vacancy(update, context):
    bot = context.bot
    answer = update.message.text
        
    answer_obj = get_current_answer_by_update(update)

    if answer == get_word('back', update):
        for q in Backup_question.objects.filter(answer = answer_obj.pk):
            q.delete()
        answer_obj.delete()
        main_menu(update, context)
        return ConversationHandler.END

    answer_obj.text = answer
    answer_obj.end = True
    answer_obj.date = datetime.now()
    answer_obj.save()

    Statement.objects.create(answer = answer_obj, status = 'waiting')
    update.message.reply_text(get_word('completed answering', update))
    main_menu(update, context)
    return ConversationHandler.END