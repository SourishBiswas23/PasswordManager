import random
import string


def random_password():
    password = ""
    for _ in range(8):
        password += random.choice(string.ascii_letters)
    for _ in range(4):
        password += random.choice(string.digits)
    for _ in range(4):
        password += random.choice(string.punctuation)
    password = list(password)
    random.shuffle(password)
    password = "".join(password)
    return password
