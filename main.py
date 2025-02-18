import telebot
from keyboards import *
from config import *
from info import *
import time

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения сообщений, отправленных ботом
bot_messages = {}

# Функция для отправки сообщений в твой чат с информацией о пользователе
def send_message_to_me(text):
    my_chat_id = "1616464024"  # Замените на ID вашего чата или канала
    bot.send_message(chat_id=my_chat_id, text=text)

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name if user.last_name else "N/A"
    username = user.username if user.username else "N/A"
    
    # Сохранение данных пользователя или выполнение действий
    user_info = f"User ID: {user_id}\nИмя: {first_name}\nФамилия: {last_name}\nИмя пользователя: {username}"
    send_message_to_me(user_info)
    
    file = open('img/logo.jpg', 'rb')
    sent_message = bot.send_photo(message.chat.id, file, caption=greet_user(message), parse_mode='html', reply_markup=get_main_markup())
    
    # Сохранение ID отправленного сообщения
    if message.chat.id not in bot_messages:
        bot_messages[message.chat.id] = []
    bot_messages[message.chat.id].append(sent_message.message_id)

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
        file_vid = open('img/vid_kor.mp4', 'rb')
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
