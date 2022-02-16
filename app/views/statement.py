from cmath import log
from unicodedata import name
from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from functions.bot import photo, split_by_slash
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_URL, GROUP, TELEGRAM_BOT_API_TOKEN

@login_required
def list_statements(request):
    sts = Statement.objects.filter(status = 'waiting')
    context = {'list': sts}
    return render(request, 'statement/list.html', context)


@login_required
def answer(request, pk):
    answer_obj = Answer.objects.get(pk=pk)
    questions = Backup_question.objects.filter(answer=pk)
    answer_list = split_by_slash(answer_obj.answer)
    photo = answer_obj.photo

    st_pk = Statement.objects.get(answer_id=pk).pk
    name = answer_obj.user.name
    phone_number = answer_obj.user.phone
    date = answer_obj.date
    context = {'questions': questions, 'answers': answer_list, 'photo': photo, 'st_pk': st_pk, 'name': name, 'phone_number': phone_number, 'date': date}
    return render(request, 'statement/answer.html', context)


@login_required
def confirm_statement(request, pk):
    obj = Statement.objects.get(pk=pk)
    obj.status = 'confirmed'
    # obj.save()
    answer_obj = obj.answer
    photo = answer_obj.photo
    id = pk


    # send to group or channel
    my_token = TELEGRAM_BOT_API_TOKEN
    bot = telegram.Bot(token=my_token)
    
    # try:
    i_go = InlineKeyboardButton(text = 'Перейти бот', url=BOT_URL)
    markup = InlineKeyboardMarkup([[i_go]])
    print(GROUP)
    bot.sendPhoto(chat_id=int(GROUP), photo=photo, caption='<b>ID:</b>'+str(id), reply_markup = markup, parse_mode = telegram.ParseMode.HTML)
    # except:
    #     error = True
    return redirect(list_statements)


