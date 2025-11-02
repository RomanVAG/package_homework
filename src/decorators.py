from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор log предназначен для автоматического логирования начала и конца выполнения функции,
    а также её результатов или возникших ошибок. Этот декоратор принимает необязательный аргумент filename,
    который определяет место записи логов: если filename задан, логи записываются в указанный файл,
    в противном случае они выводятся в консоль. Логирование включает в себя имя функции
    и результат выполнения при успешном завершении операции. В случае ошибки логирование фиксирует
    имя функции, тип возникшей ошибки и входные параметры, переданные в функцию.
    """

    def decorator_func(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")  # время начала вызова функции
            try:
                # Рискованный код
                result = func(*args, **kwargs)  # Вызов оригинальной функции
                # Сообщение об успешном выполнении
                log_message = f"{start_time} {func.__name__} ok: {result}"
                if filename:  # Если filename задан, логи записываются в указанный файл
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message + "\n")
                else:  # Если файл не задан, логи выводятся в консоль
                    print(log_message)  # Успешное выполнение
                return result  # возврат оригинальной функции

            except Exception as e:  # Обработка ошибок
                # Сообщение об ошибке: записываем тип и входные данные
                log_message = f"{start_time} {func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                if filename:  # Если filename задан, логи записываются в указанный файл
                    with open(filename, "a", encoding="utf-8") as file:  # Логирование информацию об ошибке
                        file.write(log_message + "\n")
                else:  # Если файл не задан, логи выводятся в консоль
                    print(log_message)
                raise  # Перебрасываем исключение дальше

        return wrapper

    return decorator_func


@log(filename="mylog.txt")
def my_function(x: int, y: int) -> int:
    """
    Пример декорируемой функции, которая принимает на вход два позиционных аргумента:
    x, y и возвращает их сумму.
    """
    return x + y


my_function(7, 6)
# # Вывод в консоль:
# # 2025/10/28, 12:00:00 my_function error: тип ошибки. Inputs: (1, 2), {}
# # 2025/10/28, 12:00:00 my_function ok: 13
