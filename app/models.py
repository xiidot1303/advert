import os

from django.db import models


class BotUser(models.Model):
    user_id = models.IntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=200)
    username = models.CharField(null=True, blank=True, max_length=200)
    firstname = models.CharField(null=True, blank=True, max_length=500)
    phone = models.CharField(null=True, blank=True, max_length=40)
    lang = models.CharField(null=True, blank=True, max_length=5)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)
    is_client = models.BooleanField(blank=True, null=True)

    def __str__(self) -> str:
        try:
            return self.name + " " + str(self.phone)
        except:
            return super().__str__()


class Question(models.Model):
    questionuz = models.CharField(null=True, blank=True, max_length=500)
    questionru = models.CharField(null=True, blank=True, max_length=500)
    variantsuz = models.CharField(null=True, blank=True, max_length=300)
    variantsru = models.CharField(null=True, blank=True, max_length=300)
    index = models.IntegerField(null=True, blank=True)
    req_photo = models.BooleanField(blank=True, null=True)  # is required photo
    is_required = models.BooleanField(blank=True, null=True)  #  is required answer


class Answer(models.Model):
    user = models.ForeignKey(
        "app.BotUser", null=True, blank=False, on_delete=models.PROTECT
    )
    questions = models.CharField(
        null=True, blank=True, max_length=3000
    )  # save questions by "/""
    date = models.DateTimeField(null=True, blank=True, max_length=20)
    answer = models.CharField(null=True, blank=True, max_length=300)
    new_answer = models.CharField(null=True, blank=True, max_length=300)
    photo = models.FileField(upload_to="photos/", null=True, blank=True)
    payment = models.FileField(upload_to="payment/", null=True, blank=True)
    text = models.TextField(blank=True, null=True, max_length=3000, default="")

    end = models.BooleanField(
        null=True, blank=True, default=False
    )  # completed answer or not

    def filename(self):
        return os.path.basename(self.photo.name)

    # def __str__(self) -> str:
    #     return self.


class Statement(models.Model):
    answer = models.ForeignKey(
        "Answer", null=True, blank=False, on_delete=models.PROTECT
    )
    status = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=(
            ("waiting", "waiting"),
            ("cancelled", "cancelled"),
            ("confirmed", "confirmed"),
        ),
    )
    payment_status = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=((0, "В ожидании"), (-1, "Отменено"), (1, "Оплачено")),
        default=0,
    )
    invoice_id = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True, default=0)


class Backup_question(models.Model):
    user = models.ForeignKey(
        "app.BotUser", null=True, blank=False, on_delete=models.PROTECT
    )
    question = models.CharField(null=True, blank=True, max_length=500)
    variants = models.CharField(null=True, blank=True, max_length=300)
    index = models.IntegerField(null=True, blank=True)
    req_photo = models.BooleanField(blank=True, null=True)  # is required photo
    is_required = models.BooleanField(blank=True, null=True)  #  is required answer
    answer = models.IntegerField(null=True, blank=True)  # answer ID


class Group(models.Model):
    group_id = models.CharField(null=True, blank=True, max_length=30)
    name = models.CharField(null=True, blank=True, max_length=500)


class Payment(models.Model):
    textuz = models.CharField(null=True, blank=True, max_length=1000)
    textru = models.CharField(null=True, blank=True, max_length=1000)
    card = models.CharField(null=True, blank=True, max_length=50)
    amount = models.IntegerField(null=True, blank=True)


class Message(models.Model):
    users = models.ManyToManyField("app.BotUser", blank=True)
    all = models.BooleanField(blank=True, null=True)
    text = models.TextField(blank=True, null=True, max_length=1000)
    photo = models.FileField(upload_to="messages/", null=True, blank=True)
