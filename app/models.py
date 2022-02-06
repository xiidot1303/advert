
from django.db import models

class Bot_user(models.Model):
    user_id = models.IntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=200)
    username = models.CharField(null=True, blank=True, max_length=200)
    phone = models.CharField(null=True, blank=True, max_length=40)
    lang = models.CharField(null=True, blank=True, max_length=5)
    date = models.DateTimeField(db_index = True, null=True, auto_now_add=True, blank=True)
    def __str__(self) -> str:
        try:
            return self.username + ' ' + str(self.user_id)
        except:
            return super().__str__()


class Question(models.Model):
    question = models.CharField(null=True, blank=True, max_length=500)
    variants = models.CharField(null=True, blank=True, max_length=300)
    index = models.IntegerField(null=True, blank=True)
    lang = models.CharField(null=True, blank=True, max_length=10)

class Answer(models.Model):
    user = models.ForeignKey('Bot_user', null=True, blank=False, on_delete=models.PROTECT)
    questions = models.CharField(null=True, blank=True, max_length=3000)  #save questions by "/""
    date = models.DateField(null=True, blank=True, max_length=20)
    answer = models.CharField(null=True, blank=True, max_length=300)
    photo = models.FileField(upload_to='photos/', null=True, blank=True)
    end = models.BooleanField(null=True, blank=True, default=False) # completed answer or not

    # def __str__(self) -> str:
    #     return self.

class Statement(models.Model):
    answer = models.ForeignKey('Answer', null=True, blank=False, on_delete=models.PROTECT)
    status = models.CharField(null=True, blank=True, max_length=20, choices=(('waiting', 'waiting'), ('cancelled', 'cancelled'), ('confirmed', 'confirmed')))