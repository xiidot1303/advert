from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models.functions import TruncDay
from django.db.models import Count

from datetime import datetime, timedelta
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
    amount_bot_users = [count_bot_users, count_daily_bot_users]

    amount_bot_clients = len(Bot_user.objects.filter(is_client=True))
    amount_posts = len(Statement.objects.filter(status='confirmed'))

    def make_date(obj):
        obj = obj + timedelta(hours=5)
        return obj.strftime("%Y-%m-%dT%H:%m:%S")
        
    dates_users = list(map(lambda l: make_date(l[0]), list(Bot_user.objects.annotate(day=TruncDay('date')).values('day').annotate(c=Count('id')).values_list('day', 'c'))))
    dates_posts = list(map(lambda l: make_date(l[0]), list(Statement.objects.filter(status='confirmed').annotate(answer__day=TruncDay('answer__date')).values('answer__day').annotate(c=Count('id')).values_list('answer__day', 'c'))))

    bot_users_by_date = list(map(lambda l: int(l[1]), list(Bot_user.objects.annotate(day=TruncDay('date')).values('day').annotate(c=Count('id')).values_list('day', 'c'))))
    
    posts_by_date = list(map(lambda l: int(l[1]), list(Statement.objects.filter(status='confirmed').annotate(answer__day=TruncDay('answer__date')).values('answer__day').annotate(c=Count('id')).values_list('answer__day', 'c'))))


    most_viewed_posts = Statement.objects.filter(status='confirmed').order_by('-views')[:10]

    context = {'amount_bot_users': amount_bot_users, 'amount_bot_clients': amount_bot_clients, 'amount_posts': amount_posts, 
    'bot_users_by_date': bot_users_by_date, 'dates_users': dates_users, 'posts_by_date': posts_by_date, 'dates_posts': dates_posts, 
    'most_viewed_posts': most_viewed_posts}
    return render(request, 'views/main.html', context)

@login_required
def get_photos(request, folder, file):
    f = open('files/{}/{}'.format(folder, file), 'rb')
    return FileResponse(f)