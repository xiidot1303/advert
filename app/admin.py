from operator import imod
from django.contrib import admin
from app.models import *

class Bot_userAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'phone', 'lang')
    search_fields = ('user_id', 'name', 'phone')
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'variants', 'index', 'lang')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'date', 'answer')

class StatementAdmin(admin.ModelAdmin):
    list_display = ('answer', 'status')

class Backup_questionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'variants', 'index', 'answer')

admin.site.register(Bot_user, Bot_userAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Statement, StatementAdmin)
admin.site.register(Backup_question, Backup_questionAdmin)