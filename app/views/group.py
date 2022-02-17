from pyexpat import model
from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from app.models import *
from app.forms import *

class GroupEditView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'group/update_group.html'
    success_url = '/group/update/1/'