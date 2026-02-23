import json
import os


def load_transactions_from_json(filepath):
    """Функция чтения JSON-файла возвращает список словарей с данными о финансовых транзакциях.
     Функция принимает на вход путь к JSON файлу в качестве аргумента."""
    try:
        with open(filepath, encoding="UTF-8") as file:
            data = json.load(file)
        print(data)
    #   return data
    except json.JSONDecodeError:  # файл пустой
        print("File is empty")
        return [] # возвращается пустой список.
    except ValueError:  # содержит не список
        print("File contains't  no list")
        return [] # возвращается пустой список.
    except FileNotFoundError: # файл не найден
        print("File not found")
        return [] # возвращается пустой список.

# Подняться на один уровень вверх, затем зайти в data
filepath = os.path.join("..", "data", "operations.json") # путь к файлу JSON
# Результат: "..\data\operations.json"

load_transactions_from_json(filepath)
