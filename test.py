# Функция 1
# Декоратор логирования
def log_decorator(func):
    def wrapper(*args, **kwargs):
        # Действие до вызова функции
        print("Я Декоратор, я могу выполнить что-то до вызова функции - Например Залогировать")

        # Вызов самой функции
        print(f"Потом я вызываю функцию {func.__name__}")
        result = func(*args, **kwargs)

        # Действие после вызова функции
        print("И в конце я выполняю что-то после вызова функции (Если надо)")
        print("Обрати внимание - я Никак не изменяю саму функцию {func.name} - Я только дополняю ее функционал")

        return result

    return wrapper


# Функция 2
# Функция создания пользователя и запрос к бд
@log_decorator
def create_user(name, age):
    user_data = {
        "name": name,
        "age": age
    }
    # Запрос к бд
    # ...
    if user_data:  # Если данные ОК
        return user_data
    else:
        return None


create_user("Иван", 25)