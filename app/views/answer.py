from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView, CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from app.views.statement import confirm_statement, list_statements
from app.forms import AnswerForm, AnswerCreateForm
from functions.bot import split_by_slash
from functions.form import comatoslash
from datetime import datetime


@login_required
def card(request, pk):
    answer_obj = Answer.objects.get(pk=pk)
    st_pk = Statement.objects.get(answer_id=pk).pk
    name = answer_obj.user.name
    phone_number = answer_obj.user.phone
    date = answer_obj.date
    # check only text or full
    if not answer_obj.answer:
        text = answer_obj.text
        context = {
            "st_pk": st_pk,
            "name": name,
            "phone_number": phone_number,
            "date": date,
            "text": text,
        }
        return render(request, "answer/answer_only_text.html", context)

    questions = Backup_question.objects.filter(answer=pk)
    answer_list = split_by_slash(answer_obj.answer)
    photo = answer_obj.photo
    context = {
        "questions": questions,
        "answers": answer_list,
        "photo": photo,
        "st_pk": st_pk,
        "name": name,
        "phone_number": phone_number,
        "date": date,
        "answer_pk": answer_obj.pk,
    }
    return render(request, "answer/answer.html", context)


class AnswerEditView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = "answer/update_answer.html"
    success_url = "/answer/detail/{id}/"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["questions"] = Backup_question.objects.filter(
            answer=context["object"].pk
        )
        return context


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name = "answer/create_answer.html"
    success_url = "/answer/detail/{id}/"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["questions"] = Question.objects.all().order_by("index")
        return context


class AnswerDetailView(LoginRequiredMixin, DetailView):
    model = Answer
    template_name = "answer/answer_detail.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     answer_obj = context['answer']
    #     self.st_id = st_obj.pk
    #     return context

    def get(self, request, *args, **kwargs):

        answer_obj = Answer.objects.get(pk=self.kwargs["pk"])
        answer_obj.answer = comatoslash(answer_obj.answer)
        answer_obj.save()
        try:  # check that is statement objects available
            st_obj = Statement.objects.get(answer=answer_obj)
            return redirect(confirm_statement, pk=st_obj.pk)
        except:
            answer_obj.end = True
            answer_obj.date = datetime.now()
            answer_obj.save()
            Statement.objects.create(answer=answer_obj, status="waiting")
            user = answer_obj.user
            # back up questions
            n = 1
            for q in Question.objects.all().order_by("index"):
                if user.lang == "uz":
                    Backup_question.objects.create(
                        user=user,
                        question=q.questionuz,
                        variants=q.variantsuz,
                        index=n,
                        req_photo=q.req_photo,
                        is_required=q.is_required,
                        answer=answer_obj.pk,
                    )
                else:
                    Backup_question.objects.create(
                        user=user,
                        question=q.questionru,
                        variants=q.variantsru,
                        index=n,
                        req_photo=q.req_photo,
                        is_required=q.is_required,
                        answer=answer_obj.pk,
                    )
                n += 1

            return redirect(list_statements)
        # return super().get(self, request, *args, **kwargs)
