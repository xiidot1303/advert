from telegram import ReplyKeyboardMarkup

from app.models import *
from bot.conversationList import SELECT_LANG
from functions.bot import *


def start(update, context):

    if is_registered(update.message.chat.id):
        main_menu(update, context)
    else:
        hello_text = "🤖 Xush kelibsiz!\n Bot tilini tanlang  🌎 \n\n ➖➖➖➖➖➖➖➖➖➖➖➖\n\n 👋 Добро пожаловать \n \U0001F1FA\U0001F1FF Выберите язык бота \U0001F1F7\U0001F1FA"
        update.message.reply_text(
            hello_text,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[["UZ 🇺🇿", "RU 🇷🇺"]], resize_keyboard=True
            ),
        )
        return SELECT_LANG


def settings(update, context):
    make_button_settings(update, context)
    return ALL_SETTINGS


def seller(update, context):
    user = get_user_by_update(update)

    # create an answer object
    Answer.objects.get_or_create(user=user, answer="", end=False)
    answer = Answer.objects.get(user=user, end=False)

    # back up questions
    n = 1
    for q in Question.objects.all().order_by("index"):
        if user.lang == "uz":
            BackupQuestion.objects.create(
                user=user,
                question=q.questionuz,
                variants=q.variantsuz,
                index=n,
                req_photo=q.req_photo,
                is_required=q.is_required,
                answer=answer.pk,
            )
        else:
            BackupQuestion.objects.create(
                user=user,
                question=q.questionru,
                variants=q.variantsru,
                index=n,
                req_photo=q.req_photo,
                is_required=q.is_required,
                answer=answer.pk,
            )
        n += 1
    question_obj = BackupQuestion.objects.filter(user=user, answer=answer.pk).order_by(
        "index"
    )[0]
    text = question_obj.question
    if question_obj.variants:
        keyboards = get_variants_for_buttons(question_obj.variants)
    else:
        keyboards = []
    if not question_obj.is_required:
        keyboards.append([get_word("skip", update)])
    keyboards.append([get_word("back", update)])
    update.message.reply_text(
        text, reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)
    )
    return ANSWERING


def buyer(update, context):
    text = get_word("type post number", update)
    keyboards = [[get_word("back", update)]]
    update.message.reply_text(
        text, reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)
    )
    return TYPE_POST_NUMBER


def vacancies(update, context):

    update.message.reply_text(
        get_word("all vacancies", update),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[get_word("create vacancy", update)], [get_word("back", update)]],
            resize_keyboard=True,
        ),
    )

    make_vacancies_card(update, context)

    return VACANCY_ACTIONS


def only_text(update, context):

    user = get_user_by_update(update)

    # create an answer object
    Answer.objects.get_or_create(user=user, answer="", end=False)
    answer = Answer.objects.get(user=user, end=False)

    # back up questions
    n = 1
    for q in Question.objects.all().order_by("index"):
        if user.lang == "uz":
            BackupQuestion.objects.create(
                user=user,
                question=q.questionuz,
                variants=q.variantsuz,
                index=n,
                req_photo=q.req_photo,
                is_required=q.is_required,
                answer=answer.pk,
            )
        else:
            BackupQuestion.objects.create(
                user=user,
                question=q.questionru,
                variants=q.variantsru,
                index=n,
                req_photo=q.req_photo,
                is_required=q.is_required,
                answer=answer.pk,
            )
        n += 1

    update.message.reply_text(
        get_word("send text vacancy", update),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[get_word("back", update)]], resize_keyboard=True
        ),
    )
    return GET_TEXT_VACANCY
