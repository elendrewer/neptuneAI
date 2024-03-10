import telebot
from test import *
import os


bot = telebot.TeleBot('6913733741:AAFjal-3l72-EnC8h_MAV9LOzQQXRgXCsW8')

@bot.message_handler(func=lambda message: True)
def putimg(message):
    bot.send_message(message.chat.id,"бот готовит ваше изображение😊, обычно это занимает около 40 секунд.")
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'C18CFED3080CB4D9EA3470D44C3C7F99', '06E91E54D8F83FD78A6BFE43CD57A5A7')
    model_id = api.get_model()
    uuid = api.generate(message.text, model_id)
    images = api.check_generation(uuid)
    pathh = f"img/{message.from_user.id}.png"
    api.b64i(images,pathh)
    photo = open(pathh, 'rb')
    bot.send_photo(message.chat.id, photo) 
    os.remove(pathh)

bot.infinity_polling()