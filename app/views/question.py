from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from app.models import *
from app.forms import *


@login_required
def question_list(request):
    questions = Question.objects.all().order_by("index")
    context = {"questions": questions}
    return render(request, "question/allquestions.html", context)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    template_name = "question/create_question.html"
    form_class = QuestionForm
    success_url = "/question/list"
    # success_url = '/question_detail/{id}'


class QuestionEditView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "question/update_question.html"
    # success_url = '/question_detail/{id}'
    success_url = "/question/list"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


@login_required
def question_delete(request, pk):
    question = Question.objects.get(pk=pk)
    question.delete()
    return redirect(question_list)
