import requests
import json
from config import keys, headers


class ConvertionException(Exception):
    pass


class CurrencyConverter:

    @staticmethod
    def get_price(currency_from: str, currency_to: str, amount: str):

        if currency_from == currency_to:
            raise ConvertionException('Невозможно перевести одинаковые валюты')

        try:
            base = keys[currency_from]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту \n доступные валюты /values')
            
        try:
            quote = keys[currency_to]
        except KeyError:
            raise ConvertionException('Не удалось обработать валюту \n доступные валюты /values')
            
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Не удалось обработать количество')

        
        # r = requests.get(url, headers=headers)
        r = requests.get(f'https://api.apilayer.com/exchangerates_data/convert?from={base}&to={quote}&amount={amount}', headers=headers)
            
        data = json.loads(r.content)
        converted = data['result']
        return converted, base, quote, amount