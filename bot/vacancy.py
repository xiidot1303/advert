from telegram import ReplyKeyboardMarkup
import telegram
from app.models import *
from telegram.ext import ConversationHandler
from datetime import datetime
from bot.conversationList import *
from bot.main import vacancies
from functions.bot import *
from functions.deco import *


@is_start
def vacancy_actions(update, context):
    bot = context.bot
    if update.callback_query:
        update = update.callback_query
        data = update.data
        if "publishstatement" in data:
            *args, id = str(data).split("_")
            st_obj = Statement.objects.get(pk=id)
            st_obj.status = "waiting"
            st_obj.save()
            bot.answer_callback_query(
                callback_query_id=update.id,
                text=get_word("completed answering", update),
                show_alert=True,
            )
            return

        elif "changestatement" in data:
            *args, id = str(data).split("_")
            st_obj = Statement.objects.get(pk=id)

            # ------------------------------------------------------------

            user = get_user_by_update(update)

            # get an answer object

            answer = st_obj.answer
            answer.end = False
            answer.new_answer = ""
            answer.save()

            # check only text or full
            if not answer.answer:
                update.message.reply_text(
                    get_word("send text vacancy", update),
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[[get_word("back", update)]], resize_keyboard=True
                    ),
                )
                return GET_TEXT_VACANCY

            question_obj = Backup_question.objects.filter(
                user=user, answer=answer.pk
            ).order_by("index")[0]
            text = "{}\n\n{}: *{}*".format(
                question_obj.question,
                get_word("current answer", update),
                split_by_slash(answer.answer)[0],
            )
            if question_obj.variants:
                keyboards = [
                    [get_word("stay current answer", update)]
                ] + get_variants_for_buttons(question_obj.variants)
            else:
                keyboards = [[get_word("stay current answer", update)]]

            if not question_obj.is_required:
                keyboards.append([get_word("skip", update)])
            keyboards.append([get_word("back", update)])
            update.message.reply_text(
                text,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=keyboards, resize_keyboard=True
                ),
            )
            return CHANGING

            # -----------------------------------------------------------------

    else:
        answer = update.message.text

        if answer == get_word("back", update):
            main_menu(update, context)
            return ConversationHandler.END

        elif answer == get_word("create vacancy", update):
            user = get_user_by_update(update)

            # create an answer object
            Answer.objects.get_or_create(user=user, answer="", end=False)
            answer = Answer.objects.get(user=user, end=False)

            # back up questions
            n = 1
            for q in Question.objects.all().order_by("index"):
                if user.lang == "uz":
                    Backup_question.objects.create(
                        user=user,
                        question=q.questionuz,
                        variants=q.variantsuz,
                        index=n,
                        req_photo=q.req_photo,
                        is_required=q.is_required,
                        answer=answer.pk,
                    )
                else:
                    Backup_question.objects.create(
                        user=user,
                        question=q.questionru,
                        variants=q.variantsru,
                        index=n,
                        req_photo=q.req_photo,
                        is_required=q.is_required,
                        answer=answer.pk,
                    )
                n += 1
            question_obj = Backup_question.objects.filter(
                user=user, answer=answer.pk
            ).order_by("index")[0]
            text = question_obj.question
            if question_obj.variants:
                keyboards = get_variants_for_buttons(question_obj.variants)
            else:
                keyboards = []
            if not question_obj.is_required:
                keyboards.append([get_word("skip", update)])
            keyboards.append([get_word("back", update)])
            update.message.reply_text(
                text,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=keyboards, resize_keyboard=True
                ),
            )
            return ANSWERING


# __CHANGINg__


