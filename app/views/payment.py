from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from app.models import *
from app.forms import *


class PaymentEditView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment/update_payment.html'
    # success_url = '/question_detail/{id}'
    success_url = '/payment/update/1/'
    