#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot

API_TOKEN = '7161683104:AAHqONitwtt3N4x2Wx-2MFMxC55f-d0ShVU'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am MusicTheoryBot.
I am here to help you with music theory. Maybe you want me to build a scale or give you some basic knowledges. Whatever you want!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_audio(message, "Sorry, I don't get it")


if __name__ == "__main__":
    bot.polling()
