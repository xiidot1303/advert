from django.forms import ModelForm, widgets
from app.models import *
from django import forms

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = {'questionuz', 'questionru', 'variantsuz', 'variantsru', 'index', 'req_photo'}
        widgets = {
            'questionuz': forms.Textarea(attrs={'class': 'form-control'}),
            'questionru': forms.Textarea(attrs={'class': 'form-control'}), 
            'variantsuz': forms.TextInput(attrs={'class': 'form-control'}),  
            'variantsru': forms.TextInput(attrs={'class': 'form-control'}),  
            'index': forms.TextInput(attrs={'class': 'form-control'}), 
            'req_photo': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }
        labels = {
            'questionuz': 'Вопрос на Узбекском',
            'questionru': 'Вопрос на Русском',
            'variantsuz': 'Варианты на Узбекском',
            'variantsru': 'Варианты на Русском', 
            'index': 'Индекс', 
            'req_photo': 'Ответ должен содержать  с фотографиям', 
        }
    field_order = ['questionuz', 'questionru', 'variantsuz', 'variantsru', 'index', 'req_photo']


class Profile(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    password = forms.CharField(max_length=50, required=False)