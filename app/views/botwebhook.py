from django.http import HttpResponse
from telegram import Update
from bot.update import dp, updater
import json
from django.views.decorators.csrf import csrf_exempt
from config import ENVIRONMENT


@csrf_exempt
def bot_webhook(request):

    if ENVIRONMENT == "local":
        updater.start_polling()
    else:
        update = Update.de_json(json.loads(request.body.decode("utf-8")), dp.bot)
        dp.process_update(update)
    return HttpResponse("Bot started!")
