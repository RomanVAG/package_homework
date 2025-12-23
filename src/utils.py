import json
import os


def load_transactions_from_json(filepath):
    try:
        with open(filepath, encoding="UTF-8") as file:
            data = json.load(file)
        print(data)
    #   return data
    except json.JSONDecodeError:  # файл пустой
        print("File is empty")
        return []
    except ValueError:  # содержит не список
        print("File contains't  no list")
        return []
    except FileNotFoundError: # файл не найден
        print("File not found")
        return []

# Подняться на один уровень вверх, затем зайти в data
filepath = os.path.join("..", "data", "operations.json")
# Результат: "..\data\operations.json"

load_transactions_from_json(filepath)
