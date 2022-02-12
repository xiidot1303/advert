from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def main_menu(request):
    return render(request, 'views/main.html')

@login_required
def get_photos(request, folder, file):
    f = open('files/photos/{}/{}'.format(folder, file), 'rb')
    return FileResponse(f)