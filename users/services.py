import random
import string


def generate_temp_email():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))  # Генерация случайной строки
    temp_email = f"temp_{random_string}@example.com"  # Создание временного email адреса
    return temp_email
