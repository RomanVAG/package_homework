import os
from dotenv import load_dotenv
import requests
from src.utils import load_transactions_from_json

# Загрузка переменных из .env-файла
load_dotenv()

# Получение значения переменной API_KEY из .env-файла
API_KEY = os.getenv('API_KEY')

# Задаем адрес сайта, к которому хотим обратиться
url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=amount"

payload = {}
headers= {
  "apikey": API_KEY
}
# Выполняем GET-запрос к сайту и сохраняем ответ в переменную response
response = requests.request("GET", url, headers=headers, data = payload)
# Получаем статус-код из ответа и выводим его на экран
status_code = response.status_code
result = response.text
print(f"Статус код: {status_code}")

# Проверяем, равен ли статус-код 200, то есть чтобы запрос был успешным
if status_code == 200:
    # Выводим содержимое сайта на экран
    content = response.text
    print(f"Содержимое сайта:\n{content}")
else:
    # Выводим сообщение об ошибке
    print(f"Запрос не был успешным. Возможная причина: {response.reason}")

def conversion_from_USD_and_EUR_to_RUB(id, amount) -> float:
    """
    Функция, которая принимает на вход транзакцию (id), сумму (amount) и возвращает сумму транзакции
    (amount) в рублях, тип данных — float. Если транзакция была в USD или EUR, происходит обращение
    к внешнему API для получения текущего курса валют и конвертации суммы операции в рубли.
    """
    pass


"""
# Подняться на один уровень вверх, затем зайти в data
filepath = os.path.join("..", "data", "operations.json") # путь к файлу JSON
# Результат: "..\data\operations.json"

data = load_transactions_from_json(filepath)
data
"""