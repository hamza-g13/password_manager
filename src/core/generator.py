import string
import secrets

def generate_password(length: int, use_lower: bool, use_upper: bool, use_digits: bool, use_symbols: bool):
    if length < 8:
        raise ValueError("Length must be greater than 8.")

    chars = ""

    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation

    if not chars:
        raise ValueError("You need to choose at least one option")

    while True:
        password = ''.join(secrets.choice(chars) for i in range(length))

        if check_password(password,use_lower,use_upper,use_digits,use_symbols):
            return password
        print("False")


def check_password(password: string ,use_lower: bool, use_upper: bool, use_digits: bool, use_symbols: bool ):
    result = True
    if use_lower:
        if not any(char in string.ascii_lowercase for char in password):
            result = False

    if use_upper:
        if not any(char in string.ascii_uppercase for char in password):
            result = False

    if use_digits:
        if not any(char in string.digits for char in password):
            result = False

    if use_symbols:
        if not any(char in string.punctuation for char in password):
            result = False

    return result