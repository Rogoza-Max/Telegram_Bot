import json
import requests
import telebot


bot = telebot.TeleBot('TOKEN') 
API = '56b09686009401884b4577f465368d33' # key  с ссйта https://openweathermap.org/ (необходима регистрация)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название города: ')


@bot.message_handler(content_types=['text'])
def get_wather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас погода: {temp}')

        image = 'солнце.jpeg' if temp > 5.0 else 'холод.jpeg'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)

    else:
        bot.reply_to(message, f'Город указан не верно! Попробуйте снова.')


bot.polling(non_stop=True)


