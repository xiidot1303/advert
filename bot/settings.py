from app.models import *
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot.conversationList import *
from telegram.ext import ConversationHandler
from functions.bot import *
from functions.deco import *


@is_start
def all_settings(update, context):
    msg = update.message.text
    bot = context.bot
    if msg == get_word('change lang', update):
        current_lang = get_user_by_update(update).lang
        if current_lang == 'uz':
            uz_text = 'UZ \U0001F1FA\U0001F1FF   ✅'
            ru_text = 'RU \U0001F1F7\U0001F1FA'
        else:
            uz_text = 'UZ \U0001F1FA\U0001F1FF'
            ru_text = 'RU \U0001F1F7\U0001F1FA    ✅'
        i_uz = InlineKeyboardButton(text=uz_text, callback_data='set_lang_uz')
        i_ru = InlineKeyboardButton(text=ru_text, callback_data='set_lang_ru')
        i_back = InlineKeyboardButton(get_word('back', update), callback_data='back_settings')
        del_msg = update.message.reply_text(get_word('select lang', update), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        bot.delete_message(update.message.chat.id, del_msg.message_id)
        bot.send_message(update.message.chat.id, get_word('select lang', update), reply_markup = InlineKeyboardMarkup([[i_uz], [i_ru], [i_back]]))
        return LANG_SETTINGS

    elif msg == get_word('change phone number', update):
        ###
        return PHONE_SETTINGS
    elif msg == get_word('change name', update):
        ###
        return NAME_SETTINGS



#  lang settings
@is_start
def click_lang(update, context):
    update = update.callback_query
    bot = context.bot
    data = str(update.data)
    user = Bot_user.objects.get(user_id=update.message.chat.id)
    if data == 'set_lang_uz':
        user.lang = 'uz'
        user.save()
    elif data == 'set_lang_ru':
        user.lang = 'ru'
        user.save()
    elif data == 'back_settings':
        bot.delete_message(update.message.chat.id, update.message.message_id)
        make_button_settings(update, context)
        return ALL_SETTINGS
    current_lang = user.lang
    if current_lang == 'uz':
        uz_text = 'UZ \U0001F1FA\U0001F1FF   ✅'
        ru_text = 'RU \U0001F1F7\U0001F1FA'
    else:
        uz_text = 'UZ \U0001F1FA\U0001F1FF'
        ru_text = 'RU \U0001F1F7\U0001F1FA    ✅'
    
    i_uz = InlineKeyboardButton(text=uz_text, callback_data='set_lang_uz')
    i_ru = InlineKeyboardButton(text=ru_text, callback_data='set_lang_ru')
    i_back = InlineKeyboardButton(get_word('back', update), callback_data='back_main_menu')
    update.edit_message_text(get_word('select lang', update), reply_markup = InlineKeyboardMarkup([[i_uz], [i_ru], [i_back]]))
