from typing import Optional, Callable, Any
from datetime import datetime


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор, который будет автоматически логировать начало и конец выполнения функции,
    а также ее результаты или возникшие ошибки. Декоратор должен принимать необязательный аргумент
    filename, который определяет, куда будут записываться логи (в файл или в консоль):
    Если filename задан, логи записываются в указанный файл. Если filename не задан, логи выводятся в консоль.
    Логирование должно включать:Имя функции и результат выполнения при успешной операции.
    Имя функции, тип возникшей ошибки и входные параметры, если выполнение функции привело к ошибке.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Логируем начало выполнения
            start_time = datetime.now()
            start_message = f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - {func.__name__} started. args: {args}, kwargs: {kwargs}"

            if filename:
                with open(filename, 'a', encoding='utf-8') as file:
                    file.write(start_message + '\n')
            else:
                print(start_message)

            try:
                # Выполняем исходную функцию
                result = func(*args, **kwargs)
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()

                # Логируем успешное завершение
                message = f"{end_time.strftime('%Y-%m-%d %H:%M:%S')} - {func.__name__} ok. Result: {result}. Execution time: {execution_time:.3f}s"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as file:
                        file.write(message + '\n')
                else:
                    print(message)

                return result

            except Exception as e:
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()

                # Логируем ошибку
                message = f"{end_time.strftime('%Y-%m-%d %H:%M:%S')} - {func.__name__} error: {type(e).__name__}. args: {args}, kwargs: {kwargs}. Execution time: {execution_time:.3f}s"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as file:
                        file.write(message + '\n')
                else:
                    print(message)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator


@log()
def my_function(x: int, y: int) -> int:
    return x + y