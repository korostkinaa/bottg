import telebot

TOKEN = "5564454053:AAGbprlQJgGfLakRgOpPfSYGuUoHX9aOVW4"
bot = telebot.TeleBot(TOKEN)
from telebot import types
import random
from dicts import *

chats = {}


@bot.message_handler(commands=['start'])
def start_menu(message):
    keyb = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, description, reply_markup=keyb.add(
        types.InlineKeyboardButton("Выбрать группу", url="https://telegram.me/korostkina_falshunova_bot?startgroup=")),
                     parse_mode='Markdown')
    bot.delete_message(message.chat.id, message.message_id)
    chats[message.chat.id] = {}


@bot.message_handler(commands=['play'])
def start_game(message):
    keyb = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, "выбери категорию", reply_markup=keyb.add(
        types.InlineKeyboardButton("Нажите, чтобы учавстовать", callback_data="check"),
        types.InlineKeyboardButton("Нажите, если вы готовы", callback_data="go")))


@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    if call.data == "check":
        chats.update({call.message.chat.id: {call.from_user.username: 0, "num": None, "catch": True, 'step': 0}})
        print(chats)
    elif call.data == "go":
        initilaze_dict(call.message.chat.id)
    elif call.data == "IDK":
        bot.send_message(call.message.chat.id,
                         f'Какие вы ТУПЫЕ.\nОтвет: *{QA[chats[call.message.chat.id]["num"]]["right"]}*',
                         parse_mode='Markdown')
        chats[call.message.chat.id][call.from_user.username] -= 1
        initilaze_dict(call.message.chat.id)


def initilaze_dict(id):
    chats[id]['step'] += 1
    randomize = chats[id]['step']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    [keyboard.add(types.KeyboardButton(button)) for button in QA[randomize]["variants"]]
    bot.send_message(id, f'*{QA[randomize]["caption"]}*', reply_markup=keyboard, parse_mode='Markdown')
    keyb = types.InlineKeyboardMarkup()
    bot.send_message(id, random.choice(phrase),
                     reply_markup=keyb.add(types.InlineKeyboardButton("Я не знаю...", callback_data="IDK")))
    chats[id]["num"] = randomize


def catch_error(message):
    try:
        return chats[message.chat.id]['catch']
    except KeyError:
        return False


@bot.message_handler(content_types=['text'], func=lambda message: catch_error(message))
def check_answer(message):
    print(chats)
    if message.text.lower() == QA[chats[message.chat.id]["num"]]['right'].lower() and chats[message.chat.id][
        message.from_user.username] < 15:
        chats[message.chat.id][message.from_user.username] += 1
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEE0qpijyo37rRJf3zjguFKa7EPFUvlCgACEAMAAm2wQgOS41nh81K2aSQE")
        bot.send_message(message.chat.id, f"Отличная работа @*{message.from_user.username}*!!!!", parse_mode='Markdown')
        initilaze_dict(message.chat.id)
    elif chats[message.chat.id][message.from_user.username] == 2:
        bot.send_message(message.chat.id, f"ПОЗДРАВЛЯЮ С ПОБЕДОЙ! @{message.from_user.username}!!!!",
                         parse_mode='Markdown')
        chats[message.chat.id] = {}


bot.infinity_polling()
