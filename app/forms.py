from django.forms import ModelForm, widgets
from app.models import *
from django import forms

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = {'questionuz', 'questionru', 'variantsuz', 'variantsru', 'index', 'req_photo', 'is_required'}
        widgets = {
            'questionuz': forms.Textarea(attrs={'class': 'form-control'}),
            'questionru': forms.Textarea(attrs={'class': 'form-control'}), 
            'variantsuz': forms.TextInput(attrs={'class': 'form-control'}),  
            'variantsru': forms.TextInput(attrs={'class': 'form-control'}),  
            'index': forms.TextInput(attrs={'class': 'form-control'}), 
            'req_photo': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'is_required': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }
        labels = {
            'questionuz': 'Вопрос на Узбекском',
            'questionru': 'Вопрос на Русском',
            'variantsuz': 'Варианты на Узбекском',
            'variantsru': 'Варианты на Русском', 
            'index': 'Индекс', 
            'req_photo': 'Ответ должен содержать  с фотографиям', 
            'is_required': 'Обязательное поле',
        }
    field_order = ['questionuz', 'questionru', 'variantsuz', 'variantsru', 'index', 'req_photo', 'is_required']

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = {'textru', 'textuz', 'card'}
        widgets = {
            'card': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'card': 'Номер карта',
        }
    field_order = ['textru', 'textuz' , 'card']

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = {'group_id'}
        widgets = {
            'group_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'group_id': 'ID'
        }



class ProfileForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    email = forms.CharField(max_length=200, required=False)