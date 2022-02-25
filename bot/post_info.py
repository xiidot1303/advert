from telegram import ReplyKeyboardMarkup, KeyboardButton
import telegram
from bot.uz_ru import lang_dict
from app.models import *
from telegram.ext import ConversationHandler
from datetime import date, datetime
from bot.conversationList import *
from functions.bot import *
from functions.deco import *


def send_post(update, context):
    bot = context.bot
    answer = update.message.text
    if answer == get_word('back', update):
        main_menu(update, context)
        return ConversationHandler.END
    try:
        st_obj = Statement.objects.get(pk=int(answer), status='confirmed')
    except:
        update.message.reply_text(get_word('incorrect post number', update))
        return TYPE_POST_NUMBER

    id  = st_obj.pk
    answer_obj = st_obj.answer
    answers = split_by_slash(answer_obj.answer)
    user = answer_obj.user

    # post info
    questions = Backup_question.objects.filter(answer=answer_obj.pk)
    post_info = "<b>ID: </b>{}\n".format(id)
    n = 0
    for q in questions:
        if not q.req_photo:
            post_info += '{}: <i>{}</i>\n'.format(q.question, answers[n])

        n += 1

    bot.send_message(update.message.chat.id, post_info, parse_mode=telegram.ParseMode.HTML)
    # user info
    user_info = '{text_name}: {name}\n{text_phone}: {phone}\n{text_username}: {username}'
    name = user.name
    phone = user.phone
    if user.username:
        username = '@' + user.username
    else:
        username = '<a href="tg://user?id={}">{}</a>'.format(user.user_id, user.firstname)
    update.message.reply_text(user_info.format(text_name = get_word('name', update), name=name, 
        text_phone=get_word('phone number', update), phone=phone, 
        text_username='🆔 Username', username=username), parse_mode=telegram.ParseMode.HTML)
    st_obj.views += 1
    st_obj.save()
    client = get_user_by_update(update)
    client.is_client = True
    client.save()
    main_menu(update, context)
    return ConversationHandler.END