import os

import telebot as tl
from telebot.types import CallbackQuery, Message

import stock_api
import utils

bot = tl.TeleBot(os.environ.get('TOKEN'), parse_mode='html')


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, 'Greeting! My name is Alex and I can show you stock prices.\n'
                                      'To get the stock prices press /price and choose a company you are interested '
                                      'in.\n '
                                      'To get help press /help')


@bot.message_handler(commands=['help'])
def send_help(message: Message):
    keyboard = tl.types.InlineKeyboardMarkup()
    keyboard.add(
        tl.types.InlineKeyboardButton(
            'Message to developer', url='telegram.me/BotFather'
        )
    )
    bot.send_message(message.chat.id,
                     '1) Press /price.\n\n'
                     '2) Choose a company you are interested in.', reply_markup=keyboard)


@bot.message_handler(commands=['price'])
def share_price_command(message):
    keyboard = utils.generate_keyboard()
    bot.send_message(message.chat.id,
                     'Please, choose a company.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda query: query.data.startswith('$$'))
def callback(query: CallbackQuery):
    bot.answer_callback_query(query.id)
    chat_id = query.message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    stock_symbol = query.data[2:]
    analytics = stock_api.get_stock_analytics(stock_symbol=stock_symbol)
    bot.send_message(chat_id, f'The current shares price of <b>{analytics.get("company_name")}</b> is '
                              f'<b>{analytics.get("current_price"):.2f} {analytics.get("currency")}</b> '
                              f'{analytics.get("emoji")}\n', parse_mode='html')
    bot.send_photo(chat_id, analytics.get('figure'))


bot.polling(none_stop=True)
