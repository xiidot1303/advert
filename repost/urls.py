"""repost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView
from app.views.group import GroupEditView
from app.views.payment import PaymentEditView
from app.views.question import QuestionCreateView, QuestionEditView, question_delete, question_list

from config import *
from app.views.botwebhook import bot_webhook
from app.views.main import *
from app.views.statement import *
from app.views.statistic import *
from app.views.admin import *

urlpatterns = [
    #main
    path('xiidot1303/', admin.site.urls),
    path(TELEGRAM_BOT_API_TOKEN, bot_webhook),
    path('', main_menu, name='main_menu'),

    #auth
    path('accounts/login/', LoginView.as_view()),
    path('changepassword/', PasswordChangeView.as_view(template_name = 'registration/change_password.html'), name='editpassword'),
    path('changepassword/done/', PasswordChangeDoneView.as_view(template_name = 'registration/afterchanging.html'), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # get file
    path('files/<str:folder>/<str:file>/', get_photos, name='get_photo'),

    #statement
    path('statement/list', list_statements, name='statement_list'),
    path('statement/confirm/<int:pk>/', confirm_statement, name='statement_confirm'),
    path('statement/answers/<int:pk>', answer, name='statement_answer'),
    path('statement/shared', shared_statements, name='statement_shared'),



    #question
    path('question/create', QuestionCreateView.as_view(), name = 'question_create'),
    path('question/list', question_list, name='question_list'),
    path('question/update/<int:pk>/', QuestionEditView.as_view(), name='question_update'),
    path('question/delete/<int:pk>/', question_delete, name = 'question_delete'),

    #settings
    path('payment/update/<int:pk>/', PaymentEditView.as_view(), name = 'payment_update'),
    path('group/update/<int:pk>/', GroupEditView.as_view(), name = 'group_update'),
    path('profile', change_profile, name = "change_profile"),


    #statistic
    path('statistic/users', bot_users, name='statistic_users'),

    #message
    path('sendMessage', MessageCreateView.as_view(), name='send_message'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
