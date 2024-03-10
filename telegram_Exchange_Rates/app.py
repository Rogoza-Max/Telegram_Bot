import telebot
from currency_converter import CurrencyConverter
from telebot import types 

bot = telebot.TeleBot('TOKEN')
convector = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму ')
    bot.register_next_step_handler(message, summa)



def summa(message):
    global amount
    try:  # обработчик исключения 
         amount = int(message.text.strip()) # полученные данные конвектируем число 
    except ValueError: 
         bot.send_message(message.chat.id, 'Неверный формат записи! Ведите сумму: ')
         bot.register_next_step_handler(message, summa)
         return # если неправильный вод суммы код выполнятся не будет 

    if amount > 0:
         
        markup = types.InlineKeyboardMarkup(row_width=2) # в одном ряду создаем две кнопки 
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data="eur/usd")
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data="usd/gbp")
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data="else")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else: 
        bot.send_message(message.chat.id, 'Число должно быть больше 0. Впишите сумму: ')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/') # приводим текст к верхнему регстру (split разделить строку по определенному символу)
        res = convector.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Результат: {round(res, 2)}. Впишите новое значение')
        bot.register_next_step_handler(call.message, summa)
    else: 
        bot.send_message(call.message.chat.id, 'Введите пару значение через /')
        bot.register_next_step_handler(call.message, mycurrency)
        

def mycurrency(message):
    try: 
        values = message.text.upper().split('/')
        res = convector.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Результат: {round(res, 2)}. Впишите новое значение')
        bot.register_next_step_handler(message, summa)
    except Exception: 
         bot.send_message(message.chat.id, 'Что-то не так! Впишите значение заново')
         bot.register_next_step_handler(message, mycurrency)


bot.polling(non_stop=True)