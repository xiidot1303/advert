from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from app.models import *
from app.forms import *


class GroupEditView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "group/update_group.html"
    success_url = "/group/update/1/"
