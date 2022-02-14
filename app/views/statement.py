from cmath import log
from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from functions.bot import split_by_slash


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
    context = {'questions': questions, 'answers': answer_list, 'photo': photo, 'st_pk': st_pk}
    return render(request, 'statement/answer.html', context)


@login_required
def confirm_statement(request, pk):
    obj = Statement.objects.get(pk=pk)
    obj.status = 'confirmed'
    obj.save()
    return redirect(list_statements)


