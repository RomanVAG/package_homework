import json
import os

def load_transactions_from_json(filepath):
    with open(filepath, encoding= "UTF-8") as file:
        data = json.load(file)
    print(data)

# Подняться на один уровень вверх, затем зайти в data
filepath = os.path.join("..", "data", "operations.json")
# Результат: "..\data\operations.json"

load_transactions_from_json(filepath)

