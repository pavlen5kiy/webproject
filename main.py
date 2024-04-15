#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

from telebot import *
from telebot.util import quick_markup

from notes_and_scales import *

API_TOKEN = '7161683104:AAHqONitwtt3N4x2Wx-2MFMxC55f-d0ShVU'

bot = telebot.TeleBot(API_TOKEN)

start_markup = quick_markup({
    'Learn basics': {'callback_data': 'Basics'},
    'Build a scale': {'callback_data': 'Scale'},
}, row_width=2)

key_markup = quick_markup({
    'C': {'callback_data': 'C'},
    'C#\Db': {'callback_data': 'C#\Db'},
    'D': {'callback_data': 'D'},
    'D#\Eb': {'callback_data': 'D#\Eb'},
    'E': {'callback_data': 'E'},
    'F': {'callback_data': 'F'},
    'F#\Gb': {'callback_data': 'F#\Gb'},
    'G': {'callback_data': 'G'},
    'G#\Ab': {'callback_data': 'G#\Ab'},
    'A': {'callback_data': 'A'},
    'A#\Bb': {'callback_data': 'A#\Bb'},
    'B\Cb': {'callback_data': 'B\Cb'}
}, row_width=4)

scale_markup = quick_markup({
    'Major': {'callback_data': 'Major'},
    'Minor': {'callback_data': 'Minor'},
    'Major Pentatonic': {'callback_data': 'Major Pentatonic'},
    'Minor Pentatonic': {'callback_data': 'Minor Pentatonic'},
    'Blues': {'callback_data': 'Blues'},
    'Dorian': {'callback_data': 'Dorian'},
}, row_width=2)

current_key = ''
current_scale = ''


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, """\
Hi there, I am MusicTheoryBot.
I am here to help you with music theory!
Maybe you want me to build a scale or give you some basic knowledges. Whatever you want!\
""", reply_markup=start_markup)


@bot.callback_query_handler(func=lambda call: True)
def start_callback_handler(call):
    global current_scale
    global current_key

    chat_id = call.message.chat.id

    if call.data == "Basics":
        bot.answer_callback_query(call.id, "Coming soon")
        bot.send_message(chat_id, "Sorry, this option is in development now.")
    elif call.data == "Scale":
        bot.answer_callback_query(call.id, "Build a scale")
        bot.send_message(chat_id,
                         "Let's build a scale. What key do you want it in?",
                         reply_markup=key_markup)

    elif call.data in NOTES:
        current_key = call.data

        bot.answer_callback_query(call.id, f'{current_key} key')

        bot.send_message(chat_id, 'OK. What scale do you want?',
                         reply_markup=scale_markup)

    elif call.data in SCALES:
        current_scale = call.data
        res = ', \n'.join(get_scale(current_key, current_scale))

        bot.answer_callback_query(call.id, f'{current_scale} scale')
        bot.send_message(chat_id,
                         f'Here is your *{current_key} {current_scale}* scale:\n\n{res}',
                         parse_mode="Markdown")


if __name__ == "__main__":
    bot.polling()
