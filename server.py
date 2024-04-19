import json

from telebot import *

from functions import *
from variables import *
from markups import *

bot = telebot.TeleBot(API_TOKEN)

with open('users.json') as users_data:
    users = json.load(users_data)


# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)

    users[user_id] = {'last_messages': [],
                      'last_message': '',
                      'destination': '',
                      'current_note': '',
                      'current_scale': '',
                      'current_interval': '',
                      'current_chord': '',
                      'current_addition': '',
                      'last_songs': []}

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
    chat_id = call.message.chat.id
    user_id = str(call.from_user.id)

    if call.data == "Main":
        bot.answer_callback_query(call.id, "Main menu")
        message = bot.send_message(chat_id,
                                   "*Choose from the menu:*",
                                   reply_markup=main_markup,
                                   parse_mode="Markdown")
        users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])

    elif call.data == "Back":
        if call.message.id != users[user_id]['last_message']:
            bot.answer_callback_query(call.id, "Can't go back")
        else:
            bot.answer_callback_query(call.id, "Back")
            bot.delete_message(chat_id,
                               users[user_id]['last_message'])
            users[user_id]['last_messages'].pop(-1)
            users[user_id]['last_message'] = (
                users)[user_id]['last_messages'][-1]


# Handle main menu's buttons
@bot.callback_query_handler(
    func=lambda call: call.data in callback_queries_types['home'])
def main_menu_callback_handler(call):
    chat_id = call.message.chat.id
    user_id = str(call.from_user.id)
    print(type(user_id))

    if call.data == "Basics":
        bot.answer_callback_query(call.id, "Coming soon")
        message = bot.send_message(chat_id,
                                   "Sorry, this option is under development now.")
        users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])

    elif call.data == "Scale":
        bot.answer_callback_query(call.id, "Build a scale")
        users[user_id]['destination'] = call.data
        message = bot.send_message(chat_id,
                                   "Let's build a scale. In what key?",
                                   reply_markup=notes_markup,
                                   parse_mode="Markdown")
        users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])

    elif call.data == "Intervals":
        bot.answer_callback_query(call.id, "Build an interval")
        users[user_id]['destination'] = call.data
        message = bot.send_message(chat_id,
                                   "Let's build an interval. From what note?",
                                   reply_markup=notes_markup,
                                   parse_mode="Markdown")
        users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])

    elif call.data == "Chords":
        bot.answer_callback_query(call.id, "Build a chord")
        users[user_id]['destination'] = call.data
        message = bot.send_message(chat_id,
                                   "Let's build a chord. From what note?",
                                   reply_markup=notes_markup,
                                   parse_mode="Markdown")
        users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])


# Handle all other buttons
@bot.callback_query_handler(
    func=lambda call: call.data not in callback_queries_types[
        'home'] and call.data not in callback_queries_types['main'])
