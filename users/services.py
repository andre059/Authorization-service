import random
import string


def generate_authorization_code():
    """Генерирует код авторизации"""

    return ''.join(random.choices(string.digits, k=6))