@is_start
def loop_changing(update, context):
    bot = context.bot
    answer = update.message.text

    # get an Answer object that processing
    answer_obj = get_current_answer_by_update(update)
    question_index = (
        len(split_by_slash(answer_obj.new_answer)) + 1
    )  # get next question by counting current answers
    question_obj = get_backup_question(question_index, answer_obj.pk)

    # check to back
    if update.message.text == get_word("back", update):
        question_index -= 1
        if question_index == 0:

            answer_obj.end = True
            answer_obj.save()
            vacancies(update, context)
            return VACANCY_ACTIONS

        # else
        all_answers = split_by_slash(answer_obj.new_answer)
        all_answers = all_answers[:-1]
        answer_obj.new_answer = compress_by_slash(all_answers)
        answer_obj.save()
        question_obj = get_backup_question(question_index, answer_obj.pk)
        text = "{}\n\n{}: *{}*".format(
            question_obj.question,
            get_word("current answer", update),
            split_by_slash(answer_obj.answer)[question_index - 1],
        )
        if question_obj.variants:
            keyboards = [
                [get_word("stay current answer", update)]
            ] + get_variants_for_buttons(question_obj.variants)
        else:
            keyboards = [[get_word("stay current answer", update)]]
        if not question_obj.is_required:
            keyboards.append([get_word("skip", update)])
        keyboards.append([get_word("back", update)])
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True),
        )
        return CHANGING

    if answer == get_word("skip", update):
        nothing = True
    elif answer == get_word("stay current answer", update):
        nothing = True

    # check , reuqired photo or not
    elif question_obj.req_photo:
        # check is answer photo
        try:
            # try to download photo
            p = bot.getFile(update.message.photo[-1].file_id)
            *args, file_name = str(p.file_path).split("/")
            d_photo = p.download("files/photos/{}".format(file_name))
            answer_obj.photo = str(d_photo).replace("files/", "")
            answer = photo()
        except:
            # answer is not photo object
            update.message.reply_text(get_word("send photo", update))
            return CHANGING

    if answer == None:
        return CHANGING

    if answer == get_word("skip", update):
        answer = "  "
        if question_obj.req_photo:
            answer_obj.photo = None
            answer_obj.save()
    elif answer == get_word("stay current answer", update):
        answer = split_by_slash(answer_obj.answer)[question_index - 1]

    # check a question have variants or not
    elif question_obj.variants:
        answer = update.message.text
        # check answer text is in varinats or not
        # variants = split_by_slash(question_obj.variants)
        if answer in question_obj.variants:
            ok = True
        else:
            update.message.reply_text(get_word("click variant", update))
            return CHANGING

    answer_obj.new_answer += str(answer) + "//"  # set current text as answer
    answer_obj.save()
    # check is that last question ans anwer
    last_question = Backup_question.objects.filter(answer=answer_obj.pk).order_by(
        "-index"
    )[0]
    if last_question.index == question_index:
        # end answering
        answer_obj.save()
        payment_obj = Payment.objects.get(pk=1)
        user = get_user_by_update(update)
        if user.lang == "uz":
            text = payment_obj.textuz
        else:
            text = payment_obj.textru

        card = payment_obj.card
        keyboards = []
        keyboards.append([get_word("back", update)])
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True),
            parse_mode=telegram.ParseMode.HTML,
        )
        update.message.reply_text(
            "`{}`".format(card), parse_mode=telegram.ParseMode.MARKDOWN
        )
        return CHANGE_PAYMENT

    next_question_obj = get_backup_question(question_index + 1, answer_obj.pk)
    text = "{}\n\n{}: *{}*".format(
        next_question_obj.question,
        get_word("current answer", update),
        split_by_slash(answer_obj.answer)[question_index],
    )
    if next_question_obj.variants:
        keyboards = [
            [get_word("stay current answer", update)]
        ] + get_variants_for_buttons(next_question_obj.variants)
    else:
        keyboards = [[get_word("stay current answer", update)]]
    if not next_question_obj.is_required:
        keyboards.append([get_word("skip", update)])
    keyboards.append([get_word("back", update)])
    update.message.reply_text(
        text, reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)
    )
    return CHANGING


@is_start
def change_payment(update, context):
    bot = context.bot
    answer_obj = get_current_answer_by_update(update)
    question_index = (
        len(split_by_slash(answer_obj.new_answer)) + 1
    )  # get next question by counting current answers

    # check to back
    if update.message.text == get_word("back", update):
        question_index -= 1
        if question_index == 0:

            answer_obj.end = True
            answer_obj.save()
            vacancies(update, context)
            return VACANCY_ACTIONS

        # else
        all_answers = split_by_slash(answer_obj.new_answer)
        all_answers = all_answers[:-1]
        answer_obj.new_answer = compress_by_slash(all_answers)
        answer_obj.save()
        question_obj = get_backup_question(question_index, answer_obj.pk)
        text = question_obj.question
        if question_obj.variants:
            keyboards = [
                [get_word("stay current answer", update)]
            ] + get_variants_for_buttons(question_obj.variants)
        else:
            keyboards = [[get_word("stay current answer", update)]]
        if not question_obj.is_required:
            keyboards.append([get_word("skip", update)])
        keyboards.append([get_word("back", update)])
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True),
        )
        return CHANGING

    # check is answer photo
    try:
        # try to download photo
        p = bot.getFile(update.message.photo[-1].file_id)
        *args, file_name = str(p.file_path).split("/")
        d_photo = p.download("files/payment/{}".format(file_name))
        answer_obj.payment = str(d_photo).replace("files/", "")

    except:
        # answer is not photo object
        update.message.reply_text(get_word("send photo", update))
        return CHANGE_PAYMENT

    # end answering
    answer_obj.end = True
    answer_obj.date = datetime.now()
    answer_obj.answer = answer_obj.new_answer
    answer_obj.new_answer = ""
    answer_obj.save()
    st_obj = Statement.objects.get(answer=answer_obj)
    st_obj.status = "waiting"
    st_obj.save()
    update.message.reply_text(get_word("completed answering", update))
    vacancies(update, context)
    return VACANCY_ACTIONS


