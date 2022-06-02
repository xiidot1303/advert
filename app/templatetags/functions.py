from django import template
from app.models import *
from functions.bot import *


register = template.Library()


@register.filter
def cuttext(text):
    if text:
        if len(text) > 14:
            r_text = text[:15] + "..."
        else:
            r_text = text
        return r_text
    else:
        return ""


@register.filter
def text_maker(obj):
    print(obj)
    answer_obj = obj
    questions = BackupQuestion.objects.filter(answer=answer_obj.pk)
    answers = split_by_slash(answer_obj.answer)
    list_answers = []
    n = 0
    for q in questions:
        if not q.req_photo:
            text = "{}: {}".format(q.question, answers[n])
            list_answers.append(text)
        n += 1
    return list_answers
