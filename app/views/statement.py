from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from app.models import *


def all_list(request):
    sts = Statement.objects.filter(status = 'waiting')
    context = {'list': sts}
    return render(request, 'statement/list.html', context)