from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app.models import Group, Payment

@login_required
def main_menu(request):
    # create or get a payment objects that id = 1
    Payment.objects.get_or_create(pk=1)
    Group.objects.get_or_create(pk=1)
    return render(request, 'views/main.html')

@login_required
def get_photos(request, folder, file):
    f = open('files/{}/{}'.format(folder, file), 'rb')
    return FileResponse(f)