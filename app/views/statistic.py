from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from functions.bot import photo, split_by_slash

def bot_users(request):
    users = Bot_user.objects.all().order_by('-date')
    context = {'users': users}
    return render(request, 'statistic/users.html', context)
    