import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду в следующем формате: \n <имя валюты, цену которой надо узнать>  \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты> \n Увидеть список всех доступных валют можно по команде: /values'
    bot.reply_to(message, text)



@bot.message_handler(commands=['values'])

def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
         text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров, введите 3 параметра')

        currency_from, currency_to, amount = values
        converted, base, quote, amount = CurrencyConverter.get_price(currency_from, currency_to, amount)

        text = f'{amount} {base} = {converted:.2f} {quote}'
        bot.send_message(message.chat.id, text)
        
    except APIException as e:
        bot.reply_to(message, f'Ошибка: {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    

bot.polling()