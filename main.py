from telebot import *

from functions import *
from variables import *
from markups import *

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, """\
Hi there, I am MusicTheoryBot 🎶
I am here to help you with music theory!
Maybe you want me to build a scale or give you some basic information. Whatever you want!\
""", reply_markup=start_markup)


# Handle '/home'
@bot.message_handler(commands=['home'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "*Choose from the menu:*",
                     reply_markup=main_markup,
                     parse_mode="Markdown")


# Handle non-command messages
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_non_command_messages(message):
    # Handle non-command messages here
    bot.send_message(message.chat.id, "Please, send commands only.")


# Handle "main menu" and "back" buttons
@bot.callback_query_handler(
    func=lambda call: call.data in callback_queries_types['main'])
def main_callbacks_handler(call):
    global last_message
    global last_messages

    chat_id = call.message.chat.id

    if call.data == "Main":
        bot.answer_callback_query(call.id, "Main menu")
        last_message = bot.send_message(chat_id, "*Choose from the menu:*",
                                        reply_markup=main_markup,
                                        parse_mode="Markdown")

        last_messages.append(last_message)

    elif call.data == "Back":
        if call.message.id != last_message.id:
            bot.answer_callback_query(call.id, "Can't go back")
        else:
            bot.answer_callback_query(call.id, "Back")
            bot.delete_message(chat_id, last_message.message_id)
            last_messages.pop(-1)
            last_message = last_messages[-1]


# Handle main menu's buttons
@bot.callback_query_handler(
    func=lambda call: call.data in callback_queries_types['home'])
def main_menu_callback_handler(call):
    global destination
    global last_messages
    global last_message

    chat_id = call.message.chat.id

    if call.data == "Basics":
        bot.answer_callback_query(call.id, "Coming soon")
        last_message = bot.send_message(chat_id,
                                        "Sorry, this option is under development now.")

        last_messages.append(last_message)

    elif call.data == "Scale":
        bot.answer_callback_query(call.id, "Build a scale")
        destination = call.data
        last_message = bot.send_message(chat_id,
                                        "Let's build a scale. In what key?",
                                        reply_markup=notes_markup,
                                        parse_mode="Markdown")

        last_messages.append(last_message)

    elif call.data == "Intervals":
        bot.answer_callback_query(call.id, "Build an interval")
        destination = call.data
        last_message = bot.send_message(chat_id,
                                        "Let's build an interval. From what note?",
                                        reply_markup=notes_markup,
                                        parse_mode="Markdown")

        last_messages.append(last_message)

    elif call.data == "Chords":
        bot.answer_callback_query(call.id, "Build a chord")
        destination = call.data
        last_message = bot.send_message(chat_id,
                                        "Let's build a chord. From what note?",
                                        reply_markup=notes_markup,
                                        parse_mode="Markdown")

        last_messages.append(last_message)


# Handle all other buttons
@bot.callback_query_handler(
    func=lambda call: call.data not in callback_queries_types[
        'home'] and call.data not in callback_queries_types['main'])
def main_menu_callback_handler(call):
    global current_scale
    global current_note
    global current_interval
    global last_message
    global destination
    global last_messages
    global current_chord
    global current_addition

    chat_id = call.message.chat.id

    if call.data in NOTES:
        current_note = call.data

        bot.answer_callback_query(call.id, current_note)

        last_message = bot.send_message(chat_id,
                                        destinations[destination]['text'],
                                        reply_markup=destinations[destination][
                                            'markup'], parse_mode="Markdown")

        last_messages.append(last_message)

    elif call.data in SCALES:
        current_scale = call.data
        res = '\n'.join(get_scale(current_note, current_scale))
        songs_text = ''

        if current_scale in ['Major', 'Minor']:
            songs = '\n'.join(get_songs('dataset.csv', 10,
                              NOTES_TO_NUMBERS[current_note],
                              SCALES_TO_NUMBERS[current_scale]))
            songs_text = (f'\n\nHere are some songs written in '
                          f'_{current_note} {current_scale}_:\n\n{songs}')

        bot.answer_callback_query(call.id, f'{current_scale} mode')
        last_message = bot.send_message(chat_id,
                                        f'Here is your _{current_note} '
                                        f'{current_scale}_ scale:\n\n{res}' + songs_text,
                                        parse_mode="Markdown",
                                        reply_markup=finish_markup)

        last_messages.append(last_message)

    elif call.data in INTERVALS:
        current_interval = call.data
        res = get_interval(current_note, current_interval)

        bot.answer_callback_query(call.id, current_interval)
        last_message = bot.send_message(chat_id,
                                        f'_{current_interval} of {current_note}_ is *{res}*',
                                        parse_mode="Markdown",
                                        reply_markup=finish_markup)

        last_messages.append(last_message)

    elif call.data in CHORDS:
        current_chord = call.data

        bot.answer_callback_query(call.id, current_chord)

        if current_chord == 'maj' or current_chord == 'min':
            last_message = bot.send_message(chat_id,
                                            f'OK. Any additions?',
                                            parse_mode="Markdown",
                                            reply_markup=chords_additions_markup)
        else:
            res = get_chord(current_note, current_chord)
            last_message = bot.send_message(chat_id,
                                            f'Here are notes of your '
                                            f'_{current_note}{current_chord}_'
                                            f' chord:\n*{res}*',
                                            parse_mode="Markdown",
                                            reply_markup=finish_markup)

        last_messages.append(last_message)

    elif call.data in CHORD_ADDITIONS:
        current_addition = call.data
        
        if current_chord == 'maj':
            chord_sign = ''
        else:
            chord_sign = 'm'

        if current_addition == 'None':
            addition_sign = ''
        else:
            addition_sign = current_addition

        bot.answer_callback_query(call.id, current_addition)

        res = get_chord(current_note, current_chord, current_addition)
        last_message = bot.send_message(chat_id,
                                        f'Here are notes of your '
                                        f'_{current_note}{chord_sign}'
                                        f'{addition_sign}_ chord:\n*{res}*',
                                        parse_mode="Markdown",
                                        reply_markup=finish_markup)

        last_messages.append(last_message)


if __name__ == "__main__":
    bot.polling()
