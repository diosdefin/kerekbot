import telebot
from keyboards import *
from config import *
from info import *
import time
import os

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения сообщений, отправленных ботом
bot_messages = {}

# Список для хранения ID всех пользователей
user_ids = set()

# Функция для отправки сообщений в твой чат с информацией о пользователе
def send_message_to_me(text):
    my_chat_id = "1616464024"  # Замените на ID вашего чата или канала
    bot.send_message(chat_id=my_chat_id, text=text)

# Функция для чтения счетчика из файла
def read_counter():
    if not os.path.exists('counter.txt'):
        return 0
    with open('counter.txt', 'r') as file:
        return int(file.read().strip())

# Функция для записи счетчика в файл
def write_counter(value):
    with open('counter.txt', 'w') as file:
        file.write(str(value))

# Функция для чтения ID пользователей из файла
def read_user_ids():
    if not os.path.exists('user_ids.txt'):
        return set()
    with open('user_ids.txt', 'r') as file:
        user_ids = set(int(line.strip()) for line in file)
    return user_ids

# Функция для записи ID пользователей в файл
def write_user_ids(user_ids):
    with open('user_ids.txt', 'w') as file:
        for user_id in user_ids:
            file.write(f"{user_id}\n")

user_ids = read_user_ids()

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name if user.last_name else "N/A"
    username = user.username if user.username else "N/A"

    # Сохранение ID пользователя
    user_ids.add(user_id)
    write_user_ids(user_ids)

    # Увеличиваем счетчик и сохраняем его
    counter = read_counter() + 1
    write_counter(counter)
    
    # Сохранение данных пользователя или выполнение действий
    user_info = f"{counter}. User ID: {user_id}\nИмя: {first_name}\nФамилия: {last_name}\nИмя пользователя: {username}"
    send_message_to_me(user_info)
    
    file = open('img/logo.jpg', 'rb')
    sent_message = bot.send_photo(message.chat.id, file, caption=greet_user(message), parse_mode='html', reply_markup=get_main_markup())
    
    # Сохранение ID отправленного сообщения
    if message.chat.id not in bot_messages:
        bot_messages[message.chat.id] = []
    bot_messages[message.chat.id].append(sent_message.message_id)

# Команда для отправки сообщения всем пользователям
@bot.message_handler(commands=['secret'])
def secret(message):
    if message.from_user.id == 1616464024:  # Замените на ваш Telegram ID, чтобы ограничить доступ к команде
        text = message.text[len('/secret '):]
        for user_id in user_ids:
            bot.send_message(chat_id=user_id, text=text)
    else:
        bot.reply_to(message, "У вас нет доступа к этой команде.")

# Команда для отправки сообщения конкретному пользователю
@bot.message_handler(commands=['direct'])
def direct(message):
    if message.from_user.id == 1616464024:  # Замените на ваш Telegram ID, чтобы ограничить доступ к команде
        try:
            parts = message.text.split(' ', 2)
            user_id = int(parts[1])
            text = parts[2]
            bot.send_message(chat_id=user_id, text=text)
        except (IndexError, ValueError):
            bot.reply_to(message, "Неверный формат команды. Используйте /direct <user_id> <сообщение>.")
    else:
        bot.reply_to(message, "У вас нет доступа к этой команде.")

# Обработчик для текстовых сообщений от пользователей
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name if user.last_name else "N/A"
    text = message.text
    
    # Отправка информации о сообщении вам
    user_info = f"User ID: {user_id}\nИмя: {first_name}\nФамилия: {last_name}\nСообщение: {text}"
    send_message_to_me(user_info)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # Удаление всех сообщений, отправленных ботом
    if callback.data == 'inactive':
        bot.answer_callback_query(callback.id, text="Бул курс жакынкы аралыкта кошулат.")
        return
    elif callback.message.chat.id in bot_messages:
        for msg_id in bot_messages[callback.message.chat.id]:
            try:
                bot.delete_message(callback.message.chat.id, msg_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение {msg_id}: {e}")
        bot_messages[callback.message.chat.id] = []

    if callback.data == 'main_str':
        file = open('img/logo.jpg', 'rb')
        welcome_message = greet_user(callback.message)
        sent_message = bot.send_photo(callback.message.chat.id, file, caption=welcome_message, parse_mode='html', reply_markup=get_main_markup())
        # Сохранение ID отправленного сообщения
        bot_messages[callback.message.chat.id].append(sent_message.message_id)

    elif callback.data == 'trial_lesson':
        file = open('img/tutorial.png', 'rb')
        sent_message = bot.send_photo(callback.message.chat.id, file, "Таанышуу сабагын танданыз:", reply_markup=get_trial_lesson_markup())
        # Сохранение ID отправленного сообщения
        bot_messages[callback.message.chat.id].append(sent_message.message_id)

    elif callback.data == 'long_kor':
        file = open('img/enes.jpg', 'rb')
        file_vid = open('img/vid_kor.MOV', 'rb')
        sent_photo = bot.send_photo(callback.message.chat.id, file, caption=teacher_kor, parse_mode='html')
        sent_video = bot.send_video(callback.message.chat.id, file_vid, caption=text_tutorial('корей', '🇰🇷'), parse_mode='html', reply_markup=get_bay('🇰🇷'))
        # Сохранение ID отправленных сообщений
        bot_messages[callback.message.chat.id].extend([sent_photo.message_id, sent_video.message_id])

    elif callback.data == 'buy_course':
        file = open('img/WhatsApp.png', 'rb')
        sent_message = bot.send_photo(callback.message.chat.id, file, caption=bay_course, parse_mode='html', reply_markup=get_main_markup_btn())
        # Сохранение ID отправленного сообщения
        bot_messages[callback.message.chat.id].append(sent_message.message_id)

#Этот блок добавляет обработку исключений для метода polling
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=30, long_polling_timeout=30)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(15)  # Задержка перед повторной попыткой
