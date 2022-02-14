from pyexpat import model
from re import template
from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from app.models import *
from app.forms import *

# @login_required
# def list_question(request):

class QuestionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'question/create_question.html'
    form_class = QuestionForm
    success_url = '/question_detail/{id}'
    

def question_list(request):
    questions = Question.objects.all().order_by('index')
    context = {'questions': questions}
    return render(request, 'question/allquestions.html', context)

class QuestionEditView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    success_url = '/question_detail/{id}'
    