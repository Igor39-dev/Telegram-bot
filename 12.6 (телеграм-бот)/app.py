import telebot
import requests
import json

APIkey = 'QTBtzCeH5LjU6YntGoaQ362oD6vCY4SE'
TOKEN = '8024038321:AAEIRsQlAPNASjdryeo7ZVoukHS0G1oyPJI'

url = "https://api.apilayer.com/exchangerates_data/convert?to=to&from=from&amount=amount"

payload = {}
headers= {
  "apikey": "QTBtzCeH5LjU6YntGoaQ362oD6vCY4SE"
}
response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text


bot = telebot.TeleBot(TOKEN)

keys = {'доллар': 'USD',
        'евро': 'EUR',
        'рубли': 'RUB',
}




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
    currency_from, currency_to, amount = message.text.lower().split(' ')
    amount = float(amount)

    from_code = keys[currency_from]
    to_code = keys[currency_to]

    # r = requests.get(url, headers=headers)
    r = requests.get(f'https://api.apilayer.com/exchangerates_data/convert?from={from_code}&to={to_code}&amount={amount}', headers=headers)
    
    data = json.loads(r.content)
    converted = data['result']

    text = f'{amount} {from_code} = {converted:.2f} {to_code}'
    bot.send_message(message.chat.id, text)
    

bot.polling()