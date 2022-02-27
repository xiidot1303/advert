from app.models import Message, Bot_user
from config import TELEGRAM_BOT_API_TOKEN
import telegram

def update():

    bot = telegram.Bot(token = TELEGRAM_BOT_API_TOKEN)
    for msg in Message.objects.all():

        if msg.all:
            users = Bot_user.objects.all()
        elif msg.users.all():
            users = msg.users.all()
        else:
            users = []

        for user in users:
            try:
            # if True:
                if msg.photo and msg.text:
                    bot.sendPhoto(chat_id = user.user_id, photo=msg.photo, caption=msg.text)
                elif msg.photo:
                    bot.sendPhoto(chat_id = user.user_id, photo=msg.photo)
                elif msg.text:
                    bot.sendMessage(chat_id=user.user_id, text=msg.text)
            except:
                nothing = True
        msg.delete()


