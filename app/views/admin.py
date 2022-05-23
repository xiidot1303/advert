from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView

from app.forms import *


@login_required
def change_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            user = request.user
            user.username = username
            user.email = email
            user.save()
            return redirect(change_profile)
        else:
            user = request.user
            username = user
            email = user.email
            context = {"form": form, "username": username, "email": email}
            return render(request, "profile/change_profile.html", context)
    else:
        form = ProfileForm()
        user = request.user
        username = user
        email = user.email
        context = {"form": form, "username": username, "email": email}
        return render(request, "profile/change_profile.html", context)


class MessageCreateView(LoginRequiredMixin, CreateView):
    template_name = "views/send_message.html"
    form_class = MessageForm
    success_url = "/sendMessage/success"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = context["view"].kwargs["status"]
        if status == "success":
            context["alert"] = True
        else:
            context["alert"] = False
        return context
