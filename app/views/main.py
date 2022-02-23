from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import datetime
from app.models import *

@login_required
def main_menu(request):
    # create or get a payment objects that id = 1
    Payment.objects.get_or_create(pk=1)
    Group.objects.get_or_create(pk=1)
    #-_-_-_-_-_-_-_
    count_bot_users = len(Bot_user.objects.all())
    today = datetime.now()
    count_daily_bot_users = len(Bot_user.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day))
    bot_users = [count_bot_users, count_daily_bot_users]

    bot_clients = len(Bot_user.objects.filter(is_client=True))

    context = {'bot_users': bot_users, 'bot_clients': bot_clients}
    return render(request, 'views/main.html')

@login_required
def get_photos(request, folder, file):
    f = open('files/{}/{}'.format(folder, file), 'rb')
    return FileResponse(f)