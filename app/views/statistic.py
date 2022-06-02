from django.shortcuts import render
from app.models import *


def bot_users(request):
    users = BotUser.objects.all().order_by("-date")
    context = {"users": users}
    return render(request, "statistic/users.html", context)
