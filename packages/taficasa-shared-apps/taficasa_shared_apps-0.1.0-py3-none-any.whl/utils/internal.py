def generate_test_account_email(account_name: str) -> str:
    """
    Generates test account email using standard format
    """

    return f"{account_name}@test.taficasa.com"


def strtobool(val):
    """Convert a string representation of bool value to true or false.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))
