import telebot
import sqlite3


bot = telebot.TeleBot('TOKEN') # вводим свой токен с телеграм бота 
name = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('my_bd.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS user (id int auto_increment primary key,name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем! Введите Ваше имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()
    
    conn = sqlite3.connect('my_bd.sql')
    cur = conn.cursor()

    cur.execute(f"INSERT INTO user (name, pass) VALUES('%s', '%s')" %(name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('my_bd.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM user')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n' 

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


if __name__ == '__main__':
    bot.polling(none_stop=True)