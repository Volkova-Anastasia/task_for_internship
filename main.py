import telebot
import config
import gspread
import time
import datetime
import schedule
from time import sleep
from threading import Thread
from telebot import types


bot = telebot.TeleBot(config.TOKEN)

"""Выгружаем данные из Google Таблиц"""
gs = gspread.service_account(filename='name_for_json_file.json')
sh = gs.open_by_key('token_for_google_sheets')
worksheet = sh.sheet1
res = worksheet.col_values(1)
dopmat = worksheet.col_values(2)


"""Запуск работы бота у пользователя командой /start. Клавиатурные кнопки"""
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Hello, World! \n'
                                      '<u>Я – твой онлайн-помощник по курсу Python для чайников!</u>\n\n'
                                      'Я помогу тебе начать твое обучение в Питоне с нуля. Если ты хочешь получать от меня ежедневное напоминание, вызови команду /time </b>', parse_mode='html')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    push1 = types.KeyboardButton("Видеоматериалы")
    push2 = types.KeyboardButton("Дополнительные материалы")
    markup.add(push1, push2)
    bot.send_message(message.chat.id, 'Выбери то, что тебя интересует :)', reply_markup = markup)

"""Запуск команды /time"""
@bot.message_handler(commands=['time'])
def timework(message):
     bot.send_message(message.chat.id, 'Если ты хочешь получать от меня ежедневные уведомления, отправь следующим сообщением нужное тебе <u><b>время в формате 00:00</b></u>\n'
                                       '<u><b>!ВНИМАНИЕ!</b></u>\n'
                                       'Время уведомления в последствии <u><b>нельзя</b></u> поменять или удалить', parse_mode='html')


def helpme(message):
    bot.send_message(message, "Время вернуться к учебе! Рекомендую посмотреть парочку новых видео!")

def waiting():
    while True:
        schedule.run_pending()
        sleep(1)

"""Отправка данных из разделов таблиц. Установка времени уведомления"""
@bot.message_handler(content_types=['text'])
def mess(message):
    global chat_id
    chat_id = int(message.chat.id)
    if (message.text == "Видеоматериалы"):
        for i in range(len(res)):
            bot.send_message(message.chat.id, res[i])
    elif (message.text == "Дополнительные материалы"):
        for i in range(len(dopmat)):
            bot.send_message(message.chat.id, dopmat[i])
    elif (':' not in message.text):
        bot.send_message(message.chat.id, 'Я тебя не понимаю')
    elif (message.text.split(':')[0].isdigit() is True and message.text.split(':')[1].isdigit() is True and int(message.text.split(':')[0])<24 and int(message.text.split(':')[1])<60):
        bot.send_message(message.chat.id, 'Отлично! Жди уведомление в назначенное время :)')
        schedule.every().day.at(message.text).do(helpme,message.chat.id)
        Thread(target=waiting).start()
    else:
        bot.send_message(message.chat.id, 'Извини, я не понимаю тебя. Выбери что-то из предложенного или попробуй еще раз')

bot.polling(none_stop=True)


