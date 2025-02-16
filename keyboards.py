from telebot import types

def get_main_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('📚 Пробный сабак', callback_data='trial_lesson')
    btn3 = types.InlineKeyboardButton('🎓 Бугун сатып ал (1999сом)', callback_data='buy_course')
    markup.add(btn1, btn3)
    return markup

def get_trial_lesson_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('🇰🇷 Корей тили', callback_data='long_kor')
    btn2 = types.InlineKeyboardButton('🇷🇺 Орус тили (жакында)', callback_data='inactive')
    btn3 = types.InlineKeyboardButton('🇬🇧 Англис тили (жакында)', callback_data='inactive')
    btn4 = types.InlineKeyboardButton('🔙 Башкы меню', callback_data='main_str')
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def get_bay(flag):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_bay = types.InlineKeyboardButton(f'{flag} Бугун сатып ал', callback_data='buy_course')
    btn4 = types.InlineKeyboardButton('🔙 Башкы меню', callback_data='main_str')
    markup.add(btn_bay, btn4)
    return markup

def get_main_markup_btn():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn2 = types.InlineKeyboardButton(
        f'🇰🇷 Стандарт\n💰 900c акция', 
        url='https://wa.me/996552953495?text=Саламатсызбы,%20мен%20СТАНДАРТ%20тарифи%20боюнча(🇰🇷корей тили)'
    )
    btn3 = types.InlineKeyboardButton(
        f'🇰🇷 Вип\n💰 2500c акция', 
          url='https://wa.me/996552953495?text=Саламатсызбы,%20мен%20ВИП%20тарифи%20боюнча(🇰🇷корей тили)'
    )
    btn4 = types.InlineKeyboardButton(
        f'🇰🇷 Премиум\n💰 5000c', 
         url='https://wa.me/996552953495?text=Саламатсызбы,%20мен%20ПРЕМИУМ%20тарифи%20боюнча(🇰🇷корей тили)'
    )
    btn_main = types.InlineKeyboardButton('🔙 Башкы меню', callback_data='main_str')
    markup.add(btn2, btn3, btn4, btn_main)
    return markup




