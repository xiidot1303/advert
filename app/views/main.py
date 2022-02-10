from django.http import HttpResponse, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

def main_menu(request):
    return render(request, 'views/main.html')