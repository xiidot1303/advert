from django.forms import ModelForm, widgets, ModelMultipleChoiceField
from app.models import *
from django import forms


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = {
            "questionuz",
            "questionru",
            "variantsuz",
            "variantsru",
            "index",
            "req_photo",
            "is_required",
        }
        widgets = {
            "questionuz": forms.Textarea(attrs={"class": "form-control"}),
            "questionru": forms.Textarea(attrs={"class": "form-control"}),
            "variantsuz": forms.TextInput(attrs={"class": "form-control"}),
            "variantsru": forms.TextInput(attrs={"class": "form-control"}),
            "index": forms.TextInput(attrs={"class": "form-control"}),
            "req_photo": forms.CheckboxInput(attrs={"class": "custom-control-input"}),
            "is_required": forms.CheckboxInput(attrs={"class": "custom-control-input"}),
        }
        labels = {
            "questionuz": "Вопрос на Узбекском",
            "questionru": "Вопрос на Русском",
            "variantsuz": "Варианты на Узбекском",
            "variantsru": "Варианты на Русском",
            "index": "Индекс",
            "req_photo": "Ответ должен содержать  с фотографиям",
            "is_required": "Обязательное поле",
        }

    field_order = [
        "questionuz",
        "questionru",
        "variantsuz",
        "variantsru",
        "index",
        "req_photo",
        "is_required",
    ]


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = {"answer", "photo"}
        widgets = {
            # 'answer': forms.Textarea(attrs={'class': 'form-control', "style":"height: 200px;"}),
            "answer": forms.TextInput(
                attrs={
                    "class": "custom-select form-control choicesjs",
                    "style": "size: 10px",
                }
            ),
            "photo": forms.FileInput(attrs={"class": "custom-file-input"}),
        }
        labels = {
            "answer": "Ответы",
            "photo": "Фото",
        }

    field_order = ["answer", "photo"]


class AnswerCreateForm(ModelForm):
    class Meta:
        model = Answer
        fields = {"user", "answer", "photo"}
        widgets = {
            # 'answer': forms.Textarea(attrs={'class': 'form-control', "style":"height: 200px;"}),
            "answer": forms.TextInput(
                attrs={
                    "class": "custom-select form-control choicesjs",
                    "style": "size: 10px",
                }
            ),
            "photo": forms.FileInput(attrs={"class": "custom-file-input"}),
            "user": forms.Select(
                attrs={"class": "custom-select form-control choicesjs"}
            ),
        }
        labels = {
            "answer": "Ответы",
            "photo": "Фото",
            "user": "Пользовател",
        }

    field_order = ["answer", "photo", "user"]


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = {"textru", "textuz", "card"}
        widgets = {
            "card": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "card": "Номер карта",
        }

    field_order = ["textru", "textuz", "card"]


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = {"group_id"}
        widgets = {
            "group_id": forms.TextInput(attrs={"class": "form-control"}),
        }

        labels = {"group_id": "ID"}


class ModelCommaSeparatedChoiceField(ModelMultipleChoiceField):
    widget = forms.SelectMultiple(
        attrs={"class": "custom-select form-control choicesjs", "multiple": True}
    )

    def clean(self, value):
        if value is not None:

            value = [item.strip() for item in value.split(",")]  # remove padding
        return super(ModelCommaSeparatedChoiceField, self).clean(value)


class MessageForm(ModelForm):
    # users = ModelCommaSeparatedChoiceField(
    #            required=False,
    #            queryset=Bot_user.objects.filter(),
    #            to_field_name='pk')
    class Meta:
        model = Message
        fields = {"users", "all", "text", "photo"}
        labels = {
            "users": "Пользователи",
            "all": "Все",
            "text": "Текст",
            "photo": "Фото",
        }

        widgets = {
            "users": forms.SelectMultiple(
                attrs={"class": "custom-select form-control choicesjs"}
            ),
            "all": forms.CheckboxInput(
                attrs={"class": "custom-control-input bg-primary", "checked": False}
            ),
            "text": forms.Textarea(
                attrs={"class": "form-control", "style": "height: 200px;"}
            ),
            "photo": forms.FileInput(attrs={"class": "custom-file-input"}),
        }

    field_order = ["all", "photo", "users", "text"]


class ProfileForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    email = forms.CharField(max_length=200, required=False)
