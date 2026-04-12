import json
import os
from dotenv import load_dotenv
import requests


def conversion_from_USD_and_EUR_to_RUB(parsed_data: dict) -> float:
    """
    Функция конвертации валюты из USD и EUR в рубли. Принимает на вход словарь
    с данными о транзакции и возвращает сумму транзакции (ключ amount) в рублях,
    тип данных float. Если транзакция была в USD или EUR, происходит обращение к внешнему API
    для получения текущего курса валют и конвертации суммы операции в рубли.
    """
    # Получение значения переменной currency из parsed_data по ключу code
    currency = parsed_data["operationAmount"]["currency"]["code"]

    # Загрузка переменных из .env-файла
    load_dotenv()

    # Получение значения переменной API_KEY из .env-файла
    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        print("API ключ не загружен или пуст")

    # Получение значения переменной amount_float из parsed_data по ключу amount
    amount_float = float(parsed_data["operationAmount"]["amount"])

    # Задаем адрес сайта, к которому хотим обратиться
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount_float}"

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
        content = response.json()
        return content.get("result", 0.0)  # Получаем значение конвертированной суммы
    else:
        # Выводим сообщение об ошибке
        print(f"Запрос не был успешным. Возможная причина: {response.reason}")


# Примеры данных с транзакциями в формате JSON - строк
data_RUB = '''{
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

data_USD = '''{
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

data_EUR = '''{
    "id": 782295999,
    "state": "EXECUTED",
    "date": "2019-09-11T17:30:34.445824",
    "operationAmount": {
        "amount": "54280.01",
        "currency": {
            "name": "EUR",
            "code": "EUR"
        }
    },
    "description": "Перевод организации",
    "from": "Счет 24763316288121894080",
    "to": "Счет 96291777776753236930"
    }'''

# Преобразуем словарь с данными о транзакции в формате JSON-строки в словарь Python типа dict
parsed_data = json.loads(data_EUR)

# Результат:

result = conversion_from_USD_and_EUR_to_RUB(parsed_data)
result
