from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from app.models import *
from app.forms import *


class PaymentEditView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payment/update_payment.html"
    # success_url = '/question_detail/{id}'
    success_url = "/payment/update/1/"
