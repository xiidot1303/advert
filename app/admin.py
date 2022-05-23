from operator import imod
from django.contrib import admin
from app.models import *


class Bot_userAdmin(admin.ModelAdmin):
    list_display = ("user_id", "name", "phone", "lang")
    search_fields = ("user_id", "name", "phone")


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("questionuz", "questionru", "variantsuz", "variantsru", "index")


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "date", "answer", "new_answer")


class StatementAdmin(admin.ModelAdmin):
    list_display = ("answer", "status", "pk")


class Backup_questionAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "variants", "index", "answer")


class GroupAdmin(admin.ModelAdmin):
    list_display = ("group_id", "name")


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("textru", "textuz", "card")


class MessageAdmin(admin.ModelAdmin):
    list_display = ("pk", "all", "text")


admin.site.register(Bot_user, Bot_userAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Statement, StatementAdmin)
admin.site.register(Backup_question, Backup_questionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Message, MessageAdmin)
