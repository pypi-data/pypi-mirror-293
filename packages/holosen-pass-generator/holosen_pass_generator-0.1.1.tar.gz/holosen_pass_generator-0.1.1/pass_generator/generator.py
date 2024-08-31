import random
import string
from enum import Enum


class Complexity(Enum):
    SIMPLE = 1  # فقط عدد
    MEDIUM = 2  # عدد و حروف
    COMPLEX = 3  # عدد، حروف و کاراکترهای خاص


def generate_password(length: int, complexity: Complexity) -> str:
    if complexity == Complexity.SIMPLE:
        characters = string.digits
    elif complexity == Complexity.MEDIUM:
        characters = string.ascii_letters + string.digits
    elif complexity == Complexity.COMPLEX:
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        raise ValueError("Complexity level not supported")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password
