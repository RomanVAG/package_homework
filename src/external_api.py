import json
import os
from dotenv import load_dotenv
import requests


def conversion_from_USD_and_EUR_to_RUB(parsed_data: dict) -> float:
    """
    Функция конвертации валюты из USD и EUR в рубли. Принимает на вход словарь
    с данными data о транзакции id и возвращает сумму транзакции (ключ amount) в рублях,
    тип данных float. Если транзакция была в USD или EUR, происходит обращение к внешнему API
    для получения текущего курса валют и конвертации суммы операции в рубли.
    """
    # возвращается значение словаря по ключу operationAmount -> amount
    if parsed_data["operationAmount"]["currency"]["code"] == "USD":
        # Загрузка переменных из .env-файла
        load_dotenv()

        # Получение значения переменной API_KEY из .env-файла
        API_KEY = os.getenv('API_KEY')

        # Получение значения переменной amount_USD из parsed_data по ключу amount
        amount_float = float(parsed_data["operationAmount"]["amount"])

        # Задаем адрес сайта, к которому хотим обратиться
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount={amount_float}"

        payload = {}
        headers = {
            "apikey": API_KEY
        }
        # Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
        response = requests.request("GET", url, headers=headers, data=payload)
        # Получаем статус-код из ответа и выводим его на экран
        status_code = response.status_code
        result = response.text

        # Проверяем, равен ли статус-код 200, то есть чтобы запрос был успешным
        if status_code == 200:
            # Выводим содержимое сайта на экран
            content = response.text
            print(f"Содержимое сайта:\n{content}")
        else:
            # Выводим сообщение об ошибке
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")

    else:
        return parsed_data["operationAmount"]["amount"]  # возвращаем сумму операции в рубли


# data - строка, тип str
data_1 = '''{
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
    }'''

data_2 = '''{
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
      "amount": "8221.37",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560"
    }'''

# parsed_data - словарь, тип dict
parsed_data = json.loads(data_2)

# Результат: "
# "8221.37",
result = conversion_from_USD_and_EUR_to_RUB(parsed_data)
print(result)
