from cmath import log
from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *

@login_required
def list_statements(request):
    sts = Statement.objects.filter(status = 'waiting')
    context = {'list': sts}
    return render(request, 'statement/list.html', context)


@login_required
def confirm_statement(request, pk):
    obj = Statement.objects.get(pk=pk)
    obj.status = 'confirmed'
    obj.save()
    return redirect(list_statements)