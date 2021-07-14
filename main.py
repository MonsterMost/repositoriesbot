from telebot import TeleBot
import requests
from bs4 import BeautifulSoup

TOKEN = '1704494083:AAFcXJz4UGpxPm2qs3Ra9z9TkdVeKtWP_8A'

URL = 'https://github.com/MonsterMost?tab=repositories'
github = 'https://github.com'
bot = TeleBot(token=TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     f'Привет, {message.from_user.first_name}!\nЗдесь представлен список проектов Фомичева Евгения')
    return_list(message)


def return_list(message):
    list1 = get_list()
    chat_id = message.chat.id
    for msg in list1:
        bot.send_message(chat_id, msg)


def get_list():
    responce = requests.get(URL)
    html = responce.text
    soup = BeautifulSoup(html, 'html.parser')
    list1 = []
    names = soup.find_all('li',
                          class_='col-12 d-flex width-full py-4 border-bottom color-border-secondary public source')
    for name in names:
        definition = name.find('h3', class_='wb-break-all').get_text(strip=True)
        description = name.find('p').get_text(strip=True)
        language = name.find('span', class_='ml-0 mr-3').get_text(strip=True)
        # print(definition)
        # print(description)
        # print(language)
        msg = f'''<b>Название проекта:</b>\n{definition}\n<b>Описание:</b>\n{description}\n<b>Язык:</b> {language}'''
        list1.append(msg)
    return list1


bot.polling(none_stop=True)
