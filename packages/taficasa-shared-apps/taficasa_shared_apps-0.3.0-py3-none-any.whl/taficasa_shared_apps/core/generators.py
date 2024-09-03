import secrets


def generate_temporary_password():
    """
    Returns a temporary password of size 12 chars
    """
    symbols = "!@?&#$%"
    lower_letters = "abcdefghjkmnpqrstuvwxyz"
    upper_letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    digits = "23456789"

    max_uppers = 3
    max_lowers = 3
    max_digits = 4
    max_symbols = 2

    temp = ""

    lowers_added = 0
    uppers_added = 0
    digits_added = 0
    symbols_added = 0

    counter = 0

    while counter < 12:
        # Evaluate which chars to choose from
        char_choices = ""

        if uppers_added < max_uppers:
            char_choices += upper_letters
        if lowers_added < max_lowers:
            char_choices += lower_letters
        if digits_added < max_digits:
            char_choices += digits
        if symbols_added < max_symbols:
            char_choices += symbols

        random_char = secrets.choice(char_choices)

        if random_char.isalpha():
            if random_char.isupper():
                if uppers_added < max_uppers:
                    uppers_added += 1
                    temp += random_char
                    counter += 1
            else:
                if lowers_added < max_lowers:
                    lowers_added += 1
                    temp += random_char
                    counter += 1
        else:
            if random_char.isdigit():
                if digits_added < max_digits:
                    digits_added += 1
                    temp += random_char
                    counter += 1
            else:
                if symbols_added < max_symbols:
                    symbols_added += 1
                    temp += random_char
                    counter += 1

    return temp


def generate_temp_id(length=16):
    """
    Returns a random id of specified length.
    id consists of alphanumeric chars only
    """
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    random_id = "".join([secrets.choice(charset) for _ in range(length)])

    return random_id