def main_menu_callback_handler(call):
    chat_id = call.message.chat.id
    user_id = str(call.from_user.id)

    if call.data in NOTES:
        users[user_id]["current_note"] = call.data

        bot.answer_callback_query(call.id, users[user_id]["current_note"])

        message = bot.send_message(chat_id,
                                   destinations[
                                       users[user_id][
                                           'destination']][
                                       'text'],
                                   reply_markup=
                                   destinations[
                                       users[user_id][
                                           'destination']][
                                       'markup'],
                                   parse_mode="Markdown")
        users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])

    elif call.data in SCALES:
        users[user_id]["current_scale"] = call.data
        res = '\n'.join(get_scale(users[user_id]["current_note"],
                                  users[user_id]["current_scale"]))
        songs_text = ''
        markup = finish_markup

        if users[user_id]["current_scale"] in ['Major', 'Minor']:
            current_songs = get_songs('dataset.csv', 10,
                                      NOTES_TO_NUMBERS[
                                          users[user_id]["current_note"]],
                                      SCALES_TO_NUMBERS[
                                          users[user_id]["current_scale"]])

            users[user_id]["last_songs"].append(current_songs)

            songs = '\n'.join(current_songs)
            songs_text = (f'\n\nHere are some songs written in '
                          f'_{users[user_id]["current_note"]} {users[user_id]["current_scale"]}_:\n\n{songs}')
            markup = scale_finish_markup

        bot.answer_callback_query(call.id,
                                  f'{users[user_id]["current_scale"]} mode')
        message = bot.send_message(chat_id,
                                   f'Here is your _{users[user_id]["current_note"]} '
                                   f'{users[user_id]["current_scale"]}_ scale:\n\n{res}' + songs_text,
                                   parse_mode="Markdown",
                                   reply_markup=markup)
        users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])

    elif call.data in INTERVALS:
        users[user_id]["current_interval"] = call.data
        res = get_interval(users[user_id]["current_note"],
                           users[user_id]["current_interval"])

        bot.answer_callback_query(call.id, users[user_id]["current_interval"])
        message = bot.send_message(chat_id,
                                   f'_{users[user_id]["current_interval"]} of {users[user_id]["current_note"]}_ is *{res}*',
                                   parse_mode="Markdown",
                                   reply_markup=finish_markup)
        users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])

    elif call.data in CHORDS:
        users[user_id]["current_chord"] = call.data

        bot.answer_callback_query(call.id, users[user_id]["current_chord"])

        if users[user_id]["current_chord"] == 'maj' or users[user_id][
            "current_chord"] == 'min':
            message = bot.send_message(chat_id,
                                       f'OK. Any additions?',
                                       parse_mode="Markdown",
                                       reply_markup=chords_additions_markup)
            users[user_id]['last_message'] = message.message_id

        else:
            res = get_chord(root=users[user_id]["current_note"],
                            chord=users[user_id]["current_chord"])
            message = bot.send_message(chat_id,
                                       f'Here are notes of your '
                                       f'_{users[user_id]["current_note"]}{users[user_id]["current_chord"]}_'
                                       f' chord:\n*{res}*',
                                       parse_mode="Markdown",
                                       reply_markup=finish_markup)
            users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])

    elif call.data in CHORD_ADDITIONS:
        users[user_id]["current_addition"] = call.data

        if users[user_id]["current_chord"] == 'maj':
            chord_sign = ''
        else:
            chord_sign = 'm'

        if users[user_id]["current_addition"] == 'None':
            addition_sign = ''
        else:
            addition_sign = users[user_id]["current_addition"]

        bot.answer_callback_query(call.id, users[user_id]["current_addition"])

        res = get_chord(root=users[user_id]['current_note'],
                        chord=users[user_id]['current_chord'],
                        addition=users[user_id]["current_addition"])
        message = bot.send_message(chat_id,
                                   f'Here are notes of your '
                                   f'_{users[user_id]["current_note"]}{chord_sign}'
                                   f'{addition_sign}_ chord:\n*{res}*',
                                   parse_mode="Markdown",
                                   reply_markup=finish_markup)
        users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])

    elif call.data == 'More':
        bot.answer_callback_query(call.id, 'More songs')

        current_songs = get_songs('dataset.csv', 20,
                                  NOTES_TO_NUMBERS[
                                      users[user_id]['current_note']],
                                  SCALES_TO_NUMBERS[
                                      users[user_id]["current_scale"]])

        while any(
                map(lambda s: len(set(s).intersection(set(current_songs))) > 4,
                    users[user_id]["last_songs"])):
            current_songs = get_songs('dataset.csv', 20,
                                      NOTES_TO_NUMBERS[
                                          users[user_id]['current_note']],
                                      SCALES_TO_NUMBERS[
                                          users[user_id]["current_scale"]])

        users[user_id]["last_songs"].append(current_songs)

        songs = '\n'.join(current_songs)
        songs_text = (f'\n\nHere are some more songs written in '
                      f'_{users[user_id]["current_note"]} {users[user_id]["current_scale"]}_:\n\n{songs}')

        message = bot.send_message(chat_id, songs_text,
                                   parse_mode="Markdown",
                                   reply_markup=scale_finish_markup)
        users[user_id]['last_message'] = message.message_id

        users[user_id]['last_messages'].append(users[user_id]['last_message'])


if __name__ == "__main__":
    print(users)
    bot.polling()

    # Save data before exiting
    with open('users.json', 'w') as users_data:
        json.dump(users, users_data)
    print("Data saved to data.json. Exiting...")