@is_start
def get_text_vacancy2(update, context):
    bot = context.bot
    answer = update.message.text

    answer_obj = get_current_answer_by_update(update)

    if answer == get_word("back", update):
        answer_obj.end = True
        answer_obj.save()
        vacancies(update, context)
        return VACANCY_ACTIONS

    answer_obj.text = answer
    answer_obj.end = True
    answer_obj.date = datetime.now()
    answer_obj.save()

    st_obj = Statement.objects.get(answer=answer_obj)
    st_obj.status = "waiting"
    st_obj.save()
    update.message.reply_text(get_word("completed answering", update))
    vacancies(update, context)
    return VACANCY_ACTIONS


# ___CREATING___


@is_start
def loop_answering2(update, context):
    bot = context.bot
    answer = update.message.text

    # get an Answer object that processing
    answer_obj = get_current_answer_by_update(update)
    question_index = (
        len(split_by_slash(answer_obj.answer)) + 1
    )  # get next question by counting current answers
    question_obj = get_backup_question(question_index, answer_obj.pk)

    # check to back
    if update.message.text == get_word("back", update):
        question_index -= 1
        if question_index == 0:
            for q in Backup_question.objects.filter(answer=answer_obj.pk):
                q.delete()
            answer_obj.delete()
            vacancies(update, context)
            return VACANCY_ACTIONS

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
        if not question_obj.is_required:
            keyboards.append([get_word("skip", update)])
        keyboards.append([get_word("back", update)])
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True),
        )
        return ANSWERING

    if answer == get_word("skip", update):
        nothing = True
    # check , reuqired photo or not
    elif question_obj.req_photo:
        # check is answer photo
        try:
            # try to download photo
            p = bot.getFile(update.message.photo[-1].file_id)
            *args, file_name = str(p.file_path).split("/")
            d_photo = p.download("files/photos/{}".format(file_name))
            answer_obj.photo = str(d_photo).replace("files/", "")
            answer = photo()
        except:
            # answer is not photo object
            update.message.reply_text(get_word("send photo", update))
            return ANSWERING

    if answer == None:
        return ANSWERING

    if answer == get_word("skip", update):
        answer = "  "
        if question_obj.req_photo:
            answer_obj.photo = None
            answer_obj.save()
    # check a question have variants or not
    elif question_obj.variants:
        answer = update.message.text
        # check answer text is in varinats or not
        # variants = split_by_slash(question_obj.variants)
        if answer in question_obj.variants:
            ok = True
        else:
            update.message.reply_text(get_word("click variant", update))
            return ANSWERING

    answer_obj.answer += str(answer) + "//"  # set current text as answer
    answer_obj.save()
    # check is that last question ans anwer
    last_question = Backup_question.objects.filter(answer=answer_obj.pk).order_by(
        "-index"
    )[0]
    if last_question.index == question_index:
        # end answering
        answer_obj.save()
        payment_obj = Payment.objects.get(pk=1)
        user = get_user_by_update(update)
        if user.lang == "uz":
            text = payment_obj.textuz
        else:
            text = payment_obj.textru

        card = payment_obj.card
        keyboards = []
        keyboards.append([get_word("back", update)])
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True),
            parse_mode=telegram.ParseMode.HTML,
        )
        update.message.reply_text(
            "`{}`".format(card), parse_mode=telegram.ParseMode.MARKDOWN
        )
        return ASK_PAYMENT

    next_question_obj = get_backup_question(question_index + 1, answer_obj.pk)
    text = next_question_obj.question
    if next_question_obj.variants:
        keyboards = get_variants_for_buttons(next_question_obj.variants)
    else:
        keyboards = []
    if not next_question_obj.is_required:
        keyboards.append([get_word("skip", update)])
    keyboards.append([get_word("back", update)])
    update.message.reply_text(
        text, reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)
    )
    return ANSWERING


@is_start
def ask_payment2(update, context):
    bot = context.bot
    answer_obj = get_current_answer_by_update(update)
    question_index = (
        len(split_by_slash(answer_obj.answer)) + 1
    )  # get next question by counting current answers

    # check to back
    if update.message.text == get_word("back", update):
        question_index -= 1
        if question_index == 0:
            for q in Backup_question.objects.filter(answer=answer_obj.pk):
                q.delete()
            answer_obj.delete()
            vacancies(update, context)
            return VACANCY_ACTIONS

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
        if not question_obj.is_required:
            keyboards.append([get_word("skip", update)])
        keyboards.append([get_word("back", update)])
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True),
        )
        return ANSWERING

    # check is answer photo
    try:
        # try to download photo
        p = bot.getFile(update.message.photo[-1].file_id)
        *args, file_name = str(p.file_path).split("/")
        d_photo = p.download("files/payment/{}".format(file_name))
        answer_obj.payment = str(d_photo).replace("files/", "")

    except:
        # answer is not photo object
        update.message.reply_text(get_word("send photo", update))
        return ASK_PAYMENT

    # end answering
    answer_obj.end = True
    answer_obj.date = datetime.now()
    answer_obj.save()
    Statement.objects.create(answer=answer_obj, status="waiting")
    update.message.reply_text(get_word("completed answering", update))
    vacancies(update, context)
    return VACANCY_ACTIONS
