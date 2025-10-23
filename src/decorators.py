from typing import Optional, Callable, Any
from datetime import datetime


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор log предназначен для автоматического логирования начала и конца выполнения функции,
    а также её результатов или возникших ошибок. Этот декоратор принимает необязательный аргумент filename,
    который определяет место записи логов: если filename задан, логи записываются в указанный файл,
    в противном случае они выводятся в консоль. Логирование включает в себя имя функции
    и результат выполнения при успешном завершении операции. В случае ошибки логирование фиксирует
    имя функции, тип возникшей ошибки и входные параметры, переданные в функцию.
    """
    def decorator_func(func: Any) -> Any:
        def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any | None:
            start_time = datetime.now().replace(microsecond=0)  # время начала вызова функции
            try:
                # Рискованный код
                func(*args, **kwargs)  # Вызов оригинальной функции
                if filename:   # Если filename задан, логи записываются в указанный файл
                    with open("mylog.txt", "a", encoding='utf-8') as _:  # Логирование информации об ошибке
                        _.write(f"{start_time} {func.__name__} ok \n")
                else: # Если файл не задан, логи выводятся в консоль
                    print(f"{start_time} {func.__name__} ok \n")
                return func # возврат оригинальной функции

            except Exception as e:  # Обработка ошибок
                if filename: # Если filename задан, логи записываются в указанный файл
                    with open("mylog.txt", "a", encoding='utf-8') as _:  # Логирование информацию об ошибке
                        _.write(f"{start_time} {func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs} \n")
                else: # Если файл не задан, логи выводятся в консоль
                    print(f"{start_time} {func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs} \n")

        return wrapper

    return decorator_func


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


my_function("7", 6)
# # Вывод в консоль:
# # 2024-01-15 14:30:25 - my_function error: тип ошибки. Inputs: (1, 2), {}
# # 2024-01-15 14:30:25 - my_function ok