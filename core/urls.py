from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from app.views.group import GroupEditView
from app.views.payment import PaymentEditView
from app.views.question import (
    QuestionCreateView,
    QuestionEditView,
    question_delete,
    question_list,
)

from config import *
from app.views.botwebhook import bot_webhook
from app.views.main import *
from app.views.statement import *
from app.views.statistic import *
from app.views.admin import *
from app.views.answer import *
from app.views import click_api

urlpatterns = [
    # main
    path("xiidot1303/", admin.site.urls),
    path(TELEGRAM_BOT_API_TOKEN, bot_webhook),
    path("", main_menu, name="main_menu"),
    # auth
    path("accounts/login/", LoginView.as_view()),
    path(
        "changepassword/",
        PasswordChangeView.as_view(template_name="registration/change_password.html"),
        name="editpassword",
    ),
    path(
        "changepassword/done/",
        PasswordChangeDoneView.as_view(template_name="registration/afterchanging.html"),
        name="password_change_done",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    # get file
    path("files/<str:folder>/<str:file>/", get_photos, name="get_photo"),
    # statement
    path("statement/list", list_statements, name="statement_list"),
    path("statement/confirm/<int:pk>/", confirm_statement, name="statement_confirm"),
    path("statement/answers/<int:pk>", card, name="statement_answer"),
    path("statement/shared", shared_statements, name="statement_shared"),
    # answer
    path("answer/update/<int:pk>/", AnswerEditView.as_view(), name="answer_update"),
    path("answer/detail/<int:pk>/", AnswerDetailView.as_view(), name="answer_detail"),
    path("answer/create", AnswerCreateView.as_view(), name="answer_create"),
    # question
    path("question/create", QuestionCreateView.as_view(), name="question_create"),
    path("question/list", question_list, name="question_list"),
    path(
        "question/update/<int:pk>/", QuestionEditView.as_view(), name="question_update"
    ),
    path("question/delete/<int:pk>/", question_delete, name="question_delete"),
    # settings
    path("payment/update/<int:pk>/", PaymentEditView.as_view(), name="payment_update"),
    path("group/update/<int:pk>/", GroupEditView.as_view(), name="group_update"),
    path("profile", change_profile, name="change_profile"),
    # statistic
    path("statistic/users", bot_users, name="statistic_users"),
    # message
    path("sendMessage/<str:status>", MessageCreateView.as_view(), name="send_message"),
    # click-api
    path("click/prepare", click_api.prepare),
    path("click/complate", click_api.complate),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
