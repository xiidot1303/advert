from datetime import datetime
from platform import node
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
def loop_answering(update, context):
    bot = context.bot
    answer = update.message.text

    # get an Answer object that processing
    answer_obj = get_current_answer_by_update(update)
    question_index = len(split_by_slash(answer_obj.answer)) + 1   # get next question by counting current answers
    question_obj = get_backup_question(question_index, answer_obj.pk)   

    #check to back
    if update.message.text == get_word('back', update):
        question_index -= 1
        if question_index == 0:
            for q in Backup_question.objects.filter(answer = answer_obj.pk):
                q.delete()
            answer_obj.delete()
            main_menu(update, context)
            return ConversationHandler.END
        
        all_answers = split_by_slash(answer_obj.answer)
        all_answers = all_answers[:-1]
        answer_obj.answer = compress_by_slash(all_answers)
        answer_obj.save()
        question_obj = get_backup_question(question_index, answer_obj.pk)
        text = question_obj.question
        if question_obj.variants:
            keyboards = get_variants_for_buttons(question_obj.variants)
        else:
            keyboards = []

        keyboards.append([get_word('back', update)])
        update.message.reply_text(text, reply_markup = ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True))
        return ANSWERING
    


    # check , reuqired photo or not
    if question_obj.req_photo:
        # check is answer photo 
        try:
            # try to download photo
            p = bot.getFile(update.message.photo[-1].file_id)
            *args, file_name = str(p.file_path).split('/')
            d_photo = p.download('files/photos/{}'.format(file_name))
            answer_obj.photo = str(d_photo).replace('files/', '')
            answer = photo()
        except:
            # answer is not photo object
            update.message.reply_text(get_word('send photo', update))
            return ANSWERING     


    if answer == None:
        return ANSWERING

    #check a question have variants or not
    if question_obj.variants:
        answer = update.message.text
        # check answer text is in varinats or not
        # variants = split_by_slash(question_obj.variants)
        if answer in question_obj.variants:
            ok = True
        else:
            update.message.reply_text(get_word('click variant', update))
            return ANSWERING
    
    answer_obj.answer += str(answer) + '//'   # set current text as answer
    answer_obj.save()
    #check is that last question ans anwer
    last_question = Backup_question.objects.filter(answer = answer_obj.pk).order_by('-index')[0]
    if last_question.index == question_index:
        # end answering
        answer_obj.end = True
        answer_obj.date = datetime.now()
        answer_obj.save()
        Statement.objects.create(answer = answer_obj, status = 'waiting')
        update.message.reply_text(get_word('completed answering', update))
        main_menu(update, context)
        return ConversationHandler.END

    next_question_obj = get_backup_question(question_index+1, answer_obj.pk)
    text = next_question_obj.question
    if next_question_obj.variants:
        keyboards = get_variants_for_buttons(next_question_obj.variants)
    else:
        keyboards = []
    keyboards.append([get_word('back', update)])
    update.message.reply_text(text, reply_markup = ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True))
    return ANSWERING